# Coding Conventions

**Analysis Date:** 2025-02-25

## Naming Patterns

**Files:**
- Planning docs: UPPERCASE.md (PROJECT.md, STATE.md, ROADMAP.md, REQUIREMENTS.md).
- Config: `config.json` (lowercase).
- Research/codebase: README.md or UPPERCASE.md as appropriate.

**Functions / Variables:**
- No application code; conventions to be set when first phase adds code (e.g. snake_case for Python, camelCase for JS/TS if used).

**Types:**
- Not applicable yet.

## Code Style

**Formatting:**
- Markdown: Consistent headings (##, ###), tables for Key Decisions and Progress, bullet lists.
- JSON: config.json is minimal; no formatting tool specified.

**Linting:**
- Not configured (no source code).

## Import Organization

Not applicable (no application code). When code is added, follow language norms and document in this file.

## Error Handling

**Planning docs:**
- Placeholder text and “TBD” used where content is not yet defined; no formal error handling.

**Application:**
- To be defined per phase.

## Logging

**Framework:** Not applicable.

**Patterns:** To be defined when code exists (e.g. structured logging for pipeline steps).

## Comments

**When to comment:**
- GSD artifacts use short section headers and tables; inline comments in code to be defined with first implementation.

**JSDoc/TSDoc:**
- Not applicable.

## Function Design

**Size / Parameters / Return values:** To be defined when codebase and language are chosen.

## Module Design

**Exports:** N/A.

**Barrel files:** N/A.

## Conventions Implied by GSD Artifacts

**PROJECT.md:**
- Use “What This Is,” “Core Value,” “Requirements,” “Context,” “Constraints,” “Key Decisions” (table with Decision | Rationale | Outcome).

**ROADMAP.md:**
- Overview, Milestones (with emoji prefix e.g. 📋), Phases section, Progress table (Phase | Milestone | Plans | Status | Completed).

**REQUIREMENTS.md:**
- “Core Value” recap, “Phase Requirements,” “Traceability.”

**STATE.md:**
- “Core value” recap, “Current focus,” “Current Position” (Phase, Plan, Status), “Progress” (visual bar).

**config.json:**
- Known keys: `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow` (object with booleans e.g. `research`, `plan_check`, `verifier`). Use only these to avoid misinterpretation.

---
*Convention analysis: 2025-02-25*
