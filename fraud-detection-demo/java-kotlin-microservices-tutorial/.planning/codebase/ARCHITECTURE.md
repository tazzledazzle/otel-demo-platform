# Architecture

**Analysis Date:** 2025-02-25

## Pattern Overview

**Overall:** Tutorial scaffold with GSD planning artifacts only. No application runtime or services exist yet.

**Key Characteristics:**
- Planning-only: `.planning/` holds PROJECT, ROADMAP, REQUIREMENTS, STATE, and optional research.
- Single root artifact: `config.json` drives GSD workflow (mode, depth, parallelization, commit_docs, model_profile, workflow flags).
- Intended target: JVM-based microservices (Java or Kotlin) with Spring Boot or Ktor; service boundaries, APIs, resilience, observability, deployment.

## Layers

**Planning layer:**
- Purpose: Define tutorial scope, phases, requirements, and current state for GSD workflows.
- Location: `java-kotlin-microservices-tutorial/.planning/`
- Contains: PROJECT.md, ROADMAP.md, REQUIREMENTS.md, STATE.md, `research/README.md`.
- Depends on: None (markdown and JSON only).
- Used by: GSD orchestrator, phase planning, verification.

**Configuration layer:**
- Purpose: GSD workflow and behavior configuration.
- Location: `java-kotlin-microservices-tutorial/config.json`
- Contains: `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow` (research, plan_check, verifier).
- Depends on: None.
- Used by: GSD tooling.

**Application layer (not yet present):**
- Purpose: Will hold microservice(s), APIs, and tutorial runnable code.
- Location: To be added (e.g. `src/` or per-service modules).
- Intended: Service boundaries, REST/gRPC APIs, resilience (e.g. retries, circuit breakers), observability, deployment config.

## Data Flow

**Current:** No application data flow. Only planning documents and config are read/written by GSD.

**Intended (from PROJECT.md):** Tutorial will teach request flow across services, API contracts, and deployment topology; exact flow TBD when phases are defined.

**State Management:**
- Project state: `.planning/STATE.md` (phase, plan, status, progress).
- No runtime state or persistence yet.

## Key Abstractions

**GSD project:**
- Purpose: Single tutorial “project” with roadmap and traceability.
- Examples: `.planning/PROJECT.md`, `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`
- Pattern: Markdown docs with tables and sections; ROADMAP phases and REQUIREMENTS traceability to be filled after research.

**GSD workflow config:**
- Purpose: Control how GSD runs (yolo/standard depth, parallelization, which workflow steps run).
- Examples: `config.json`
- Pattern: JSON object with `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow`.

## Entry Points

**Planning entry:**
- Location: `java-kotlin-microservices-tutorial/.planning/PROJECT.md`
- Triggers: Human or GSD new-project / map-codebase / plan-phase.
- Responsibilities: Define what the tutorial is, audience, stack, constraints, key decisions.

**Config entry:**
- Location: `java-kotlin-microservices-tutorial/config.json`
- Triggers: GSD workflow invocation.
- Responsibilities: Select mode, depth, parallelization, and which workflow steps (research, plan_check, verifier) run.

**Application entry (future):**
- Not present. Expected: main class per service (Spring Boot or Ktor) once implementation phases exist.

## Error Handling

**Strategy:** Not applicable for current scaffold (no application code). Planning docs are prose; `config.json` is static.

## Cross-Cutting Concerns

**Logging:** Not applicable.
**Validation:** Not applicable (no runtime).
**Authentication:** Not applicable.
**Conventions implied by GSD:** Markdown in `.planning/`; config schema in `config.json`; phase/requirement traceability in ROADMAP and REQUIREMENTS.

---

*Architecture analysis: 2025-02-25*
