# Coding Conventions

**Analysis Date:** 2025-02-25

## Naming Patterns

**Files (planning):**
- GSD planning docs: UPPERCASE with .md (PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md).
- Config: `config.json` (lowercase).

**Directories:**
- `.planning/` for all GSD artifacts; `research/` under `.planning/` for optional research.

No application source code exists; conventions for code (functions, variables, types) will be established when phases add implementation.

## Code Style

**Formatting:** Not applicable—no source code. When adding code, follow the language and tooling chosen per phase (e.g. project-specific formatters for SQL, application language).

**Linting:** Not detected. Add linters when tutorial code is introduced.

## Import Organization

Not applicable. No application modules.

## Error Handling

Not applicable. Document patterns when first phase introduces application or script code.

## Logging

Not applicable.

## Comments

**Planning docs:** PROJECT.md uses a Key Decisions table (Decision | Rationale | Outcome). REQUIREMENTS.md and ROADMAP.md use section headers and placeholder text; traceability and progress tables to be filled. Footer line `*Initialized by GSD new-project workflow*` is standard for GSD-initialized artifacts.

## Function Design

Not applicable until implementation exists.

## Module Design

Not applicable. GSD artifact layout: one file per concern (PROJECT, REQUIREMENTS, ROADMAP, STATE); optional `research/README.md`.

## GSD Artifact Conventions (Implied)

**PROJECT.md:**
- Sections: What This Is, Core Value, Requirements, Context, Constraints, Key Decisions (markdown table).
- Context includes Audience and Stack.
- Key Decisions table: Decision | Rationale | Outcome.

**ROADMAP.md:**
- Sections: Overview, Milestones, Phases, Progress (table: Phase | Milestone | Plans | Status | Completed).

**REQUIREMENTS.md:**
- Core Value statement; Phase Requirements; Traceability.

**STATE.md:**
- Core value; Current focus; Current Position (Phase, Plan, Status); Progress bar.

**config.json:**
- Top-level keys: `mode`, `depth`, `parallelization`, `commit_docs`, `model_profile`, `workflow`.
- `workflow` object: `research`, `plan_check`, `verifier` (booleans).

---

*Convention analysis: 2025-02-25*
