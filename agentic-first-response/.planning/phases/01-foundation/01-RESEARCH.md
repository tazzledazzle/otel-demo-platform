# Phase 1: Foundation — Research

**Researched:** 2026-02-26
**Domain:** Alert ingestion (PagerDuty/Datadog), webhook endpoint, project setup, stub triage agent
**Confidence:** HIGH

## Summary

Phase 1 requires: (1) alert ingestion from PagerDuty or Datadog, (2) project layout and config, (3) minimal triage agent entrypoint that receives an alert payload and returns a stub response, (4) single-command run and health check. Research (see `.planning/research/05-Alert-ingestion-ecosystem.md`) recommends **webhook** as the trigger: PagerDuty or Datadog POST to our endpoint when an alert fires; we normalize to a single internal schema and invoke the agent. **Python + FastAPI** is the recommended stack for the service: aligns with later phases (LLM, Pydantic, RAG), single-command run (`uvicorn` or `fastapi dev`), and simple JSON handling.

## User Constraints (from CONTEXT.md)

### Locked Decisions
- Webhook ingestion (not polling) for "alert fires → start triage."
- Normalized internal alert schema: `service`, `alert_type`, `severity`, `source`, `external_id`, `links` (and optional raw payload for debugging).
- Idempotency: use incident/event ID to avoid duplicate triage runs for the same alert.
- Stub agent: accepts normalized payload, returns fixed stub response (no LLM/RAG in Phase 1).
- Single-command run and a health check endpoint (e.g. GET /health).

### Claude's Discretion
- PagerDuty vs Datadog payload shapes: support at least one in Phase 1; document the other for Phase 1 completion or a follow-up task.
- Project layout: flat or minimal package (e.g. `src/` or `app/`); config via env vars or small config module.

### Deferred Ideas (OUT OF SCOPE)
- RAG, LLM, tools, OpenTelemetry, real remediation — later phases.

---

## Alert Ingestion (from research/05)

### Webhook vs polling
- **Webhook:** PagerDuty or Datadog POST to our URL on incident create/update; real-time; recommended.
- **Polling:** We call their API periodically; more control, less real-time; defer.

### Normalized schema (internal)
| Field         | Type   | Purpose |
|---------------|--------|---------|
| `service`     | str    | Service name (for RAG/tools later) |
| `alert_type`  | str    | e.g. high_cpu, 5xx_spike, workflow_stalled |
| `severity`    | str    | critical, high, medium, low |
| `source`      | str    | `pagerduty` or `datadog` |
| `external_id` | str    | Incident/event ID for idempotency |
| `links`       | list   | URLs (runbook, dashboard, incident) |
| `raw`         | object | Optional; original payload for debugging |

### Idempotency
- Use `external_id` to dedupe: if we already processed this incident/event, return cached or 200 without re-running triage (Phase 1 can log "already seen" and return same stub).
- Store in memory for Phase 1 (e.g. set of recent IDs with TTL); Redis/DB in later phase if needed.

### PagerDuty webhook payload (typical)
- Events API v2 sends different event types; common fields: `routing_key`, `event_action` (trigger, acknowledge, resolve), `dedup_key`, `payload` (summary, severity, source, custom_details).
- Map: `dedup_key` or `payload.custom_details.incident_id` → `external_id`; `payload.summary` / `payload.source` / `payload.severity` → normalized fields; `payload.custom_details` may have service, link.

### Datadog webhook payload (typical)
- Alert payloads include `id`, `title`, `text`, `tags`, `alert_type`, `severity`, `link`, `org`, etc.
- Map: `id` or event ID → `external_id`; `tags` (e.g. `service:foo`) → `service`; `title`/`alert_type` → `alert_type`; `link` → `links`.

---

## Stack: Python + FastAPI

