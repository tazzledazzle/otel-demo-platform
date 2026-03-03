# Phase 1: Foundation — Context

**Gathered:** 2026-02-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver alert ingestion (webhook from PagerDuty or Datadog), project setup with config, and a minimal triage agent that accepts a normalized alert payload and returns a stub response. Single-command run and health check. No RAG, LLM, or tools in this phase.

</domain>

<decisions>
## Implementation Decisions

### Ingestion
- Webhook (POST) to receive alerts; support at least one of PagerDuty or Datadog in Phase 1.
- Normalized internal schema: `service`, `alert_type`, `severity`, `source`, `external_id`, `links` (and optional `raw`).
- Idempotency: use `external_id` to avoid duplicate triage for the same incident (in-memory for Phase 1).

### Stack
- Python 3.10+ with FastAPI for the HTTP service (aligns with later phases: LLM, Pydantic, RAG).
- Single-command run: e.g. `uvicorn app.main:app --reload` or `fastapi dev app/main.py`.
- Config via environment variables (e.g. PORT, LOG_LEVEL).

### Stub agent
- Entrypoint receives NormalizedAlert (Pydantic), returns StubTriageResponse with shape: `hypothesis`, `confidence`, `suggested_action`, `risk_level` (stub values only).
- No LLM or external calls; synchronous and fast.

### Claude's Discretion
- Project layout: `app/` package vs flat files; exact route path (`/webhook/alert` vs `/alerts`).
- Which adapter to implement first (PagerDuty vs Datadog) if only one in 01-01.

</decisions>

<specifics>
## Specific Ideas

- GET /health → `{"status": "ok", "service": "triage-agent"}`.
- POST /webhook/alert (or /alerts): JSON body, parse → normalize → idempotency check → stub agent → return JSON response.
- README: prerequisites (Python 3.10+), install, run command, how to test (curl health, curl POST with sample payload).
- Pydantic models for request/response to enable validation and future OpenAPI docs.

</specifics>

<deferred>
## Deferred Ideas

- RAG, vector store, runbooks (Phase 2).
- LLM, ReAct loop, structured output from model (Phase 4).
- Tools (query_logs, get_pod_status, etc.) (Phase 5).
- OpenTelemetry and metrics (Phase 7).
- Redis/DB for idempotency (in-memory sufficient for Phase 1).

</deferred>

---
*Phase: 01-foundation*
*Context gathered: 2026-02-26*
