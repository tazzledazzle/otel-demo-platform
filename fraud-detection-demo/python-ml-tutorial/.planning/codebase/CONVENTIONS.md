# Coding Conventions

**Analysis Date:** 2025-02-25

## Scope Note

The codebase is a **minimal tutorial scaffold**. No application source code exists yet. Conventions below are inferred from GSD planning artifacts and PROJECT.md constraints; they should be applied when implementing tutorial content.

## Naming Patterns

**Files (planning):**
- Planning documents: UPPERCASE with `.md` (e.g. `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`).
- Config: `config.json` at project root.

**Intended (from PROJECT.md):**
- Tech: Python 3.10+, pandas, scikit-learn; optional PyTorch/TensorFlow.
- Tooling: pip/venv, pytest. Use standard Python and pytest naming when adding code (e.g. `test_*.py`, `*_test.py`).

## Code Style

**Formatting:**
- Not configured in-repo. Use standard Python style (PEP 8) when adding code; consider black or ruff for consistency.

**Linting:**
- Not detected. Add .eslintrc / ruff / pyproject.toml as phases introduce code.

## Import Organization

- Not applicable (no Python modules yet). When adding modules: prefer standard library first, then third-party, then local.

## Error Handling

- Not applicable. In tutorial code, use clear exceptions and messages for learners.

## Logging

- PROJECT.md does not specify; use `logging` or print for tutorial clarity as appropriate.

## Comments

**Planning docs:**
- Footer: `---` and `*Initialized by GSD new-project workflow*` or similar provenance.
- Tables used for Key Decisions (PROJECT.md), Out of Scope (REQUIREMENTS.md), Progress (ROADMAP.md, STATE.md).

**When adding code:**
- Tutorial code should be well-commented for teaching (e.g. inline explanations for ML steps).

## Function Design

- Not applicable until modules exist. Keep tutorial functions small and single-purpose.

## Module Design

- Not applicable. When adding: one logical unit per file; expose clear public API for labs.

## GSD Artifact Conventions

**PROJECT.md:**
- Sections: What This Is, Core Value, Requirements (Validated / Active / Out of Scope), Context, Constraints, Key Decisions (table).

**REQUIREMENTS.md:**
- Sections: Defined date, Core Value, Phase Requirements, Out of Scope (table), Traceability.

**ROADMAP.md:**
- Sections: Overview, Milestones, Phases, Progress (table with Phase, Milestone, Plans, Status, Completed).

**STATE.md:**
- Sections: Project Reference, Current Position (Phase, Plan, Status, Last activity, Progress bar), Performance Metrics, Accumulated Context (Decisions, Pending Todos, Blockers/Concerns), Session Continuity.

**config.json:**
- Top-level keys: `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow`. `workflow` holds boolean flags (e.g. `research`, `plan_check`, `verifier`).

---

*Convention analysis: 2025-02-25*
