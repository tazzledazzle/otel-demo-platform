# Codebase Concerns

**Analysis Date:** 2025-02-24

**Scope:** `otel-demo-platform`

## Tech Debt

**Telemetry duplication (Kotlin):**
- Issue: Same `initOpenTelemetry` logic in `api/src/main/kotlin/dev/otel/demo/api/Telemetry.kt` and `worker/src/main/kotlin/dev/otel/demo/worker/Telemetry.kt` (identical OTLP + W3C setup).
- Files: `api/.../Telemetry.kt`, `worker/.../Telemetry.kt`
- Impact: Changes to exporter or resource must be done twice; risk of drift.
- Fix approach: Extract shared module (e.g. `otel-common` or a Gradle source set) or publish a small shared library and depend from api/worker.

**No app containerization:**
- Issue: Only infrastructure is in Docker (`docker-compose.yml`); API, worker, and agent are run via `./gradlew run` and `python -m agent.main`.
- Files: Repo root; no Dockerfiles.
- Impact: Inconsistent or manual production-like runs; no single-command “run full stack in containers.”
- Fix approach: Add Dockerfiles for api, worker, and agent (multi-stage if desired) and optional docker-compose profile to run app services.

**API port hardcoded:**
- Issue: API listens on 8080 in `api/src/main/kotlin/dev/otel/demo/api/Main.kt` with no env override.
- Files: `api/.../Main.kt`
- Impact: Cannot change port without code change or env support.
- Fix approach: Read port from env (e.g. `API_PORT`) with default 8080.

## Known Bugs

- None explicitly documented in project source. No TODO/FIXME in app code (only in vendored/.venv deps).

## Security Considerations

**No authentication:**
- Risk: API, worker, and agent expose endpoints with no auth; any caller can trigger workflows and agent invocations.
- Files: All route and activity entry points.
- Current mitigation: None; intended for local/demo.
- Recommendations: For any non-local use, add auth (API key, JWT, or mTLS) and document that default setup is insecure.

**Secrets in docker-compose:**
- Risk: `docker-compose.yml` contains literal Postgres and Temporal credentials (temporal/temporal).
- Files: `otel-demo-platform/docker-compose.yml`
- Current mitigation: Typically not committed with real production secrets; fine for local dev.
- Recommendations: Use env files or secrets management for any shared or production deployment; do not commit production secrets.

## Performance Bottlenecks

**Blocking HTTP in Temporal activity:**
- Problem: Worker calls agent via `runBlocking` in `worker/.../client/AgentClient.kt`; activity thread is blocked for the full HTTP + LLM round-trip.
- Files: `worker/.../client/AgentClient.kt`
- Cause: Ktor client used in synchronous way inside activity.
- Improvement path: Prefer coroutine-based client and run activity in a non-blocking way if Temporal Kotlin supports async activities, or accept blocking with appropriate activity timeouts (currently 2 minutes).

**No connection pooling or client reuse:**
- Problem: `AgentClient.kt` uses a single shared `HttpClient` (good) but no explicit tuning; agent calls can be slow (LLM).
- Impact: Under load, activity timeout or thread usage may become an issue.
- Improvement path: Ensure single client instance (already so), consider timeouts and retries for agent HTTP calls.

## Fragile Areas

**Chat route without Temporal mock:**
- Files: `api/src/test/kotlin/dev/otel/demo/api/routes/ChatRoutesTest.kt`
- Why fragile: Test only verifies route registration; calling POST /chat would require real Temporal. Any refactor that breaks workflow start or response handling is not caught by unit tests.
- Safe modification: When changing ChatRoutes or TemporalClientFactory, run manual or integration test (docs/TESTING.md).
- Test coverage: No unit test for full chat handler path.

