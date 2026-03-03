# Configuration reference

Single reference for environment variables and defaults used by otel-demo-platform. Linked from [README.md](README.md), [integration/README.md](integration/README.md), and [agent/README.md](agent/README.md).

**Preferred defaults (Phase 1):** API on **8080**, Agent on **8000**. Set `API_PORT` / `AGENT_PORT` only when you need to avoid conflicts. Infra (Temporal, Grafana) use fixed ports below.

---

## API (Kotlin, Ktor)

| Variable                      | Default                                       | Description                                                                                                            |
|-------------------------------|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| `API_PORT`                    | `8080` when unset                             | HTTP port. When unset, API uses 8080 only; if 8080 is in use the process fails with a clear message. Set `API_PORT` to override. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317`                       | OTLP gRPC endpoint for traces.                                                                                         |

---

## Worker (Kotlin, Temporal)

| Variable                      | Default                 | Description                                                     |
|-------------------------------|-------------------------|-----------------------------------------------------------------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` | OTLP gRPC endpoint for traces.                                  |
| `TEMPORAL_ADDRESS`            | `localhost:7233`        | Temporal gRPC address.                                          |
| `TEMPORAL_TASK_QUEUE`         | `agent-task-queue`      | Task queue for workflows.                                       |
| `AGENT_BASE_URL`              | `http://localhost:8000` | Base URL of the Agent service (`POST {AGENT_BASE_URL}/invoke`). |

---

## Agent (Python, FastAPI)

| Variable                      | Default                                              | Description                                                                                        |
|-------------------------------|------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| `AGENT_PORT`                  | `8000` when unset                             | HTTP port. When unset, Agent uses 8000 only; if 8000 is in use the process exits with a clear message. Set `AGENT_PORT` to override. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317`                              | OTLP gRPC endpoint for traces.                                                                     |
| `OLLAMA_BASE_URL`             | `http://localhost:11434`                             | Ollama API URL.                                                                                    |
| `OLLAMA_MODEL`                | `llama3.2`                                           | Model name (e.g. after `ollama pull llama3.2`).                                                    |

---

## Infrastructure (Docker Compose)

| Service             | Port(s)                                             | Notes                        |
|---------------------|-----------------------------------------------------|------------------------------|
| Temporal            | `7233` (gRPC)                                       | `temporalio/auto-setup`.     |
| Grafana (otel-lgtm) | `3000` (UI), `4317` (OTLP gRPC), `4318` (OTLP HTTP) | Grafana + Tempo + collector. |
| Postgres            | `5432`                                              | Used by Temporal.            |

---

## Run order (recommended)

1. Start infra: `docker compose up -d`
2. Start **Agent** (needs Ollama + model): `cd agent && python -m agent.main`
3. Start **Worker**: `cd worker && ./gradlew run`
4. Start **API**: `cd api && ./gradlew run`

Or use the one-command target (Makefile / scripts) that starts infra + all three apps with preferred defaults (Phase 1).
