# Research: Alert Ingestion (PagerDuty, Datadog)

**Domain:** Incident alerting; webhooks; event APIs.  
**Consumed by:** Phase 1 (Foundation).

---

## Summary

PagerDuty and Datadog integrate bidirectionally: Datadog can send events to PagerDuty based on metric thresholds, and incidents can sync back. For an agentic triage system, the triage service can consume alerts either via **webhooks** (Datadog → your endpoint, or PagerDuty → your endpoint) or by **polling/API** (e.g. PagerDuty Events API v2, Datadog API). Webhooks are the natural trigger for “alert fires → start triage agent.”

---

## Key Findings

### Datadog ↔ PagerDuty

- **Datadog → PagerDuty:** When metrics breach thresholds, Datadog sends events to PagerDuty to create or update incidents; severity can drive urgency.
- **Bidirectional sync:** Incident state and escalations can sync back so both systems stay in sync.
- **Enriched payloads:** Datadog can send metric visualizations and service-level data with the event, which is useful context for the triage agent (service name, metric type, time range).

### Triggering the Triage Agent

- **Option A – Webhook from PagerDuty:** Configure a PagerDuty integration or extension to POST to your triage service when an incident is created or updated; payload includes incident ID, title, service, urgency, and custom details.
- **Option B – Webhook from Datadog:** Send alerts to a webhook endpoint (your triage service); payload includes metric, tags, host, and link to dashboard.
- **Option C – Polling:** Triage service periodically calls PagerDuty or Datadog API for new/open incidents; less real-time, more control over rate and filtering.

**Recommendation:** Webhook (A or B) for “alert fires → invoke agent” so triage starts immediately; include in payload service name, alert type, and links (runbook, dashboard) for RAG and tool use.

### API Capabilities

- **PagerDuty Events API v2:** Send trigger, acknowledge, resolve events; used by Datadog and other integrations; your service can also consume webhooks from PagerDuty.
- **Datadog API:** Configure PagerDuty integration programmatically; create/update incidents; query events and metrics for tool use (e.g. `query_logs` backed by Datadog).

### Implications for This Project

- **Phase 1 (Foundation):** Implement an **HTTP webhook endpoint** that accepts PagerDuty and/or Datadog payloads, parses service/alert type/severity, and invokes the triage agent entrypoint with a normalized alert payload.
- **Normalize** payloads to a single internal schema (e.g. `service`, `alert_type`, `severity`, `source`, `external_id`, `links`) so RAG and tools are source-agnostic.
- **Idempotency:** Use incident/event ID to avoid duplicate triage runs for the same alert.
- **Enriched context:** Pass through any dashboard links, metric names, or tags from the webhook for inclusion in the agent prompt or tool parameters.

---

## References (from search)

- PagerDuty Datadog Integration Guide; Datadog PagerDuty integration docs.
- PagerDuty Events API v2 – Send alert events.
- “Monitor with Datadog and take action with PagerDuty.”
