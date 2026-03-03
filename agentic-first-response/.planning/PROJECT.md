# agentic-first-response

## What This Is

An agentic triage system that automates the first-responder investigation loop for Invisible Technologies’ platform: 28+ microservices on GCP with Temporal workflows orchestrating human+AI operations. When incidents hit (Temporal worker stalls, Django 5xx spikes, downstream activity failures), the system correlates context, retrieves runbooks and past incidents, and suggests remediation—reducing mean time to triage and replacing scattered tribal knowledge with a structured ReAct-based agent.

## Core Value

Reduce MTTR by automating the initial triage loop: retrieve relevant runbook and incident context, reason about root cause, suggest (and optionally verify) remediation, with human-in-the-loop approval for high-risk actions.

## Problem Statement

On-call engineers previously had to manually correlate logs across services, read runbooks, and figure out root cause. Tribal knowledge lived in Slack threads and was undocumented. Mean time to triage was high.

## Architecture (High Level)

- **Trigger:** Alerts from PagerDuty/Datadog.
- **Agent:** ReAct loop: **Retrieve** (RAG over runbooks + past incidents in Chroma/pgvector) → **Reason** (LLM hypothesis from alert + runbook + logs) → **Act** (suggest remediation: restart pod, scale, rollback, escalate) → **Verify** (check resolution or loop back).
- **Safety:** Human-in-the-loop approval gate for high-risk actions; read-only tools by default; write actions gated.
- **Observability:** Full OpenTelemetry instrumentation; trace context alert → agent → tools → remediation; metrics and Datadog dashboards.

(Detailed architecture—ingestion pipeline, RAG tuning, LLM tools, guardrails, OTel—can be expanded on request.)

## Requirements

(Detailed in REQUIREMENTS.md; traced to ROADMAP phases.)

## Context

- **Platform:** 28+ microservices on GCP; Temporal workflows; human+AI operations.
- **Incident types:** Temporal worker stalls, Django 5xx spikes, downstream activity failures.
- **Stack:** RAG (Chroma/pgvector), LLM (Claude Sonnet/Opus), function calling for tools, OpenTelemetry, Datadog.

## Constraints

- **Safety:** No automatic execution of destructive or high-risk actions without HITL approval.
- **Cost:** Token budget per triage session; tracked via OTel.
- **Scope:** First-responder triage and suggestion; escalation to human when ambiguous or high-risk.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| ReAct pattern for agent | Clear retrieve–reason–act–verify loop; good fit for runbook-driven triage | Structured agent loop with tool use |
| Hybrid RAG (semantic + metadata) | Balance recall (embeddings) with precision (service/alert type) | Runbook + postmortem retrieval |
| HITL gate for write actions | Safety and compliance for production | Restart/scale/rollback require approval |
| OTel end-to-end | Single trace from alert to remediation; SRE visibility | Dashboards alongside existing SRE metrics |

---
*Initialized by GSD new-project workflow*
