# Configuration reference

Single reference for environment variables and defaults used by otel-demo-platform. Linked from [README.md](README.md), [integration/README.md](integration/README.md), and [agent/README.md](agent/README.md).

**Preferred defaults (Phase 1):** API on **8080**, Agent on **8000**. Set `API_PORT` / `AGENT_PORT` only when you need to avoid conflicts. Infra (Temporal, Grafana) use fixed ports below.

---

## API (Kotlin, Ktor)

| Variable                      | Default                                       | Description                                                                                                            |
|-------------------------------|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| `API_PORT`                    | `8080` (or first free in 8080..8089 if unset) | HTTP port. **Preferred:** set `API_PORT=8080` and ensure no other process uses it so docs and one-command start match. |
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
| `AGENT_PORT`                  | `8000` (or next available 8001..8009 if 8000 in use) | HTTP port. **Preferred:** set `AGENT_PORT=8000` and start Agent after API so 8080 is free for API. |
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
