# OpenTelemetry Demo Platform

## What This Is

A multi-service demo (Kotlin API + Temporal worker, Python LangChain agent) with full OpenTelemetry tracing and W3C propagation, backed by Temporal and Grafana otel-lgtm. It is for showing OTel + Temporal in ~1 hour (explain, demo, implement one feature) — e.g. interviews or internal teaching.

## Core Value

End-to-end observable request flow from HTTP → Temporal workflow → agent, so an interviewer or attendee can see one trace across API, worker, and LLM and add one pipeline step live.

## Requirements

### Validated

<!-- Inferred from existing otel-demo-platform codebase. -->

- ✓ Kotlin API (Ktor) with `GET /health` and `POST /chat` starting a Temporal workflow — current
- ✓ Kotlin worker executing `AgentWorkflow` and `RunAgentActivity` (HTTP to agent) — current
- ✓ Python agent (FastAPI) with LangChain + Ollama, `POST /invoke`, `GET /health` — current
- ✓ Shared Temporal contracts (AgentWorkflow) between API and worker — current
- ✓ OpenTelemetry in API, worker, and agent; OTLP export; W3C trace context propagation — current
- ✓ Infra: temporalio/auto-setup, Grafana otel-lgtm, no app containers — current
- ✓ Interview-ready docs (architecture, use cases, script, live feature), test data, integration steps — v1.0
- ✓ One live-coding feature (summarize step in agent chain) demonstrable in-session — v1.0

### Active

<!-- Next milestone or future goals. -->

- (None — v1.0 delivered interview-ready demo and live-coding feature)

### Out of Scope

- **Datadog** — using Grafana otel-lgtm only.
- **LangChain4j / all-Kotlin agent** — agent is Python (LangChain) called by Kotlin worker.
- **Containerizing app services** — Docker only for infra (Temporal, Postgres, Grafana).
- **Production hardening in v1** — focus is demo and interview; productionization is out of scope unless added later.

## Context

- v1.0 shipped 2026-02-25: runnable demo docs, interview-ready docs (architecture, use cases, script, LIVE_FEATURE), and one implemented pipeline step (summarize in agent chain).
- Built for a 1-hour interview flow: explain architecture, demo trace, implement one feature.
- Codebase map and architecture docs: `.planning/codebase/`, `otel-demo-platform/docs/`. Agent uses local LLM via Ollama (no API keys).

## Constraints

- **Tech stack**: Kotlin (API, worker, contracts), Python (agent), Temporal, OpenTelemetry, Grafana otel-lgtm.
- **Timeline**: Demo and interview script must be completable in ~1 hour.
- **Compatibility**: JVM 17+, Python 3.11+, Docker Compose for infra; Ollama for local LLM.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Single Python agent called by Kotlin worker | Simpler than LangChain4j; reuses LangChain + Ollama. | ✓ Good |
| Grafana otel-lgtm (not Datadog) | Self-hosted, OTLP-native, no vendor lock-in for demo. | ✓ Good |
| No Dockerfiles for app services | Infra only in Docker; run API/worker/agent locally. | — Pending |
| Summarize step as RunnableLambda (Phase 3) | Post-LLM chain step; executor normalizes list content. | ✓ Good |
| Test mock LLM with RunnableLambda for LCEL | MagicMock not invoked as runnable; RunnableLambda works. | ✓ Good |

---
*Last updated: 2026-02-25 after v1.0 milestone*
