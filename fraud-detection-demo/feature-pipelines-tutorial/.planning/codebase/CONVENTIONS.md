# Coding Conventions

**Analysis Date:** 2025-02-25

## Scope

The codebase is a tutorial scaffold with no application source. Conventions below are inferred from the existing GSD planning artifacts and the `config.json` schema. Application conventions (language, style, tests) will be established when phases are implemented.

## Naming Patterns

**Planning documents:**
- UPPERCASE with `.md`: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md.
- Codebase analysis: UPPERCASE.md in `.planning/codebase/` (e.g. ARCHITECTURE.md, CONCERNS.md).

**Config:**
- Single config file: `config.json` at tutorial root; keys lowercase (mode, depth, parallelization, commit_docs, model_profile, workflow).

**Research:**
- Placeholder readme: `research/README.md`.

## Code Style

**Formatting:** Not applicable (no app code). Use project-standard formatter when code is added (e.g. Black/Ruff for Python, Prettier for JS/TS).

**Linting:** Not applicable. Add linter config when source is introduced.

## Import Organization

Not applicable.

## GSD Artifact Conventions (Implied)

**PROJECT.md:**
- Sections: What This Is, Core Value, Requirements, Context, Constraints, Key Decisions (table).
- Footer: `*Initialized by GSD new-project workflow*` or similar.

**REQUIREMENTS.md:**
- Sections: Core Value, Phase Requirements, Traceability.
- Footer: Same as above.

**ROADMAP.md:**
- Sections: Overview, Milestones, Phases, Progress (table with Phase | Milestone | Plans | Status | Completed).
- Footer: Same as above.

**STATE.md:**
- Sections: Core value, Current focus, Current Position (Phase | Plan | Status, progress bar), Session Continuity.
- Footer: Same as above.

**Markdown:**
- Use `##` for main sections; tables for decisions and progress.
- Date or “Analysis Date” in analysis docs.

## Error Handling

Not applicable.

## Logging

Not applicable.

## Comments

Not applicable. Planning docs use clear section headers and optional footers.

## Function Design

Not applicable.

## Module Design

Not applicable.

## config.json Schema (Observed)

- `mode`: string (e.g. `"yolo"`).
- `depth`: string (e.g. `"standard"`).
- `parallelization`: boolean.
- `commit_docs`: boolean.
- `model_profile`: string (e.g. `"balanced"`).
- `workflow`: object with `research`, `plan_check`, `verifier` (booleans).

---

*Convention analysis: 2025-02-25*
