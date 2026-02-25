# Coding Conventions

**Analysis Date:** 2025-02-24

**Scope:** `otel-demo-platform`

## Naming Patterns

**Files (Kotlin):**
- One main type per file; file name matches type (e.g. `Main.kt`, `ChatRoutes.kt`, `AgentWorkflowImpl.kt`, `RunAgentActivityInterface.kt`).
- Routes in `*Routes.kt`; plugins in `plugins/` with descriptive names.

**Files (Python):**
- Modules: snake_case (`main.py`, `chain.py`, `telemetry.py`).
- Tests: `test_<module>.py` in `tests/`.

**Functions (Kotlin):**
- camelCase for top-level and member functions (`chatRoutes`, `configureRouting`, `initOpenTelemetry`, `agentInvoke`).
- Extension functions for routing: `fun Routing.chatRoutes()`, `fun Application.configureSerialization()`.

**Functions (Python):**
- snake_case (`create_app`, `get_agent_executor`, `setup_telemetry`, `instrument_app`).
- Private executor: `_Executor` (single leading underscore by convention).

**Variables:**
- Kotlin: camelCase (`agentBaseUrl`, `taskQueue`, `otelEndpoint`).
- Python: snake_case (`otlp_endpoint`, `service_name`).

**Types:**
- Kotlin: PascalCase for classes, interfaces, objects (`ChatRequest`, `AgentWorkflowClient`, `TemporalClientFactory`).
- Python: PascalCase for classes and Pydantic models (`InvokeRequest`, `InvokeResponse`, `_Executor`).

## Code Style

**Formatting:**
- Kotlin: No ktlint or formatter config in repo; follow standard Kotlin style (4-space indent, camelCase).
- Python: pyproject.toml has pytest config only; no black/ruff/formatter; use consistent 4-space indent.

**Linting:**
- Kotlin: No ESLint/ktlint config detected.
- Python: `noqa: ANN001` used in `agent/agent/telemetry.py` for `instrument_app(app)` (type annotation omitted).

## Import Organization

**Kotlin:**
- Order: Project imports first (`dev.otel.demo.*`), then third-party (io.ktor, io.temporal, io.opentelemetry).
- No path aliases; full package paths.

**Python:**
- Order: Standard library, then third-party, then local (`from agent.chain import ...`, `from agent.telemetry import ...`).
- No path aliases in agent; tests import via `agent.*`.

## Error Handling

**Patterns:**
- Kotlin: No try/catch in routes or client; let Ktor/Temporal surface errors.
- Python: No custom exception handlers; Pydantic and FastAPI handle validation and responses.
- Use explicit handling when adding new I/O or external calls; document expected failures.

## Logging

**Framework:** No shared logging; worker uses `println` for startup.

**Patterns:**
- Prefer structured logging (e.g. SLF4J/Logback in Kotlin, structlog or logging in Python) if adding; avoid scattering println/print.

## Comments

**When to comment:**
- Stub behavior (e.g. agent `search` tool: "(Stub for demo.)").
- Non-obvious env or integration choices if added.
- Test scope (e.g. ChatRoutesTest: "full E2E requires Temporal + worker (see integration test)").

**JSDoc/TSDoc:** Not used. Kotlin: no KDoc on public APIs in this codebase; add KDoc for public functions when extending.

## Function Design

**Size:** Functions are short (single responsibility); e.g. routes are small, `agentInvoke` is a single expression with runBlocking.

**Parameters:** Few parameters; config via env or constructor (e.g. `RunAgentActivity(agentBaseUrl)`).

**Return values:** Data classes or simple types; no generic Result type.

## Module Design

**Exports:**
- Kotlin: Public types and top-level functions by default; `agentInvoke` and `InvokeResponse` in AgentClient are package-private (no `internal`/`private` on file level).
- Python: `create_app`, `app` in main; `get_agent_executor`, `search`, `get_llm` in chain; `setup_telemetry`, `instrument_app` in telemetry.

**Barrel files:** Not used; import from concrete modules.

---

*Convention analysis: 2025-02-24*
