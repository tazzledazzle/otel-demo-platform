# Coding Conventions

**Analysis Date:** 2025-02-25

## Naming Patterns

**Files:**
- Planning: UPPERCASE.md (PROJECT.md, ROADMAP.md, STATE.md, REQUIREMENTS.md).
- Config: `config.json` (lowercase).
- Research: README.md in `.planning/research/`.

**Functions / variables / types:** Not applicable; no application source yet. When adding code, use the client and language conventions (e.g. redis-py: snake_case; Jedis: Java conventions).

## Code Style

**Formatting:** Not established (no linters or formatters in repo). When introducing code, add project-appropriate formatters (e.g. Black/ruff for Python, Prettier for JS).

**Linting:** Not detected. Add per-language linter when source is added.

## Import Organization

Not applicable. When adding code: use standard library first, then third-party (e.g. Redis client), then local modules.

## Error Handling

Not applicable. When adding Redis code: handle connection failures and Redis errors explicitly; avoid silent failures in tutorial examples.

## Logging

Not established. For tutorial code, prefer clear print/output or minimal logging so readers see what’s happening.

## Comments

**When to comment:** In tutorial code, comment to explain Redis concepts and non-obvious steps, not to restate the API.

**JSDoc/TSDoc:** Not applicable unless the stack becomes TypeScript/JavaScript.

## Function Design

Not established. Keep tutorial examples small and single-purpose so each phase stays “completable in a focused session” (PROJECT.md).

## Module Design

Not established. When adding code, prefer one concept per file or per phase so structure matches ROADMAP phases.

## GSD Conventions (Implied)

- **PROJECT.md:** Single source of truth for scope, audience, stack, constraints.
- **ROADMAP.md:** Phases and progress table; keep progress table updated.
- **STATE.md:** Reflect current phase, plan, and progress.
- **REQUIREMENTS.md:** Phase requirements and traceability to roadmap.
- **config.json:** Do not commit secrets; config holds workflow knobs only.

---

*Convention analysis: 2025-02-25*
