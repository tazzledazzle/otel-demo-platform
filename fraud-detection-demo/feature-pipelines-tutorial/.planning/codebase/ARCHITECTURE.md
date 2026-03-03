# Architecture

**Analysis Date:** 2025-02-25

## Pattern Overview

**Overall:** Tutorial scaffold (GSD-initialized). No application architecture yet—only planning artifacts and workflow configuration.

**Key Characteristics:**
- Planning-first: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md define scope and progress.
- Config-driven: `config.json` drives GSD workflow (mode, depth, parallelization, commit_docs, model_profile, workflow flags).
- No runtime or source layers; architecture will emerge when phases are implemented.

## Layers

**Not applicable.** No application code exists. Future layers (e.g. feature computation, store, serving) will be defined in phase plans and implemented under a structure such as `src/` or phase-specific directories.

## Data Flow

**Not applicable.** No data flow until tutorial phases implement feature pipelines (offline/online computation, versioning, backfills).

**State Management:**
- Project state is tracked in `feature-pipelines-tutorial/.planning/STATE.md` (phase, plan, progress, session continuity).
- Roadmap progress table in `feature-pipelines-tutorial/.planning/ROADMAP.md`.

## Key Abstractions

**GSD planning artifacts:**
- **PROJECT.md** — Scope, value, audience, constraints, key decisions.
- **REQUIREMENTS.md** — Phase requirements and traceability (to be filled when phases exist).
- **ROADMAP.md** — Milestones, phases, progress table.
- **STATE.md** — Current position and session continuity.
- **config.json** — Workflow options (yolo/standard depth, parallelization, research/plan_check/verifier).

## Entry Points

**None.** No application entry points. Tutorial content and code will be added per roadmap phases.

## Error Handling

**Not applicable.** No application code.

## Cross-Cutting Concerns

**Logging:** Not applicable.
**Validation:** Not applicable (config.json is the only structured input; schema implied by usage).
**Authentication:** Not applicable.

---

*Architecture analysis: 2025-02-25*
