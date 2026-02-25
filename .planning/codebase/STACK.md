# Technology Stack

**Analysis Date:** 2025-02-24

**Scope:** `otel-demo-platform` (Kotlin API/worker, Python agent, Docker infra)

## Languages

**Primary:**
- Kotlin 1.9.24 — API, worker, and shared contracts; JVM 17
- Python ≥3.11 — Agent service (LangChain + Ollama); pyproject specifies 3.11+

**Secondary:**
- Groovy/Kotlin DSL — Build: `build.gradle.kts`, `settings.gradle.kts`

## Runtime

**Environment:**
- JVM 17 (Kotlin modules)
- Python 3.11+ (agent; optional dev uses 3.14 in venv)

**Package Manager:**
- Gradle (Kotlin) — no wrapper version pinned in repo; uses Gradle 8.x from wrapper
- pip/hatch (Python) — `agent/pyproject.toml`; build backend hatchling, install via `pip install -e ".[dev]"`

**Lockfile:**
- Kotlin: Gradle dependency lockfiles not present
- Python: Lockfile not committed (deps in `pyproject.toml` only)

## Frameworks

**Core:**
- Ktor 2.3.9 — API (Netty server, content negotiation, Jackson); worker uses Ktor client (CIO, Jackson)
- Temporal SDK 1.24.0 — Workflow orchestration (API as client, worker as worker)
- FastAPI (≥0.115.0) + Uvicorn — Agent HTTP API
- LangChain (≥0.3.0), langchain-ollama (≥0.2.0), langchain-core — Agent LLM pipeline

**Testing:**
- JUnit 5 (kotlin-test-junit5, junit-platform-launcher) — Kotlin unit tests
- Ktor Test Engine (testApplication, TestHost) — API route tests
- temporal-testing 1.24.0 — Worker tests (available; RunAgentActivityTest is shallow)
- pytest (≥8.0), pytest-asyncio (≥0.24) — Agent tests
- FastAPI TestClient, unittest.mock — Agent app and chain tests

**Build/Dev:**
- Gradle (base + kotlin jvm + application) — Kotlin build
- hatchling — Agent wheel build

## Key Dependencies

**Critical:**
- io.temporal:temporal-sdk / temporal-kotlin 1.24.0 — Workflow/activity contract and execution
- io.opentelemetry:* 1.35.0 (API/SDK/exporter-otlp, instrumentation-annotations) — Tracing in API and worker
- opentelemetry-api/sdk/exporter-otlp-proto-grpc, opentelemetry-instrumentation-fastapi (Python) — Agent tracing
- langchain-ollama — Local LLM (Ollama) for agent

**Infrastructure:**
- Jackson (ktor-serialization-jackson, jackson-module-kotlin) — JSON in Kotlin
- OpenTelemetry OTLP gRPC exporters — All services export to collector

## Configuration

**Environment:**
- API: `OTEL_EXPORTER_OTLP_ENDPOINT` (default `http://localhost:4317`), port 8080 hardcoded in `api/src/main/kotlin/dev/otel/demo/api/Main.kt`
- Worker: `OTEL_EXPORTER_OTLP_ENDPOINT`, `TEMPORAL_ADDRESS` (default `localhost:7233`), `TEMPORAL_TASK_QUEUE` (default `agent-task-queue`), `AGENT_BASE_URL` (default `http://localhost:8000`)
- Agent: `OTEL_EXPORTER_OTLP_ENDPOINT`, `AGENT_PORT` (default 8000), `OLLAMA_BASE_URL` (default `http://localhost:11434`), `OLLAMA_MODEL` (default `llama3.2`)
- No `.env` in repo; all via process environment

**Build:**
- Root: `otel-demo-platform/build.gradle.kts`, `settings.gradle.kts` (includes api, worker, contracts)
- Per-module: `api/build.gradle.kts`, `worker/build.gradle.kts`, `contracts/build.gradle.kts`
- Agent: `agent/pyproject.toml` (deps, pytest asyncio_mode, testpaths)

## Platform Requirements

**Development:**
- JDK 17+, Gradle (or wrapper)
- Python 3.11+, venv, Ollama (local LLM) with model (e.g. llama3.2)
- Docker and Docker Compose for Temporal + Grafana otel-lgtm

**Production:**
- Same runtimes; deployment target not defined (no Dockerfiles for app services; docker-compose is infra only)

---

*Stack analysis: 2025-02-24*
