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

Project initialized; implementation not started. See `.planning/STATE.md` and `.planning/ROADMAP.md` for progress.
