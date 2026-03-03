# Coding Conventions

**Analysis Date:** 2025-02-25

## Naming Patterns

**Files:**
- Planning documents: UPPERCASE with `.md` (e.g. `PROJECT.md`, `ROADMAP.md`, `REQUIREMENTS.md`, `STATE.md`).
- Config: `config.json` at project root.
- Research: `README.md` in `.planning/research/`.

**Functions / Variables / Types:**
- Not applicable; no application source code yet. When adding Spark code, follow language norms (e.g. Python snake_case, Scala camelCase for methods).

## Code Style

**Formatting:**
- Not configured. No formatter or linter config in repo.

**Linting:**
- Not detected.

## Import Organization

- Not applicable (no source files).

## Error Handling

- Not defined. When adding Spark pipelines, use try/except or equivalent and clear error messages for tutorial clarity.

## Logging

- Not defined. For tutorials, print or logging should be consistent and instructive.

## Comments

**When to Comment:**
- GSD planning docs use short section headers and tables (e.g. Key Decisions in PROJECT.md). No formal comment policy for code yet.

**JSDoc/TSDoc:**
- Not applicable (no TypeScript/JavaScript).

## Function Design

- Not applicable until code is added.

## Module Design

- Not applicable.

## GSD Artifact Conventions (Implied)

**PROJECT.md:**
- Sections: What This Is, Core Value, Requirements, Context (Audience, Stack, Constraints), Key Decisions table, footer with workflow attribution.

**ROADMAP.md:**
- Overview, Milestones, Phases, Progress table (Phase | Milestone | Plans | Status | Completed), footer.

**REQUIREMENTS.md:**
- Core Value, Phase Requirements, Traceability, footer.

**STATE.md:**
- Core value, Current focus, Current Position (Phase, Plan, Status), Progress bar, footer.

**config.json:**
- Top-level keys: `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow` (with sub-flags e.g. `research`, `plan_check`, `verifier`).

---

*Convention analysis: 2025-02-25*
