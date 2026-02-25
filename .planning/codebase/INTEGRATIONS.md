# External Integrations

**Analysis Date:** 2025-02-24

**Scope:** `otel-demo-platform`

## APIs & External Services

**Temporal:**
- Workflow engine — gRPC `localhost:7233` (default)
- SDK: `io.temporal:temporal-sdk`, `temporal-kotlin`
- Auth: None (local/dev); connection via `TEMPORAL_ADDRESS`

**Ollama (LLM):**
- Local LLM for agent — HTTP `OLLAMA_BASE_URL` (default `http://localhost:11434`)
- Client: `langchain-ollama` (ChatOllama)
- No API key; local only

**OpenTelemetry Collector:**
- OTLP gRPC — `OTEL_EXPORTER_OTLP_ENDPOINT` (default `http://localhost:4317`)
- All three app services export traces; no metrics/logs from app code

## Data Storage

**Databases:**
- PostgreSQL 15 (Docker) — Used by Temporal only (`temporalio/auto-setup`); credentials in `docker-compose.yml` (temporal/temporal)

**File Storage:**
- Local filesystem only (test-data, fixtures)

**Caching:**
- None in application code

## Authentication & Identity

**Auth Provider:**
- None — No auth on API, worker, or agent; demo/local use

## Monitoring & Observability

**Tracing:**
- OpenTelemetry SDK in API, worker, and agent; W3C Trace Context propagation
- Export: OTLP gRPC to Grafana otel-lgtm (Collector → Tempo → Grafana)

**Error Tracking:**
- None

**Logs:**
- Console (e.g. worker startup message); no structured logging framework

## CI/CD & Deployment

**Hosting:**
- Not defined; services run via `./gradlew run` and `python -m agent.main`

**CI Pipeline:**
- Not detected in `otel-demo-platform` (no `.github/workflows` or other CI config in this repo)

## Environment Configuration

**Required env vars (for full E2E):**
- Optional for apps: `OTEL_EXPORTER_OTLP_ENDPOINT`, `TEMPORAL_ADDRESS`, `TEMPORAL_TASK_QUEUE`, `AGENT_BASE_URL`, `AGENT_PORT`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL` (all have defaults)
- Docker: `POSTGRES_USER`, `POSTGRES_PASSWORD` (and Temporal env) in `docker-compose.yml`

**Secrets location:**
- Not used; no secrets in repo (`.env` not present)

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- API → Temporal (start workflow)
- Worker → Agent `POST /invoke` (HTTP)
- All services → OTLP collector (traces)

---

*Integration audit: 2025-02-24*
