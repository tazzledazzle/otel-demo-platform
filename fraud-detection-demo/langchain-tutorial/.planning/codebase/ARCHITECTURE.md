# Architecture

**Analysis Date:** 2025-02-25

## Pattern Overview

**Overall:** GSD planning scaffold (no application runtime yet).

**Key Characteristics:**
- Planning-only layout: `.planning/` and `config.json` define project intent and workflow.
- No application layers, entry points, or data flow—tutorial content and code to be added per ROADMAP phases.
- Single “layer” today: GSD artifact layer consumed by `/gsd:plan-phase`, `/gsd:execute-phase`, and related commands.

## Layers

**GSD planning layer:**
- Purpose: Capture project definition, state, roadmap, requirements, and optional research.
- Location: `langchain-tutorial/.planning/`
- Contains: PROJECT.md, STATE.md, ROADMAP.md, REQUIREMENTS.md, research/README.md.
- Depends on: Nothing in-repo; GSD workflow tooling reads these files.
- Used by: Orchestrators and phase planners; future implementation will follow phases defined here.

## Data Flow

**Current (planning only):**
1. PROJECT.md defines scope (LangChain tutorial, audience, stack hints).
2. ROADMAP.md and REQUIREMENTS.md are placeholders for phases and traceability.
3. STATE.md tracks phase/plan/status; progress 0%.
4. config.json drives GSD workflow behavior (mode, depth, parallelization, research, plan_check, verifier).

**State Management:**
- No application state. Planning state lives in STATE.md and ROADMAP progress table.

## Key Abstractions

**Project definition:**
- Purpose: Single source of “what this is” and constraints.
- Example: `langchain-tutorial/.planning/PROJECT.md`
- Pattern: Sections for What This Is, Core Value, Requirements, Context, Constraints, Key Decisions.

**Workflow config:**
- Purpose: GSD behavior (yolo/standard depth, parallelization, research, verification).
- Example: `langchain-tutorial/config.json`
- Pattern: JSON with `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow` flags.

## Entry Points

**Planning entry:**
- Location: `langchain-tutorial/.planning/PROJECT.md`
- Triggers: GSD new-project workflow (already run); phase planning will use PROJECT + ROADMAP + REQUIREMENTS.
- Responsibilities: Define tutorial scope and value; no executable entry points yet.

## Error Handling

**Strategy:** Not applicable—no application code.

## Cross-Cutting Concerns

**Logging:** Not applicable.
**Validation:** config.json drives workflow; no schema enforced in repo.
**Authentication:** Not applicable.

---

*Architecture analysis: 2025-02-25*