### Rationale
- **Later phases:** LLM (Python SDKs), Pydantic (structured output), RAG (Chroma/LangChain etc.), OTel (Python API) — all Python. One language for the whole project.
- **FastAPI:** Async HTTP; automatic JSON validation and OpenAPI docs; single-command run (`uvicorn app.main:app` or `fastapi dev app/main.py`); minimal boilerplate.
- **Single-command run:** `pip install -r requirements.txt` then `uvicorn app.main:app --reload` (or `fastapi dev`); GET /health and POST /webhook/alert (or /alerts) for ingestion.

### Minimal project layout (Phase 1)

```
/
├── app/
│   ├── __init__.py
│   ├── main.py       # FastAPI app, /health, /webhook/alert (or /alerts)
│   ├── config.py     # env-based config (port, log level)
│   ├── schemas.py    # Pydantic: NormalizedAlert, StubTriageResponse
│   ├── webhook.py    # parse PagerDuty/Datadog → NormalizedAlert
│   └── agent.py      # stub triage: receive NormalizedAlert, return StubTriageResponse
├── requirements.txt
├── README.md
└── .env.example      # optional; PORT, LOG_LEVEL
```

Alternative: flat layout with `main.py`, `schemas.py`, `webhook.py`, `agent.py` at root if preferred; research recommends a single clear entrypoint (e.g. `app.main:app`).

### Health check
- **GET /health** → 200 with body e.g. `{"status": "ok", "service": "triage-agent"}`. No dependency checks in Phase 1 (no DB or LLM).

### Webhook endpoint
- **POST /webhook/alert** (or **POST /alerts**): Accept JSON body. Content-Type application/json. Parse via PagerDuty or Datadog adapter (detect by payload shape or query param `?source=pagerduty|datadog`). Normalize to NormalizedAlert; check idempotency (external_id); call stub agent; return stub response as JSON with 200. On parse error or validation error → 422 or 400 with error body.

### Stub agent
- **Input:** NormalizedAlert (Pydantic).
- **Output:** StubTriageResponse e.g. `{"hypothesis": "Stub: no analysis yet", "confidence": 0, "suggested_action": "escalate_to_human", "risk_level": "unknown"}`. Matches the structured output shape used in later phases (Phase 4).

---

## Anti-patterns

- **Don’t hand-roll HTTP:** Use FastAPI/uvicorn.
- **Don’t process same alert twice:** Use external_id for idempotency (in-memory set with size/TTL limit for Phase 1).
- **Don’t block webhook on long work:** Stub agent is sync and fast; in later phases, consider async or queue so webhook returns 202 and processes in background.
- **Don’t skip validation:** Use Pydantic for request body and response so we catch bad payloads early.

---

## Open Questions

1. **Support both PagerDuty and Datadog in Plan 01?**
   - Recommendation: Implement **one** adapter in 01-01 (e.g. PagerDuty) with a clear adapter interface so adding Datadog in a second task or follow-up is trivial. Document the second in README as "Phase 1.1" or leave for executor discretion.
2. **Route name:** `/webhook/alert` vs `/alerts` vs `/triage/alert`?
   - Recommendation: **POST /webhook/alert** or **POST /alerts**; README documents how to configure PagerDuty/Datadog to send to this URL.

---

## Sources

- `.planning/research/05-Alert-ingestion-ecosystem.md` (primary).
- FastAPI first steps, Pydantic — standard docs.
- PagerDuty Events API v2, Datadog webhooks — official integration docs (referenced in research).

---

## RESEARCH COMPLETE

**Phase:** 1 - Foundation  
**Confidence:** HIGH

### Key findings
- Webhook ingestion (PagerDuty or Datadog) with normalized schema and idempotency by external_id.
- Python + FastAPI: single-command run, /health, POST /webhook/alert (or /alerts), Pydantic schemas, stub agent returning structured stub response.
- One payload adapter in Plan 01 is enough; second source can be added in same plan or follow-up.

### Ready for planning
Planner can create 01-01-PLAN.md with tasks: project setup (requirements, app layout, config), Pydantic schemas (NormalizedAlert, StubTriageResponse), webhook endpoint with one adapter (PagerDuty or Datadog), idempotency (in-memory), stub agent, health check, README with run and test instructions.
