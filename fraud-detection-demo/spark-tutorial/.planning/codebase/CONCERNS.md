# Codebase Concerns

**Analysis Date:** 2025-02-25

## Tech Debt

**N/A for code:** No application code exists, so no code-level tech debt. Planning artifacts are placeholders.

**Placeholder content:**
- Issue: ROADMAP phases, REQUIREMENTS phase requirements, and PROJECT Key Decisions are TBD or empty.
- Files: `spark-tutorial/.planning/ROADMAP.md`, `spark-tutorial/.planning/REQUIREMENTS.md`, `spark-tutorial/.planning/PROJECT.md`
- Impact: GSD plan-phase and execute-phase workflows lack concrete phases and requirements to implement.
- Fix approach: Run roadmap/requirement derivation (e.g. gsd-roadmapper, research) and fill ROADMAP.md and REQUIREMENTS.md; then add Key Decisions to PROJECT.md as choices are made.

## Known Bugs

- None (no runnable application).

## Security Considerations

**Secrets:**
- No application code or deployment yet. When adding cluster or cloud config, keep secrets out of repo; use env vars or a secrets manager and do not commit `.env` or credential files.

**config.json:**
- File: `spark-tutorial/config.json`
- Risk: Low; contains workflow flags only, no secrets. Do not add API keys or credentials here.

## Performance Bottlenecks

- Not applicable (no pipelines or runtime).

## Fragile Areas

**Planning only:**
- Files: `spark-tutorial/.planning/STATE.md`, `spark-tutorial/.planning/ROADMAP.md`
- Why fragile: STATE and progress table must be updated when phases/plans change; manual edits can desync.
- Safe modification: Prefer GSD workflow updates for STATE and ROADMAP when available; otherwise update STATE and ROADMAP in one logical change.

## Scaling Limits

- Not applicable. Tutorial scope is single-user, local or classroom use unless roadmap explicitly adds multi-tenant or production deployment.

## Dependencies at Risk

- No dependency manifest (no `requirements.txt`, `build.sbt`, `pom.xml`, etc.). When stack is added, pin versions and document in STACK.md.

## Missing Critical Features

**Phases and requirements:**
- Problem: No defined phases or phase requirements.
- Blocks: Execution of tutorial content and GSD phase planning.
- Fix: Define phases in ROADMAP.md and requirements in REQUIREMENTS.md (and optionally research in `.planning/research/`).

**Application structure:**
- Problem: No `src/`, `notebooks/`, `examples/`, or lesson layout.
- Blocks: Where to add code and how to run lessons.
- Fix: Decide structure in roadmap (e.g. one dir per phase or one `notebooks/` + `scripts/`) and document in STRUCTURE.md.

## Test Coverage Gaps

**Entire codebase:**
- What's not tested: All future tutorial code and examples.
- Files: N/A (no code yet).
- Risk: Regressions and broken examples once code is added.
- Priority: High once first phase delivers runnable content; add tests per phase.

---

*Concerns audit: 2025-02-25*
