# Research: agentic-first-response

Domain research for the agentic triage system. Produced by GSD project-researcher workflow. Consumed by roadmap refinement and phase planning (e.g. /gsd:plan-phase).

## Index

| Document | Domain | Consumed By |
|----------|--------|-------------|
| [01-ReAct-incident-triage.md](01-ReAct-incident-triage.md) | ReAct pattern for incident triage; single vs multi-agent; when to use/avoid | Phase 4 (Triage Agent), Phase 5 (Tools) |
| [02-RAG-runbooks-postmortems.md](02-RAG-runbooks-postmortems.md) | RAG for runbooks/postmortems; chunking; hybrid retrieval; production failure modes | Phase 2 (Knowledge Base), Phase 3 (RAG) |
| [03-LLM-tools-guardrails-HITL.md](03-LLM-tools-guardrails-HITL.md) | Function calling risks; guardrails; HITL; allowlists; cost controls | Phase 4, 5, 6 (Guardrails & Safety) |
| [04-Observability-OTel-agents.md](04-Observability-OTel-agents.md) | OpenTelemetry for LLM agents; spans; trace propagation; metrics; backends | Phase 7 (Observability) |
| [05-Alert-ingestion-ecosystem.md](05-Alert-ingestion-ecosystem.md) | PagerDuty/Datadog integration; webhooks; event API; triggering triage | Phase 1 (Foundation) |
| [06-Vector-store-reindex.md](06-Vector-store-reindex.md) | Chroma vs pgvector; re-index pipeline; production choices | Phase 2 (Knowledge Base) |

## Summary Themes

- **ReAct:** Fits triage (multi-step, tool coordination, audit trail); use iteration limit and allowlist; multi-agent can improve specificity/correctness if needed later.
- **RAG:** Hybrid retrieval + metadata filtering; ~500-token section-aware chunking; re-index on deploy; plan for retrieval quality monitoring.
- **Safety:** Tool allowlist, Pydantic validation, HITL for write actions; token budget and cost tracking.
- **Observability:** OTel trace per alert; spans for LLM and tools; W3C propagation; metrics (triage_duration_seconds, hypothesis_accuracy, tool_call_success_rate); Datadog (or equivalent) dashboards.
- **Ingestion:** Webhook from PagerDuty or Datadog to start triage; normalize payload; idempotency by incident/event ID.
- **Vector store:** pgvector if Postgres is central; Chroma for dedicated vector store; re-index job on deploy with stable chunk IDs.

---
*Populated by GSD project-researcher workflow*
