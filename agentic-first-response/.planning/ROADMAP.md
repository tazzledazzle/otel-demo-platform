# Roadmap: agentic-first-response

## Overview

Agentic triage system for Invisible Technologies: ReAct-based first-responder loop with RAG over runbooks and past incidents, LLM-driven hypothesis and remediation suggestions, and HITL approval for high-risk actions. Phases align with ingestion → RAG → agent loop → tools → guardrails → observability.

## Milestones

- 📋 **v0.1** — Alert ingestion + stub agent
- 📋 **v0.2** — Knowledge base + RAG retrieval
- 📋 **v0.3** — Full ReAct agent + tools + guardrails
- 📋 **v0.4** — Observability (OTel, metrics, dashboards)

## Phases

### Phase 1: Foundation
**Goal:** Alert ingestion (PagerDuty/Datadog), project setup, and minimal triage agent that accepts an alert payload and returns a stub response. Single-command run and health check.
**Success Criteria:** Incoming alert triggers agent entrypoint; stub response returned; runnable locally or in target env.
**Plans:** 1 plan
- [ ] 01-01-PLAN.md — Webhook ingestion (PagerDuty/Datadog), normalized schema, idempotency, stub agent, health, README

### Phase 2: Knowledge Base & Ingestion
**Goal:** Runbooks (markdown) and past postmortems ingested, chunked, embedded, and stored in vector DB (Chroma/pgvector). Re-index on deploy (e.g. K8s Job).
**Success Criteria:** Runbook and postmortem content searchable by semantic + metadata; re-index repeatable on deploy.
**Plans:** TBD (e.g. 02-01 chunking + embedding pipeline, 02-02 vector store + metadata, 02-03 re-index job).

### Phase 3: RAG & Retrieval
**Goal:** Hybrid retrieval (semantic + metadata filter); retrieved context injected into system prompt with alert payload; chunk size ~500 tokens.
**Success Criteria:** Agent receives relevant runbook and incident chunks for a given alert; context fits within LLM budget.
**Plans:** TBD (e.g. 03-01 retrieval API, 03-02 prompt assembly).

### Phase 4: Triage Agent (ReAct Loop)
**Goal:** ReAct loop (retrieve → reason → act → verify) with max iterations. LLM outputs structured JSON (hypothesis, confidence, suggested_action, risk_level); Pydantic validation. Model routing (Sonnet default, Opus for ambiguous).
**Success Criteria:** Agent produces validated triage output; loop terminates or escalates within iteration limit.
**Plans:** TBD (e.g. 04-01 ReAct loop, 04-02 structured output + validation, 04-03 model routing).

### Phase 5: Tools & Remediation
**Goal:** Function-calling tools: `query_logs`, `get_pod_status`, `get_recent_deploys`, `suggest_remediation`. Read-only by default; write actions behind HITL approval.
**Success Criteria:** Agent can call tools; high-risk actions require approval gate; remediation suggestions actionable.
**Plans:** TBD (e.g. 05-01 tool definitions + read-only impl, 05-02 HITL gate + gated write).

### Phase 6: Guardrails & Safety
**Goal:** Iteration limit, tool allowlist, Pydantic validation on all LLM responses, token budget per session (tracked via OTel).
**Success Criteria:** No runaway loops; only allowlisted tools; cost visible per triage session.
**Plans:** TBD (e.g. 06-01 limits + allowlist, 06-02 cost tracking).

### Phase 7: Observability
**Goal:** Full OTel instrumentation; spans for LLM calls (model, token_count, duration_ms, tool_called); W3C trace propagation; metrics (triage_duration_seconds, hypothesis_accuracy, tool_call_success_rate); Datadog dashboards.
**Success Criteria:** End-to-end trace from alert to remediation; metrics and dashboards available for SRE.
**Plans:** TBD (e.g. 07-01 OTel agent + tools, 07-02 metrics + dashboards).

## Progress

| Phase | Milestone | Plans | Status | Completed |
|-------|-----------|-------|--------|-----------|
| 1. Foundation | v0.1 | 0/1 | Planned | — |
| 2. Knowledge Base | v0.2 | 0 | Not started | — |
| 3. RAG & Retrieval | v0.2 | 0 | Not started | — |
| 4. Triage Agent | v0.3 | 0 | Not started | — |
| 5. Tools & Remediation | v0.3 | 0 | Not started | — |
| 6. Guardrails & Safety | v0.3 | 0 | Not started | — |
| 7. Observability | v0.4 | 0 | Not started | — |

---
*Initialized by GSD new-project workflow*
