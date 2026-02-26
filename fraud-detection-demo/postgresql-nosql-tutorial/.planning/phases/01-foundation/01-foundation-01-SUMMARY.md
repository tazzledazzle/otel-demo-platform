---
phase: 01-foundation
plan: 01
subsystem: database
tags: postgres, psycopg, python, env

# Dependency graph
requires: []
provides:
  - requirements.txt (psycopg[binary], pymongo)
  - .env.example (DATABASE_URL, MONGODB_URI)
  - postgres_example.py (runnable connect + query)
affects: []

# Tech tracking
tech-stack:
  added: psycopg[binary], pymongo
  patterns: env-based DSN, psycopg context manager, parameterized queries ready

key-files:
  created: requirements.txt, .env.example, postgres_example.py
  modified: []

key-decisions:
  - "Connection string from DATABASE_URL only; default postgresql://localhost/postgres for local runs"
  - "psycopg 3 (package psycopg) with binary extra so learners need no system libpq"

patterns-established:
  - "DSN from os.environ.get with fallback default"
  - "with psycopg.connect(dsn) as conn for connection lifecycle"

# Metrics
duration: ~5min
completed: "2026-02-26"
---

# Phase 01 Plan 01: Foundation (PostgreSQL example) Summary

**Project dependency setup and one runnable PostgreSQL example: connect via env, run a query, print result.**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-02-26T02:05:00Z (approx)
- **Completed:** 2026-02-26T02:06:02Z
- **Tasks:** 2
- **Files modified:** 3 created

## Accomplishments

- requirements.txt with psycopg[binary] and pymongo; pip install -r requirements.txt succeeds (e.g. in a venv).
- .env.example documenting DATABASE_URL and MONGODB_URI.
- postgres_example.py: reads DSN from DATABASE_URL, uses psycopg.connect context manager, runs SELECT now(), prints result.

## Task Commits

Each task was committed atomically:

1. **Task 1: Project setup — requirements and env example** - `6e654ae` (feat)
2. **Task 2: PostgreSQL runnable example** - `3ac2cdd` (feat)

**Plan metadata:** (final docs commit after STATE update)

## Files Created/Modified

- `postgresql-nosql-tutorial/requirements.txt` - psycopg[binary] and pymongo
- `postgresql-nosql-tutorial/.env.example` - DATABASE_URL, MONGODB_URI placeholders
- `postgresql-nosql-tutorial/postgres_example.py` - Connect via env, SELECT now(), print

## Decisions Made

None - followed plan as specified. Connection from env, no hardcoded DSN, context manager for connect.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Local pip is externally managed; verified install by creating a venv and running `pip install -r requirements.txt` there. No code or plan change.
- Script run verification requires a running Postgres instance and valid DATABASE_URL (e.g. with password if required). With Postgres available and env set, `python postgres_example.py` exits 0 and prints server time.

## User Setup Required

None beyond copying .env.example to .env and setting DATABASE_URL (and optionally MONGODB_URI) for later phases. For running postgres_example.py: start Postgres and set DATABASE_URL if not using default.

## Next Phase Readiness

- Setup artifacts in place for Phase 1.
- One runnable PostgreSQL example; learner can run and see result when Postgres is available.
- Ready for Plan 01-02 (NoSQL example) using same requirements and .env.

## Self-Check: PASSED

- requirements.txt, .env.example, postgres_example.py present.
- Commits 6e654ae and 3ac2cdd present in git history.

---
*Phase: 01-foundation*
*Completed: 2026-02-26*
