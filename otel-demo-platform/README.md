# OpenTelemetry Demo Platform

A portable, interview-ready sandbox: multi-service app with **Kotlin** API + Temporal worker, **one Python agent** (LangChain + Ollama), full OpenTelemetry instrumentation, W3C trace propagation, [temporalio/auto-setup](https://hub.docker.com/r/temporalio/auto-setup), and [Grafana otel-lgtm](https://grafana.com/docs/opentelemetry/docker-lgtm).

## Architecture

- **API (Kotlin, Ktor)** — Entrypoint `POST /chat`; starts Temporal workflow, returns result. OTel + W3C.
- **Worker (Kotlin)** — Temporal workflow + activity; activity calls Agent via HTTP. OTel + W3C.
- **Agent (Python, FastAPI)** — LangChain pipeline + Ollama; `POST /invoke`. OTel Python SDK.
- **Infrastructure** — Temporal (`temporalio/auto-setup`), Grafana otel-lgtm (Collector + Tempo + Grafana).

```
Client → API → Temporal → Worker → Agent (LangChain)
         ↓         ↓         ↓         ↓
              OTel Collector → Tempo → Grafana
```

## Prerequisites

- **Ollama** (local LLM): [Install](https://ollama.ai) and pull a model, e.g. `ollama pull llama3.2`
- **Docker** and **Docker Compose** (for Temporal + Grafana)
- **JDK 17+** and **Gradle** (for Kotlin services)
- **Python 3.11+** (for Agent service)

## Quick Start

1. **Start infrastructure**

   ```bash
   docker compose up -d
   ```

   - Temporal: gRPC on `localhost:7233`
   - Grafana: http://localhost:3000 (admin / admin)
   - OTLP: gRPC `localhost:4317`, HTTP `localhost:4318`

2. **Start services** (in this order, in separate terminals)

   ```bash
   # (1) Agent (Python) — requires Ollama running with a model
   cd agent && pip install -r requirements.txt && python -m agent.main

   # (2) Worker (Kotlin)
   cd worker && ./gradlew run

   # (3) API (Kotlin)
   cd api && ./gradlew run
   ```

3. **Smoke check** — confirm each service is up before sending chat:

   - **API:** `GET http://localhost:8080/health`
   - **Agent:** `GET http://localhost:8000/health` (default `AGENT_PORT`)

   Quick validation: `curl -s http://localhost:8080/health && curl -s http://localhost:8000/health`

4. **Send a request**

   ```bash
   curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"message":"Hello"}'
   ```

   For more examples (e.g. "What is 2 + 2?"), see `test-data/sample_requests.json`.

5. **View traces in Grafana**

   - Open Grafana at http://localhost:3000 (login: admin / admin).
   - Go to **Explore** → select **Tempo**.
   - Find the trace: use the **TraceQL** tab and filter by service name. String values must be quoted, e.g. `resource.service.name="api"` or `resource.service.name="otel-demo-api"`. Alternatively use **Search** or time range.
   - You should see one trace with spans for **API**, **worker**, and **agent**.

## Project Layout

- `api/` — Kotlin Ktor API (Temporal client, OTel)
- `worker/` — Kotlin Temporal worker (workflow, activities, HTTP to Agent)
- `agent/` — Python FastAPI + LangChain + Ollama (OTel)
- `docs/` — ARCHITECTURE.md, USE_CASES.md, INTERVIEW_SCRIPT.md
- `test-data/` — Fixtures and sample requests
- **E2E steps:** See [integration/README.md](integration/README.md) for full run order, health checks, and trace verification.

## Testing

- **Unit tests**
  - **Kotlin**: `./gradlew :api:test :worker:test`
  - **Agent**: `cd agent && .venv/bin/python -m pytest tests/ -v` (create venv and install deps first; see [agent/README.md](agent/README.md)).
- **Integration (E2E)**: Start infra + API + Worker + Agent, then `curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"message":"Hello"}'`. See [docs/TESTING.md](docs/TESTING.md) for full steps and test data location.
- **Prerequisite for local/demo**: Ollama installed and a model pulled (e.g. `ollama pull llama3.2`).

## License

MIT
