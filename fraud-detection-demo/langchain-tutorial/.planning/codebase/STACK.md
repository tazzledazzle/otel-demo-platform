# Technology Stack

**Analysis Date:** 2025-02-25

## Languages

**Primary:**
- Not chosen yet. PROJECT.md suggests LangChain (Python or JS); decision deferred until phases are defined.

**Secondary:**
- Not applicable.

## Runtime

**Environment:**
- None (planning scaffold only).

**Package manager:**
- None. Add `requirements.txt` / `pyproject.toml` or `package.json` with first code phase.
- Lockfile: Not present.

## Frameworks

**Core:**
- LangChain (Python or JS)—intended per PROJECT.md; version and variant TBD.

**Testing:**
- Not selected.

**Build/Dev:**
- None. GSD workflow uses `config.json`; no build tooling in repo.

## Key Dependencies

**Critical:**
- LangChain—to be added when first phase introduces code.
- LLM provider (e.g. OpenAI)—referenced in PROJECT.md; add with first runnable example.

**Infrastructure:**
- None.

## Configuration

**Environment:**
- Not configured. Future: use env vars for API keys and provider config; do not commit secrets.

**Build:**
- No build config files.

## Platform Requirements

**Development:**
- GSD tooling to read `.planning/` and `config.json`. For future code: Python 3.x or Node.js per stack choice.

**Production:**
- Tutorial/deployment target not defined (e.g. notebooks, static site, or local run only).

---

*Stack analysis: 2025-02-25*
