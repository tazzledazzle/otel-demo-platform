# Testing Patterns

**Analysis Date:** 2025-02-24

**Scope:** `otel-demo-platform`

## Test Framework

**Kotlin:**
- Runner: JUnit 5 (JUnit Platform).
- Config: `useJUnitPlatform()` in `api/build.gradle.kts` and `worker/build.gradle.kts`; no separate JUnit config file.
- Assertions: `org.junit.jupiter.api.Assertions` (e.g. `assertEquals`, `assertTrue`); kotlin-test available via kotlin-test-junit5.

**Python:**
- Runner: pytest ≥8.0.
- Config: `agent/pyproject.toml` — `[tool.pytest.ini_options]` with `asyncio_mode = "auto"`, `testpaths = ["tests"]`.
- Assertions: Plain `assert`.

**Run commands:**
```bash
# Kotlin (from repo root)
./gradlew :api:test :worker:test

# Python (from agent/)
cd agent && .venv/bin/python -m pytest tests/ -v
# or: pip install -e ".[dev]" then pytest
```

## Test File Organization

**Location:**
- Kotlin: Tests next to source tree under `src/test/kotlin/` with same package path as main.
- Python: Top-level `tests/` under `agent/`; no co-located test files.

**Naming:**
- Kotlin: `*Test.kt` (e.g. `ChatRoutesTest.kt`, `HealthRoutesTest.kt`, `RunAgentActivityTest.kt`).
- Python: `test_*.py` (e.g. `test_main.py`, `test_chain.py`).

**Structure:**
```
api/src/test/kotlin/dev/otel/demo/api/routes/
  ChatRoutesTest.kt, HealthRoutesTest.kt
worker/src/test/kotlin/dev/otel/demo/worker/
  RunAgentActivityTest.kt
agent/tests/
  test_main.py, test_chain.py
```

## Test Structure

**Kotlin (API):**
- Use `testApplication { }` (Ktor Test Engine); inside, `application { }` to install plugins and routing, then `client.get(...)` or similar.
- Example (`HealthRoutesTest.kt`): install ContentNegotiation + routing with healthRoutes only; GET /health; assert body text "OK".
- Example (`ChatRoutesTest.kt`): install ContentNegotiation + routing with health + chat routes; no HTTP call to /chat (Temporal not mocked); comment notes full E2E is integration.

**Kotlin (Worker):**
- Plain JUnit test: instantiate `RunAgentActivity("http://localhost:8000")`, assert it implements `RunAgentActivityInterface`. No Temporal or HTTP mocked.

**Python:**
- Fixture `client`: create app with `create_app(agent=mock_agent)`, set `app.state.agent` to mock, return TestClient(app). Tests use `client.get("/health")`, `client.post("/invoke", json=...)`.
- Chain tests: patch `ChatOllama` or `get_llm` to avoid real Ollama; assert executor exists and invoke returns dict with "output".

**Patterns:**
- Setup: Kotlin testApplication block; Python fixture with mock agent.
- No shared teardown beyond test scope.
- Assertions: Kotlin `assertEquals`, `assertTrue`; Python `assert r.status_code == 200`, `assert "reply" in data`.

## Mocking

**Kotlin:**
- No mocking framework (no MockK/Mockito in deps). Chat route test does not mock Temporal; worker test only checks interface implementation.

**Python:**
- `unittest.mock`: `MagicMock`, `patch` (e.g. `patch("agent.chain.ChatOllama")`, `patch("agent.chain.get_llm")`).
- Mock agent in app: `mock_agent.invoke.return_value = {"output": "Echo: hello"}`.
- Mock LLM in chain: `mock_llm.invoke.return_value = type("R", (), {"content": "Hello back"})()`.

**What to mock:**
- Agent: External LLM (Ollama) and agent executor in app tests.
- Chain: ChatOllama or get_llm to avoid network.

**What NOT to mock:**
- FastAPI app, routing, Pydantic models; Ktor routing and serialization in tests that exercise them.

## Fixtures and Factories

**Test data:**
- `otel-demo-platform/test-data/sample_requests.json` — sample POST /chat bodies.
- `otel-demo-platform/test-data/mock_llm_responses.json` — fixtures; tests use in-memory mocks rather than loading these in unit tests.
- Python: No dedicated fixture files; mocks built in tests/fixtures.

**Location:**
- Repo-level: `test-data/`.
- Agent: `agent/tests/`; docs mention `agent/tests/fixtures/` for mock LLM responses.

## Coverage

**Requirements:** None enforced; no coverage config in Gradle or pytest.

**View coverage:**
- Kotlin: Not configured (could add JaCoCo to Gradle).
- Python: `pytest --cov=agent` if pytest-cov is added.

## Test Types

**Unit tests:**
- API: Route registration and health route with test server; chat route only install check.
- Worker: Activity type check only.
- Agent: Health and /invoke with mock agent; chain and executor with mock LLM.

**Integration tests:**
- No automated integration suite in repo. `docs/TESTING.md` describes manual E2E: start infra (docker compose), API, worker, agent, then curl POST /chat. `integration/` has README.

**E2E:** Manual only (see docs/TESTING.md).

## Common Patterns

**Async (Python):**
- pytest-asyncio `asyncio_mode = "auto"`; TestClient is sync; no async tests in current tests.

**Error testing:**
- Not present (no tests for 4xx/5xx or invalid payloads).

---

*Testing analysis: 2025-02-24*
