# Coding Conventions

**Analysis Date:** 2025-02-25

## Naming Patterns

**Files:**
- Planning docs: UPPERCASE.md (PROJECT.md, STATE.md, ROADMAP.md, REQUIREMENTS.md).
- Config: `config.json` at project root.
- Code: Not present; follow language norms when added (e.g. snake_case for Python modules, PascalCase for classes).

**Functions / variables:**
- Not applicable until application or tutorial code exists. Prefer language-standard (e.g. Python: snake_case, JS: camelCase).

**Types:**
- Not applicable. Use language and framework conventions when code is introduced.

## Code Style

**Formatting:**
- No formatter config in repo. When adding code, add project-appropriate config (e.g. Black/ruff for Python, Prettier/ESLint for JS).

**Linting:**
- Not configured. Introduce linters with first code phase.

## Import Organization

**Order:** Not applicable.

**Path aliases:** Not applicable.

## Error Handling

**Patterns:** To be established with first implementation phase.

## Logging

**Framework:** Not applicable. Use standard or observability patterns when backend/tooling is added.

## Comments

**When to comment:**
- PROJECT.md and planning docs use short section headers and tables (Key Decisions). Keep planning docs clear and scannable.

**JSDoc/TSDoc:** Not applicable.

## Function Design

**Size / parameters / return values:** To be defined when code is added; follow language and tutorial clarity goals.

## Module Design

**Exports:** Not applicable.

**Barrel files:** Not applicable.

## GSD Artifact Conventions (Implied)

**PROJECT.md:**
- Sections: What This Is, Core Value, Requirements, Context, Constraints, Key Decisions.
- Requirements and Key Decisions may reference REQUIREMENTS.md and ROADMAP.md.
- Footer: `*Initialized by GSD new-project workflow*` or similar.

**STATE.md:**
- Core value one-liner, current focus, Phase | Plan | Status, progress bar (e.g. 0%), footer.

**ROADMAP.md:**
- Title "Roadmap: <project-name>", Overview, Milestones (e.g. v1.0), Phases table (Phase, Milestone, Plans, Status, Completed), Progress table, footer.

**REQUIREMENTS.md:**
- Title "Requirements: <project-name>", Core Value, Phase Requirements, Traceability, footer.

**config.json:**
- Top-level keys: `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow`.
- `workflow` object: boolean flags (e.g. `research`, `plan_check`, `verifier`).

Use these patterns when creating or updating GSD artifacts so orchestrators and phase planners parse them correctly.

---

*Convention analysis: 2025-02-25*