**Worker activity test:**
- Files: `worker/src/test/kotlin/dev/otel/demo/worker/RunAgentActivityTest.kt`
- Why fragile: Only asserts that RunAgentActivity implements the interface; does not test agent HTTP call, error handling, or serialization.
- Safe modification: Add test that mocks HTTP (e.g. mock server or mock Ktor client) and asserts reply propagation.
- Test coverage: Activity behavior and AgentClient are untested by unit tests.

**Agent executor and chain:**
- Files: `agent/agent/chain.py`, `agent/agent/main.py`
- Why fragile: Chain and _Executor are coupled to LangChain/Ollama; changes in prompt or tool set can break invoke contract expected by worker.
- Safe modification: Keep worker’s `InvokeResponse(reply)` and agent’s `InvokeResponse(reply=...)` in sync; add contract test or shared schema if payload evolves.
- Test coverage: test_chain and test_main cover happy path with mocks; no tests for malformed input or LLM errors.

## Scaling Limits

**Single worker process:**
- Current capacity: One worker process per task queue; activities run on that process.
- Limit: Throughput bounded by single JVM and activity timeout (2 min); no horizontal scaling of workers documented.
- Scaling path: Run multiple worker processes (same task queue) for more throughput; ensure agent can handle concurrent requests (FastAPI/uvicorn can).

**Agent single instance:**
- No load balancing or replication in repo; scaling agent is out of scope for current design.

## Dependencies at Risk

**Python lockfile:**
- Risk: No committed lockfile (e.g. requirements.txt or uv.lock); `pip install -e ".[dev]"` resolves at install time.
- Impact: Different environments may get different minor/patch versions; builds not reproducible.
- Migration plan: Add lockfile (e.g. `pip freeze > requirements.txt` for CI, or use uv/poetry with lockfile) and pin in CI.

**Temporal and OTel versions:**
- Kotlin: Temporal 1.24.0, OTel 1.35.0; Gradle does not use strict resolution or BOM in the scanned files.
- Impact: Future upgrades may require compatibility check (Temporal server in docker-compose is 1.24.2).
- Recommendation: Align Temporal server and SDK versions when upgrading; test workflow and activities after OTel upgrades.

## Missing Critical Features

**No automated integration/E2E:**
- Problem: Full flow (API → Temporal → Worker → Agent) is only documented as manual steps; no script or CI job.
- Blocks: Regression detection for end-to-end behavior; onboarding “one-command” verification.
- Recommendation: Add script (e.g. shell or Makefile) or CI job that starts infra + services and runs a single POST /chat assertion, or use Testcontainers for Temporal.

**No health of dependencies:**
- Problem: API /health does not check Temporal connectivity; agent /health does not check Ollama.
- Blocks: Orchestrators cannot distinguish “process up but Temporal down” or “Ollama unreachable.”
- Recommendation: Optional readiness checks that ping Temporal (API) and Ollama (agent), behind config or separate endpoint.

## Test Coverage Gaps

**API chat path:**
- What’s not tested: Receiving body, creating workflow stub, calling `run`, returning ChatResponse; TemporalClientFactory creation with env.
- Files: `api/.../routes/ChatRoutes.kt`, `api/.../TemporalClientFactory.kt`
- Risk: Regressions in request/response or workflow options go unnoticed in unit tests.
- Priority: Medium (manual E2E exists).

**Worker activity and HTTP client:**
- What’s not tested: agentInvoke with real or mock HTTP; error handling when agent returns 5xx or timeouts.
- Files: `worker/.../RunAgentActivity.kt`, `worker/.../client/AgentClient.kt`
- Risk: Changes to URL building or response parsing can break production path.
- Priority: Medium.

**Agent error paths:**
- What’s not tested: Invalid JSON, missing fields, LLM or chain exceptions, non-200 from Ollama.
- Files: `agent/agent/main.py`, `agent/agent/chain.py`
- Risk: Unhandled exceptions or poor error responses in edge cases.
- Priority: Low for demo; higher if used as template for production.

---

*Concerns audit: 2025-02-24*
