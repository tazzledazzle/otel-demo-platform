---
phase: 03-live-coding-feature
plan: 01
subsystem: agent
tags: langchain, ollama, runnable, lcel, pytest

# Dependency graph
requires: []
provides:
  - Pipeline with new runnable step (prompt | llm | summarize_step)
  - Test that new step is exercised and output is asserted
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns: prompt | llm | new_step (LCEL), RunnableLambda for post-LLM step

key-files:
  created: []
  modified: otel-demo-platform/agent/agent/chain.py, otel-demo-platform/agent/tests/test_chain.py

key-decisions:
  - "Summarize step implemented as pass-through RunnableLambda returning AIMessage for _Executor compatibility"
  - "Executor normalizes list content to string when AIMessage.content is a list"

patterns-established:
  - "Post-LLM chain step: RunnableLambda that accepts LLM output and returns value with .content"
  - "Test mock LLM with RunnableLambda so LCEL invokes it (MagicMock is not invoked as a runnable)"

# Metrics
duration: ~5min
completed: "2026-02-25"
---

# Phase 3 Plan 1: Live-Coding Feature Summary

**New chain step (prompt | llm | summarize_step) in agent/chain.py with RunnableLambda and test that asserts chain output.**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-02-25T03:52:02Z
- **Completed:** 2026-02-25
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Added `_summarize_step` runnable (RunnableLambda) after the LLM; chain is `prompt | llm | new_step`.
- `get_agent_executor()` returns an executor whose `invoke()` returns `{"output": ...}`.
- New test `test_chain_includes_summarize_step` mocks LLM with RunnableLambda, invokes executor, asserts `output` and exact content.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add new chain step in chain.py** - `e10c53e` (feat)
2. **Task 2: Add test for new step / chain output** - `514570a` (test)

**Plan metadata:** `4e5c2cf` (docs: complete plan)

## Files Created/Modified

- `otel-demo-platform/agent/agent/chain.py` - Added _summarize_step, RunnableLambda, chain = prompt | llm | new_step; executor list-content normalization.
- `otel-demo-platform/agent/tests/test_chain.py` - Added test_chain_includes_summarize_step (RunnableLambda mock, assert output).

## Decisions Made

- Summarize step is a pass-through that ensures result has `.content` for _Executor; implemented with AIMessage and str/list content handling.
- Executor normalizes `result.content` when it is a list (join to string) so output is always a string.
- Test uses RunnableLambda as mock LLM so the LCEL sequence invokes it; MagicMock is not invoked as a runnable by LangChain.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical] Executor list content normalization**
- **Found during:** Task 2 (test asserted exact output)
- **Issue:** LangChain AIMessage can have `.content` as a list; executor returned list and test expected string.
- **Fix:** In _Executor.invoke, if `content` is a list, join to string before returning `{"output": content}`.
- **Files modified:** otel-demo-platform/agent/agent/chain.py
- **Committed in:** 514570a (Task 2)

**2. [Rule 3 - Blocking] Mock LLM not invoked by LCEL**
- **Found during:** Task 2 (test got MagicMock as chain result)
- **Issue:** Patching get_llm with MagicMock meant the “LLM” in the pipe was not invoked by RunnableSequence; chain result was the mock itself.
- **Fix:** Use RunnableLambda(lambda _: AIMessage(content="...")) as mock LLM so the framework invokes it and passes output to new_step.
- **Files modified:** otel-demo-platform/agent/tests/test_chain.py
- **Committed in:** 514570a (Task 2)

---

**Total deviations:** 2 auto-fixed (1 missing critical, 1 blocking)
**Impact on plan:** Necessary for correctness and for tests to run; no scope creep.

## Issues Encountered

None beyond the deviations above (handled inline).

## User Setup Required

None - no external service configuration required for tests (Ollama optional for manual invoke).

## Next Phase Readiness

- Live-coding pipeline step and test are in place; demonstrable via pytest and (with stack) via trace in Grafana.
- No blockers.

## Self-Check: PASSED

- FOUND: .planning/phases/03-live-coding-feature/03-01-SUMMARY.md
- FOUND: commit e10c53e
- FOUND: commit 514570a

---
*Phase: 03-live-coding-feature*
*Completed: 2026-02-25*
