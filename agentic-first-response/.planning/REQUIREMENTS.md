# Requirements: agentic-first-response

**Core Value:** Automate first-responder triage (retrieve → reason → act → verify) with RAG, LLM, and HITL safety to reduce MTTR.

## Phase Requirements

### Phase 1: Foundation
- Alert ingestion from PagerDuty/Datadog (webhook or poll).
- Project layout, config, and minimal triage agent entrypoint that receives alert payload and returns a stub response.
- Single-command run and basic health check.

### Phase 2: Knowledge Base & Ingestion
- Runbooks (markdown in repo) chunked and embedded into vector store (Chroma or pgvector).
- Past incident postmortems ingested with structured metadata (service, severity, root cause category).
- Re-index on deploy via K8s Job (or equivalent).

### Phase 3: RAG & Retrieval
- Hybrid retrieval: semantic search (embeddings) + metadata filtering (service name, alert type).
- Retrieved context injected into system prompt with raw alert payload.
- Chunk size tuned (~500 tokens) for context budget.

### Phase 4: Triage Agent (ReAct Loop)
- ReAct loop: retrieve → reason → act → verify (with max iteration limit, e.g. 10).
- LLM integration with structured JSON output: `{ hypothesis, confidence, suggested_action, risk_level }` (Pydantic-validated).
- Model routing: Claude Sonnet for routine triage; escalate to Opus for ambiguous cases when configured.

### Phase 5: Tools & Remediation
- Function-calling tools: `query_logs`, `get_pod_status`, `get_recent_deploys`, `suggest_remediation`.
- Read-only observability tools by default; write actions (restart, scale, rollback) gated behind HITL approval.
- Human-in-the-loop approval gate before executing high-risk actions.

### Phase 6: Guardrails & Safety
- Max iteration limit to prevent runaway loops.
- Tool allowlist; output validation (Pydantic) on every LLM response.
- Cost controls: token budget per triage session, tracked via OpenTelemetry.

### Phase 7: Observability
- Full OpenTelemetry instrumentation through the agent loop.
- Each LLM call as span with attributes: `model`, `token_count`, `duration_ms`, `tool_called`.
- W3C trace context propagated alert → agent → tool execution → remediation.
- Metrics: e.g. `triage_duration_seconds`, `hypothesis_accuracy` (vs postmortem), `tool_call_success_rate`.
- Dashboards in Datadog (or equivalent) showing agent performance alongside SRE metrics.

## Traceability

(To be filled when phases and plans are mapped to requirements.)

---
*Initialized by GSD new-project workflow*
