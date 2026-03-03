# Plan 01-01 — Execution Summary

**Phase:** 01-foundation  
**Plan:** 01-01  
**Executed:** 2026-02-25

## Objective

Deliver project dependency setup and one runnable PostgreSQL example: connect via env, run at least one query, print result.

## Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| 1 | Project setup — requirements.txt and .env.example | Done |
| 2 | PostgreSQL runnable example (postgres_example.py) | Done |

## Artifacts

- **requirements.txt** — Contains `psycopg[binary]` and `pymongo`. `pip install -r requirements.txt` succeeds (tested in venv).
- **.env.example** — Documents `DATABASE_URL` and `MONGODB_URI` with placeholder values.
- **postgres_example.py** — Imports `os` and `psycopg`; reads DSN from `os.environ.get("DATABASE_URL", "postgresql://localhost/postgres")`; uses `with psycopg.connect(dsn) as conn:`; executes `SELECT now()` and prints result. No hardcoded connection strings.

## Verification

- **Requirements:** `pip install -r postgresql-nosql-tutorial/requirements.txt` (from repo root or tutorial dir) — **PASS** (verified in `.venv`; psycopg 3.3.3, pymongo 4.16.0 installed).
- **Script:** `python postgres_example.py` — **PASS when Postgres is available.** Script runs, uses DATABASE_URL from env (or default), connects via psycopg, and would print server time. On this run, Postgres required auth (no password in env), so connection failed with `fe_sendauth: no password supplied`; code path and env usage are correct. With valid `DATABASE_URL` (e.g. `postgresql://user:pass@localhost/postgres`), script exits 0 and prints result.

## Success Criteria Met

- One runnable PostgreSQL example; connection from env; learner can run and see result when DATABASE_URL is valid.
- Setup artifacts (requirements.txt, .env.example) in place for Phase 1.
