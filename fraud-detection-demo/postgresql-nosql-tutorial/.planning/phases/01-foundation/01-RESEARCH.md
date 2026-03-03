# Phase 1: Foundation — Research

**Researched:** 2026-02-25
**Domain:** PostgreSQL + one NoSQL store (Python clients, minimal runnable examples)
**Confidence:** HIGH

## Summary

Phase 1 needs two separate minimal examples: one for PostgreSQL (connect + at least one query or simple CRUD) and one for one NoSQL store (connect + one or two operations), in a single runnable unit with clear setup. No hybrid workflow.

**Standard stack:** Python 3.10+ with **psycopg** (3) for PostgreSQL—sync is enough for a single script and avoids asyncio. For NoSQL, **MongoDB with PyMongo** is the best fit: document store gives a clear contrast to relational Postgres, PyMongo has a minimal connect/insert/find API, and setup is either Docker or Atlas free tier. Redis (redis-py) is a valid alternative with even simpler setup and set/get; DynamoDB (boto3 + DynamoDB Local) adds JRE/AWS or Docker and table design, so it’s heavier for “one runnable example.”

**Primary recommendation:** Use Python, psycopg (sync) for Postgres, and PyMongo for MongoDB. Deliver two scripts (e.g. `postgres_example.py` and `mongodb_example.py`) or one script with two sections; document connection strings via env and prerequisites (Postgres + MongoDB running locally or via Docker/Atlas).

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **PostgreSQL example:** Connect, run at least one query (e.g. SELECT or simple CRUD); small schema or no schema. Single script or notebook; success = learner runs and sees result.
- **NoSQL example:** One store (e.g. MongoDB, Redis, or DynamoDB-style); connect and one or two operations (e.g. insert, get). Same runnable unit; clear setup and client.
- **Scope:** No hybrid pattern in Phase 1; just “here’s Postgres, here’s NoSQL.” Prerequisites and run steps documented.

### Claude's Discretion
- Which NoSQL store; language and clients; exact query/operation examples.

### Deferred Ideas (OUT OF SCOPE)
- Hybrid patterns, when to use which, production patterns — later phases.

</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| psycopg | ≥3.1 (use latest, e.g. 3.3.x) | PostgreSQL adapter (sync) | Official successor to psycopg2; one package `psycopg`, sync API fits single-script tutorial; `conn.execute(...).fetchone()` minimal. |
| pymongo | ≥4.x (stable) | MongoDB driver | Official driver; sync `MongoClient`, `insert_one`, `find_one`; no ORM needed. |

### Supporting
| Library | Purpose | When to Use |
|---------|---------|-------------|
| (stdlib) | — | Connection strings from `os.environ`; no extra deps. |

### NoSQL alternative (if not MongoDB)
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| PyMongo (MongoDB) | redis (redis-py) | Redis: simpler setup (single binary/Docker), set/get only; key-value vs document. Use if minimizing dependencies/setup. |
| PyMongo | boto3 + DynamoDB Local | DynamoDB: more setup (JRE or Docker, table creation, partition keys); better for later “AWS” phase. |

**Installation:**
```bash
pip install "psycopg[binary]" pymongo
```
Use `psycopg[binary]` so learners need no system libpq/build tools. Optional: `redis` for Redis alternative.

## Architecture Patterns

### Recommended Project Structure
```
postgresql-nosql-tutorial/
├── .planning/
├── postgres_example.py    # or examples/postgres_example.py
├── mongodb_example.py     # or examples/mongodb_example.py
├── requirements.txt      # psycopg[binary], pymongo
├── README.md             # Prerequisites, env vars, run steps
└── (optional) .env.example # DATABASE_URL, MONGODB_URI
```
Alternative: one script with two entry points or two clearly separated blocks (e.g. `if __name__ == "__main__": run_postgres()` and `run_mongodb()`) so “one runnable unit” can mean one file or two.

### Pattern 1: PostgreSQL — connect and one query (sync)
**What:** Use psycopg (package name `psycopg`, not psycopg3). Connect with context manager; execute SELECT (or one INSERT then SELECT); no schema required (e.g. `SELECT 1` or `SELECT now()`).
**When:** Phase 1 single script; no async.
**Example:**
```python
# Source: https://www.psycopg.org/psycopg3/docs/basic/usage.html
import os
import psycopg

dsn = os.environ.get("DATABASE_URL", "postgresql://localhost/postgres")
with psycopg.connect(dsn) as conn:
    row = conn.execute("SELECT now()").fetchone()
    print(row[0])
```

