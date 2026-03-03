# Plan 01-02 — Execution Summary

**Phase:** 01-foundation  
**Plan:** 01-02  
**Executed:** 2026-02-25

## Objective

Deliver one runnable MongoDB example and README: connect via env, insert_one + find_one, print result; document prerequisites and run steps for both Postgres and MongoDB examples.

## Tasks Completed

| Task | Description | Status |
|------|-------------|--------|
| 1 | MongoDB runnable example (mongodb_example.py) | Done |
| 2 | README — prerequisites and run steps | Done |

## Artifacts

- **mongodb_example.py** — Uses PyMongo `MongoClient` (sync only). Reads `MONGODB_URI` from `os.environ.get("MONGODB_URI", "mongodb://localhost:27017")`. Connects, gets db `tutorial` and collection `demo`, `insert_one({"name": "example", "value": 1})`, `find_one` with same criteria, prints document. `client.close()` in `finally`. Handles `ServerSelectionTimeoutError` / `ConnectionFailure` with a clear stderr message and exit 1 when MongoDB is unavailable. `serverSelectionTimeoutMS=5000` for fast failure.
- **README.md** — Project description (PostgreSQL + NoSQL tutorial; Phase 1 = two runnable examples). Prerequisites: PostgreSQL and MongoDB (local, Docker, or cloud/Atlas). Docker one-liners for Postgres and MongoDB. MongoDB Atlas note with link. Environment variables table: `DATABASE_URL`, `MONGODB_URI` with defaults. Reference to `.env.example`. Run steps: `pip install -r requirements.txt`, set env if needed, `python postgres_example.py`, `python mongodb_example.py`. Short descriptions of both scripts.

## Verification

- **mongodb_example.py** — With MongoDB not running (or connection refused), script exits with code 1 and prints: "MongoDB connection failed. Is MongoDB running? Set MONGODB_URI if needed." plus exception details. **PASS** (clear error path). With MongoDB running and valid `MONGODB_URI`, script would exit 0 and print the found document.
- **README.md** — Contains `DATABASE_URL`, `MONGODB_URI`, `postgres_example`, `mongodb_example`, "Prerequisites", and "Run steps". **PASS**.

## Success Criteria Met

- One runnable MongoDB example; connection from env; learner can run and see result when MongoDB is available, or a clear error when not.
- README enables a new learner to install deps, set env, and run both examples; documents local, Docker, and Atlas options.
