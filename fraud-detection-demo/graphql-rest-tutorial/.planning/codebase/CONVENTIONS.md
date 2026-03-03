# Coding Conventions

**Analysis Date:** 2025-02-25

## Scope

No application source code exists. Conventions below are **implied by GSD artifacts** and the tutorial scope (GraphQL and REST). Use them when adding code in future phases.

## Naming Patterns (Implied by GSD)

**Planning and codebase docs:**
- UPPERCASE.md for canonical planning and analysis (PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, ARCHITECTURE.md, etc.).
- `config.json` lowercase at project root.

**Future application code:**
- Follow language and framework norms for the chosen stack (e.g. Apollo/GraphQL-Java for GraphQL; language-specific REST conventions).
- PROJECT.md states: "any language" and "standard tooling"; conventions will be set by the first phase that introduces a stack.

## Code Style

**Formatting:** Not applicable until a language/toolchain is chosen. When added, use project-standard formatters (e.g. Prettier for JS/TS, black/ruff for Python).

**Linting:** Not applicable. Introduce a linter in the first phase that adds source code.

## Import Organization

Not applicable. When code is added, follow the chosen framework’s import style and document here or in phase-specific guidance.

## Error Handling

Not applicable. When implementing APIs, use consistent HTTP status codes for REST and GraphQL error extensions per phase design.

## Logging

Not applicable. When adding servers/clients, use standard logging for the stack (e.g. structured logs for debugging tutorial steps).

## Comments

**Planning docs:** GSD artifacts use a trailing footer, e.g. `*Initialized by GSD new-project workflow*` or `*Architecture analysis: 2025-02-25*`. Preserve or update these when editing.

**Future code:** Prefer clear naming; comment non-obvious tutorial intent (e.g. "Demonstrates N+1 without DataLoader").

## Function Design

Not applicable. When defining resolvers or REST handlers, keep tutorial units small and focused per ROADMAP phase.

## Module Design

Not applicable. When adding code, prefer one logical unit per file (e.g. one resolver module, one route module) to keep the tutorial navigable.

## GSD Conventions (From Artifacts)

- **PROJECT.md:** Include "What This Is", "Core Value", "Requirements", "Context", "Constraints", "Key Decisions" table.
- **REQUIREMENTS.md:** Phase requirements and traceability; fill when phases exist.
- **ROADMAP.md:** Milestones, phases list, progress table (Phase | Milestone | Plans | Status | Completed).
- **STATE.md:** Current phase, plan, status, and progress bar (e.g. 0%).
- **config.json:** Top-level keys observed: mode, depth, parallelization, commit_docs, model_profile, workflow (research, plan_check, verifier).

---

*Convention analysis: 2025-02-25*
