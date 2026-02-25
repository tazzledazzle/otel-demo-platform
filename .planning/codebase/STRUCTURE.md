# Codebase Structure

**Analysis Date:** 2025-02-24

**Scope:** `otel-demo-platform`

## Directory Layout

```
otel-demo-platform/
├── api/                    # Kotlin Ktor API (entrypoint, Temporal client)
│   ├── build.gradle.kts
│   └── src/
│       ├── main/kotlin/dev/otel/demo/api/
│       │   ├── Main.kt
│       │   ├── Telemetry.kt
│       │   ├── TemporalClientFactory.kt
│       │   ├── models/Models.kt
│       │   ├── plugins/Serialization.kt, Routing.kt
│       │   └── routes/ChatRoutes.kt, HealthRoutes.kt
│       └── test/kotlin/dev/otel/demo/api/routes/
│           ├── ChatRoutesTest.kt
│           └── HealthRoutesTest.kt
├── worker/                 # Kotlin Temporal worker (workflow + activity, HTTP to agent)
│   ├── build.gradle.kts
│   └── src/
│       ├── main/kotlin/dev/otel/demo/worker/
│       │   ├── Main.kt
│       │   ├── Telemetry.kt
│       │   ├── AgentWorkflowImpl.kt
│       │   ├── RunAgentActivity.kt, RunAgentActivityInterface.kt
│       │   └── client/AgentClient.kt
│       └── test/kotlin/dev/otel/demo/worker/
│           └── RunAgentActivityTest.kt
├── contracts/              # Shared Temporal workflow interface
│   ├── build.gradle.kts
│   └── src/main/kotlin/dev/otel/demo/contracts/
│       └── AgentWorkflow.kt
├── agent/                  # Python FastAPI + LangChain agent
│   ├── pyproject.toml
│   ├── agent/
│   │   ├── main.py
│   │   ├── chain.py
│   │   └── telemetry.py
│   └── tests/
│       ├── test_main.py
│       └── test_chain.py
├── docs/                   # ARCHITECTURE.md, TESTING.md, USE_CASES.md, etc.
├── test-data/              # sample_requests.json, mock_llm_responses.json
├── integration/            # README (integration notes)
├── docker-compose.yml      # Temporal + Postgres + Grafana otel-lgtm
├── build.gradle.kts
└── settings.gradle.kts     # include api, worker, contracts
```

## Directory Purposes

**api/:**
- Purpose: HTTP API and Temporal client.
- Contains: Kotlin source and tests, Gradle build.
- Key files: `Main.kt`, `routes/ChatRoutes.kt`, `TemporalClientFactory.kt`, `Telemetry.kt`.

**worker/:**
- Purpose: Temporal worker and agent HTTP client.
- Contains: Kotlin source and tests, Gradle build.
- Key files: `Main.kt`, `AgentWorkflowImpl.kt`, `RunAgentActivity.kt`, `client/AgentClient.kt`, `Telemetry.kt`.

**contracts/:**
- Purpose: Shared workflow interface for API and worker.
- Contains: Single Kotlin source set; no tests.
- Key files: `AgentWorkflow.kt`.

**agent/:**
- Purpose: Python agent service (LangChain + Ollama).
- Contains: Package `agent/`, `tests/`, `pyproject.toml`; `.venv` and `.pytest_cache` local.
- Key files: `agent/main.py`, `agent/chain.py`, `agent/telemetry.py`, `tests/test_main.py`, `tests/test_chain.py`.

**docs/:**
- Purpose: Architecture, testing, use cases, interview script.
- Key files: `ARCHITECTURE.md`, `TESTING.md`, `USE_CASES.md`, `INTERVIEW_SCRIPT.md`.

**test-data/:**
- Purpose: Sample payloads and mock data for manual/integration use.

## Key File Locations

**Entry points:**
- `api/src/main/kotlin/dev/otel/demo/api/Main.kt`: API server.
- `worker/src/main/kotlin/dev/otel/demo/worker/Main.kt`: Worker process.
- `agent/agent/main.py`: Agent app and `__main__` uvicorn.

**Configuration:**
- `settings.gradle.kts`, `build.gradle.kts`, `api/build.gradle.kts`, `worker/build.gradle.kts`, `contracts/build.gradle.kts`: Gradle.
- `agent/pyproject.toml`: Python deps and pytest.
- `docker-compose.yml`: Infra only.

**Core logic:**
- Chat flow: `api/.../routes/ChatRoutes.kt`, `api/.../TemporalClientFactory.kt`, `worker/.../AgentWorkflowImpl.kt`, `worker/.../RunAgentActivity.kt`, `worker/.../client/AgentClient.kt`, `agent/agent/main.py`, `agent/agent/chain.py`.
- Contracts: `contracts/.../AgentWorkflow.kt`.

**Testing:**
- Kotlin: `api/src/test/...`, `worker/src/test/...`.
- Python: `agent/tests/test_main.py`, `agent/tests/test_chain.py`.

## Naming Conventions

**Files:**
- Kotlin: PascalCase for types (`Main.kt`, `ChatRoutes.kt`, `AgentWorkflowImpl.kt`); camelCase for multi-word (`RunAgentActivity.kt`).
- Python: snake_case modules (`main.py`, `chain.py`, `telemetry.py`); test files `test_*.py`.

**Directories:**
- Kotlin: package path `dev/otel/demo/{api|worker|contracts}` under `src/main/kotlin` and `src/test/kotlin`.
- Agent: `agent/` package, `tests/` at repo root of agent.

## Where to Add New Code

**New API route:**
- Route: `api/src/main/kotlin/dev/otel/demo/api/routes/` (new or existing `*Routes.kt`).
- Register in `api/.../plugins/Routing.kt`.
- Tests: `api/src/test/kotlin/dev/otel/demo/api/routes/`.

**New workflow/activity:**
- Interface: `contracts/` or extend existing; workflow impl in `worker/.../`, activity impl in `worker/.../` and optionally `worker/.../client/` for HTTP.
- Register in `worker/.../Main.kt`.

**New agent endpoint or chain:**
- App: `agent/agent/main.py` (routes and lifespan).
- Chain/tools: `agent/agent/chain.py` or new module under `agent/agent/`.
- Tests: `agent/tests/` (e.g. `test_main.py`, `test_chain.py`).

**Utilities:**
- Kotlin: Per-module (e.g. under `api/.../` or `worker/.../`); no shared lib.
- Python: Under `agent/agent/` or `agent/tests/` for test helpers.

## Special Directories

**build/ (Gradle):**
- Purpose: Kotlin build output (api, worker, contracts).
- Generated: Yes.
- Committed: No (typically in .gitignore).

**.gradle/, .venv/, .pytest_cache/:**
- Purpose: Gradle cache, Python venv, pytest cache.
- Generated: Yes.
- Committed: No.

---

*Structure analysis: 2025-02-24*