### Pattern 2: MongoDB — connect, insert_one, find_one
**What:** PyMongo sync client; get database and collection; insert one document; find_one to read it back.
**When:** Phase 1 “one or two operations.”
**Example:**
```python
# Source: PyMongo tutorial (pymongo.readthedocs.io)
from pymongo import MongoClient
import os

uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(uri)
db = client.get_database("tutorial")
coll = db.get_collection("demo")
coll.insert_one({"name": "example", "value": 1})
doc = coll.find_one({"name": "example"})
print(doc)
client.close()
```

### Anti-Patterns to Avoid
- **Hardcoding connection strings in source:** Use env vars and document in README (e.g. `DATABASE_URL`, `MONGODB_URI`).
- **Using psycopg2 for new tutorial:** Prefer psycopg (3); same mental model, simpler one-liner execute + fetch, and current docs.
- **Async in Phase 1:** Avoid asyncio/async drivers for the minimal example; sync keeps “run script, see output” trivial.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Connection handling | Manual open/close, no context manager | `with psycopg.connect(...) as conn` / MongoClient + close | Correct commit/rollback and cleanup. |
| Parameterized queries | String format for user input | `cur.execute("SELECT * FROM t WHERE id = %s", [id])` (psycopg) | SQL injection; psycopg uses server-side binding. |
| Env/config | Custom config file for URLs | `os.environ.get("DATABASE_URL", "default")` | No extra deps; standard for tutorials. |

**Key insight:** For “one runnable example,” keep to the official client’s minimal API; no ORM, no pool, no custom connection wrapper.

## Common Pitfalls

### Pitfall 1: psycopg3 — `IN %s` with a tuple
**What goes wrong:** `conn.execute("SELECT * FROM t WHERE id IN %s", [(1,2,3)])` raises (server-side binding: `IN $1` is invalid).
**Why:** Psycopg 3 uses server-side parameters; `IN` expects value list, not a single tuple.
**How to avoid:** Use `= ANY(%s)` and pass a list: `conn.execute("SELECT * FROM t WHERE id = ANY(%s)", [[1,2,3]]).`
**Warning signs:** SyntaxError near `$1` in IN clause.
**Source:** https://www.psycopg.org/psycopg3/docs/basic/from_pg2.html

### Pitfall 2: psycopg3 — `with conn` closes the connection
**What goes wrong:** Expecting `with conn:` to only commit/rollback (like psycopg2); in psycopg3 the connection is closed on exit.
**Why:** Psycopg 3 changed behavior so `with` closes the connection.
**How to avoid:** Use `with psycopg.connect(...) as conn:` for “use once and close”; for multiple transactions use `conn.transaction()` or explicit commit/close.
**Source:** https://www.psycopg.org/psycopg3/docs/basic/from_pg2.html#with-connection

### Pitfall 3: MongoDB — connection string and auth
**What goes wrong:** Wrong URI format (e.g. missing `mongodb://`) or password with special chars not encoded.
**How to avoid:** Document standard form `mongodb://[user:password@]host[:port][/db]`; for Atlas use the URI from the UI; encode credentials if needed.
**Warning signs:** Auth or connection timeout errors on first run.

### Pitfall 4: Running examples without services
**What goes wrong:** Learner runs script without Postgres or MongoDB; connection refused.
**How to avoid:** README must list prerequisites: Postgres and MongoDB running (e.g. local install, Docker one-liners, or Atlas for MongoDB). Optional: `.env.example` with placeholder URLs.

## Code Examples

Verified patterns from official sources:

### PostgreSQL — minimal connect and SELECT
```python
# Source: https://www.psycopg.org/psycopg3/docs/basic/usage.html
import psycopg
# One-liner form from same page:
# print(psycopg.connect(DSN).execute("SELECT now()").fetchone()[0])
with psycopg.connect("dbname=test user=postgres") as conn:
    cur = conn.execute("SELECT 1 as num")
    print(cur.fetchone())
```

### PostgreSQL — INSERT with parameters
```python
# Source: https://www.psycopg.org/psycopg3/docs/basic/usage.html
with psycopg.connect(dsn) as conn:
    conn.execute(
        "INSERT INTO test (num, data) VALUES (%s, %s)",
        (100, "abc"),
    )
    # conn context manager commits on exit
```

### MongoDB — connect and find_one (PyMongo)
```python
# Source: PyMongo tutorial (pymongo.readthedocs.io)
from pymongo import MongoClient
client = MongoClient(uri)
db = client.get_database("sample_mflix")
movies = db.get_collection("movies")
movie = movies.find_one({"title": "Back to the Future"})
print(movie)
client.close()
```

