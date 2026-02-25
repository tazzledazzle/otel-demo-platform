# Roadmap: OpenTelemetry Demo Platform

## Overview

Deliver interview-ready demo and docs: first make the full demo runnable with test data and integration steps, then document architecture and script, then provide one implementable live-coding feature so a ~1hr session can explain, demo, and implement one pipeline step.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Runnable demo** - Test data and integration steps allow running full demo (infra → API/worker/agent → chat → trace) ✓ 2026-02-25
- [x] **Phase 2: Interview-ready docs** - Docs cover architecture, use cases, interview script, and one live-coding feature ✓ 2026-02-25
- [x] **Phase 3: Live-coding feature** - One pipeline step or small feature implementable live in-session ✓ 2026-02-25

## Phase Details

### Phase 1: Runnable demo
**Goal**: A full demo can be run from scratch so anyone can start infra, services, send chat, and view one trace.
**Depends on**: Nothing (first phase)
**Requirements**: DOC-02
**Success Criteria** (what must be TRUE):
  1. Reviewer can start all infra (Temporal, Grafana otel-lgtm, etc.) from documented integration steps.
  2. Reviewer can start API, worker, and agent and confirm they are healthy (e.g. health endpoints).
  3. Reviewer can send a chat request and receive a response (test data or example request documented).
  4. Reviewer can view the end-to-end trace in Grafana (one trace spanning API, worker, agent/LLM).
**Plans:** 1 plan

Plans:
- [x] 01-01-PLAN.md — Complete README and integration/README (start order, health checks, test data, Grafana steps)

### Phase 2: Interview-ready docs
**Goal**: Documentation supports a ~1hr interview flow: explain architecture, demo trace, implement one feature.
**Depends on**: Phase 1
**Requirements**: DOC-01
**Success Criteria** (what must be TRUE):
  1. Architecture is documented (services, OTel, Temporal flow, request path).
  2. Use cases and value of the demo are documented (why OTel, why Temporal, trace visibility).
  3. An interview script exists (order of explain / demo / live-coding, rough timing for ~1hr).
  4. One live-coding feature is described (e.g. which pipeline step to add and where it fits).
**Plans:** 2 plans

Plans:
- [x] 02-01-PLAN.md — Complete ARCHITECTURE.md and USE_CASES.md (services, OTel, Temporal, request path; use cases and value)
- [x] 02-02-PLAN.md — Complete INTERVIEW_SCRIPT.md and LIVE_FEATURE.md (~1hr order and timing; one live-coding step and where it fits)

### Phase 3: Live-coding feature
**Goal**: One pipeline step or small feature can be implemented live in-session and demonstrated.
**Depends on**: Phase 2
**Requirements**: FEAT-01
**Success Criteria** (what must be TRUE):
  1. The chosen pipeline step (or small feature) is clearly identified and scoped for in-session implementation.
  2. A candidate can implement it following existing patterns (e.g. new activity or enrichment step).
  3. The change is demonstrable (e.g. visible in trace or in observable behavior).
**Plans:** 1 plan

Plans:
- [x] 03-01-PLAN.md — Add new chain step (prompt | llm | step) in chain.py + test

## Progress

**Execution Order:** 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Runnable demo | 1/1 | Complete | 2026-02-25 |
| 2. Interview-ready docs | 2/2 | Complete | 2026-02-25 |
| 3. Live-coding feature | 1/1 | Complete | 2026-02-25 |
