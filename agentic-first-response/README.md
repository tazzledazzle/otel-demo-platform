# Agentic First Response

Agentic triage system for reducing mean time to triage when incidents hit a microservices platform (GCP, Temporal, 28+ services). Automates the first-responder loop: **retrieve** runbooks and past incidents via RAG → **reason** with an LLM to form a root-cause hypothesis → **act** by suggesting remediation → **verify** or loop, with human-in-the-loop approval for high-risk actions.

## Problem

On-call engineers had to manually correlate logs across services, read runbooks, and rely on scattered tribal knowledge (e.g. Slack). MTTR was high when Temporal workers stalled, Django services threw 5xx spikes, or downstream activities failed.

## Solution

- **Alert trigger:** PagerDuty/Datadog → triage agent.
- **ReAct agent:** RAG over runbooks + postmortems (Chroma/pgvector), LLM hypothesis and structured output (`hypothesis`, `confidence`, `suggested_action`, `risk_level`), function-calling tools (`query_logs`, `get_pod_status`, `get_recent_deploys`, `suggest_remediation`).
- **Safety:** Read-only tools by default; restart/scale/rollback behind HITL approval; iteration limit and token budget.
- **Observability:** Full OpenTelemetry; trace from alert → agent → tools → remediation; metrics and Datadog dashboards.

## Planning

- [.planning/PROJECT.md](.planning/PROJECT.md) — project identity, value, architecture summary.
- [.planning/REQUIREMENTS.md](.planning/REQUIREMENTS.md) — phase requirements.
- [.planning/ROADMAP.md](.planning/ROADMAP.md) — phases and progress.
- [.planning/STATE.md](.planning/STATE.md) — current state.

Phases: Foundation → Knowledge Base & Ingestion → RAG & Retrieval → Triage Agent (ReAct) → Tools & Remediation → Guardrails & Safety → Observability.

## Status

Foundation phase in progress: alert ingestion FastAPI service with stub triage agent.

## Getting started

- Python 3.10+ recommended.
- Install dependencies from the project root:

```bash
pip install -r requirements.txt
```

## Running the service

From the project root:

```bash
uvicorn app.main:app --reload
```

By default, the app listens on port 8000. You can override the port with the `PORT` environment variable.

## Health check

Once the server is running:

```bash
curl -s http://127.0.0.1:8000/health
```

You should see a JSON response containing `status: "ok"`.

## Webhook endpoint

The main entrypoint for alerts is:

- **POST** `http://127.0.0.1:8000/webhook/alert`
- **Content-Type:** `application/json`

### Example PagerDuty-style payload

```bash
curl -s -X POST http://127.0.0.1:8000/webhook/alert \
  -H "Content-Type: application/json" \
  -d '{
    "event_action": "trigger",
    "dedup_key": "evt-1",
    "payload": {
      "summary": "High CPU on service foo",
      "severity": "critical"
    }
  }'
```

### Example Datadog-style payload

```bash
curl -s -X POST http://127.0.0.1:8000/webhook/alert \
  -H "Content-Type: application/json" \
  -d '{
    "id": "dd-1",
    "title": "High latency on bar",
    "alert_type": "error",
    "severity": "critical",
    "tags": ["service:bar"]
  }'
```

Both calls should return a JSON `StubTriageResponse` with fields:

- `hypothesis`
- `confidence`
- `suggested_action`
- `risk_level`

Sending the same payload again with the same `external_id` (PagerDuty `dedup_key` or Datadog `id`) will return the same stub response without re-processing, satisfying the idempotency requirement.