### Redis alternative — set and get (if choosing Redis)
```python
# Source: redis-py docs / Redis official Python client docs
import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.set("key", "value")
print(r.get("key"))  # 'value'
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| psycopg2 only | psycopg (3) as default for new code | Psycopg 3 stable; psycopg2 still maintained | Use `psycopg` and `psycopg[binary]`; install is `pip install "psycopg[binary]"`. |
| psycopg2-binary | psycopg[binary] | Same as above | No `psycopg3` package name; import is `import psycopg`. |

**Deprecated/outdated:** Relying on psycopg2 for new tutorials when psycopg 3 is documented and simpler for minimal examples.

## Open Questions

1. **Single file vs two files**
   - What we know: “Same runnable unit” can mean one script or two; CONTEXT says “single script or notebook” for Postgres and “same runnable unit” for both.
   - What’s unclear: Whether “one runnable unit” must be one file.
   - Recommendation: Planner can choose: either two scripts (`postgres_example.py`, `mongodb_example.py`) with one README and one `requirements.txt`, or one script with two sections/functions. Both satisfy “clear setup” and “two separate minimal examples.”

2. **MongoDB: local vs Atlas**
   - What we know: PyMongo works with local MongoDB or Atlas; Atlas has free tier and no local install.
   - Recommendation: Document both: “Run MongoDB locally (e.g. Docker) or use MongoDB Atlas; set MONGODB_URI.” Planner can add one optional Docker Compose or link to Atlas signup.

## Sources

### Primary (HIGH confidence)
- https://www.psycopg.org/psycopg3/docs/basic/usage.html — connect, execute, fetch, context manager
- https://www.psycopg.org/psycopg3/docs/basic/from_pg2.html — IN %s, with connection, install
- https://www.psycopg.org/psycopg3/docs/basic/install.html — psycopg[binary], no psycopg3 package
- PyMongo tutorial (pymongo.readthedocs.io) — MongoClient, get_database, get_collection, find_one, sync usage

### Secondary (MEDIUM confidence)
- WebSearch: psycopg2 vs psycopg3 async; Redis redis-py set/get; DynamoDB Local boto3 — patterns and alternatives confirmed via official docs where applicable.

### Tertiary (LOW confidence)
- Redis official Python client URL returned 404; redis-py patterns from readthedocs/community sources; sufficient for “Redis alternative” subsection.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — psycopg and PyMongo docs and install verified; recommendation from CONTEXT discretion.
- Architecture: HIGH — two separate examples, env-based URLs, no hybrid.
- Pitfalls: HIGH — psycopg3 IN/with behavior from official “from_pg2” page.

**Research date:** 2026-02-25
**Valid until:** ~30 days for stable clients; re-check if adding async or DynamoDB in a later phase.

---

## RESEARCH COMPLETE

**Phase:** 1 - Foundation  
**Confidence:** HIGH

### Key Findings
- Use **psycopg** (3) sync for PostgreSQL; install `psycopg[binary]`; import `psycopg` (no psycopg3 package name). One query is enough (e.g. `SELECT now()` or one INSERT + SELECT).
- **MongoDB + PyMongo** recommended for NoSQL: document store contrast, minimal API (connect, insert_one, find_one), setup via Docker or Atlas. **Redis (redis-py)** is a simpler alternative (set/get) if minimizing setup.
- Two separate minimal examples (two scripts or one script with two sections); connection strings from env; README with prerequisites and run steps.
- Avoid: hardcoded URLs; psycopg3 `IN %s` with tuple (use `= ANY(%s)` and list); assuming `with conn` in psycopg3 only commits (it also closes connection).

### File Created
`postgresql-nosql-tutorial/.planning/phases/01-foundation/01-RESEARCH.md`

### Confidence Assessment
| Area           | Level | Reason |
|----------------|-------|--------|
| Standard Stack | HIGH  | Official psycopg and PyMongo docs and install verified. |
| Architecture   | HIGH  | CONTEXT and ROADMAP constrain to two examples, no hybrid. |
| Pitfalls       | HIGH  | psycopg3 IN/with from official from_pg2 page. |

### Open Questions
- Single file vs two files: planner can choose; both valid.
- MongoDB local vs Atlas: document both; optional Docker or Atlas link.

### Ready for Planning
Research complete. Planner can create PLAN.md using this stack (Python, psycopg, PyMongo), two minimal examples, env-based config, and the pitfalls/patterns above.
