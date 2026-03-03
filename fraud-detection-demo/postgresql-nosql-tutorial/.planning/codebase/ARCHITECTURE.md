# Architecture

**Analysis Date:** 2025-02-25

## Pattern Overview

**Overall:** Tutorial scaffold (GSD-initialized). No application architecture exists yet—only planning and workflow configuration.

**Key Characteristics:**
- Planning-first: `.planning/` holds PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, and optional research.
- Single top-level config: `config.json` drives GSD workflow behavior.
- No source code, no entry points, no runtime layers.

## Layers

**Planning layer:**
- Purpose: Project definition, requirements, roadmap, and state tracking for GSD workflows.
- Location: `postgresql-nosql-tutorial/.planning/`
- Contains: Markdown artifacts (PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md) and `research/README.md`.
- Depends on: Nothing (human- and GSD-tool-edited).
- Used by: GSD commands (plan-phase, execute-phase, verifier, roadmapper) and future implementation.

**Configuration layer:**
- Purpose: GSD workflow settings (mode, depth, parallelization, commit behavior, model profile, workflow flags).
- Location: `postgresql-nosql-tutorial/config.json`
- Contains: Single JSON object with `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow`.
- Used by: GSD orchestrator when operating on this directory.

## Data Flow

**Current:** None. No application data flow; only planning documents and config are present.

**Intended (from PROJECT.md):** Tutorial will cover relational vs document/key-value stores, schema design, queries, and hybrid patterns (e.g. Postgres JSONB + dedicated NoSQL). Actual code layout and data flow will be defined when phases are implemented.

**State Management:**
- Project state is tracked in `STATE.md` (phase, plan, status, progress, decisions, todos, blockers).
- No application state or runtime state exists.

## Key Abstractions

**GSD project artifact:**
- Purpose: Canonical project description and constraints.
- Location: `postgresql-nosql-tutorial/.planning/PROJECT.md`
- Defines: Core value, requirements, context (audience, stack), constraints, key decisions table.

**GSD config schema:**
- Purpose: Workflow behavior for this project.
- Location: `postgresql-nosql-tutorial/config.json`
- Schema (observed): `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow` (with sub-keys: `research`, `plan_check`, `verifier`).

## Entry Points

**None.** No runnable application. Entry points will be defined when tutorial phases (e.g. labs, scripts, sample apps) are added.

## Error Handling

**Strategy:** Not applicable—no application code.

## Cross-Cutting Concerns

**Logging:** Not applicable.
**Validation:** Config is JSON; no schema validation detected in-repo.
**Authentication:** Not applicable.

---

*Architecture analysis: 2025-02-25*
