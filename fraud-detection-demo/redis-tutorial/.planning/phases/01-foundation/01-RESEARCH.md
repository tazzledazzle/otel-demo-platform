# Phase 1: Foundation — Research

**Researched:** 2026-02-25  
**Domain:** Redis client (Python), connection, basic operations (string set/get, optional list/hash/TTL)  
**Confidence:** HIGH

## Summary

Phase 1 needs one runnable example that connects to Redis and performs basic operations so the learner sees read/write working. The standard choice for a minimal, engineer-oriented tutorial is **Python with redis-py**: official Redis client, simple synchronous API, and excellent docs. Use a single script (not notebook) for “run and see output”; connection via `redis.Redis(...)` or `redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))` with connection details documented. Require at least connect + set + get; add one extra structure—hash or TTL (setex/ttl)—to show one more data type or expiration without scope creep.

**Primary recommendation:** Use **redis-py** (Python) with a single runnable script: connect (host/port or REDIS_URL), set/get, and one of hash or TTL; document Redis running locally or via URL; success = learner runs the script and sees read/write work.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Operations:** At least connect, set, get. Optionally one more (list, hash, or TTL).
- **Deliverable:** Single runnable script or small app; success = learner runs and sees read/write work.
- **Redis instance:** Local or cloud; connection (URL/env) documented. No clustering in Phase 1.
- **Language and client:** Language TBD (e.g. Python, Node, or Java); standard client library. Prerequisites stated (Redis running, client install).

### Claude's Discretion
- Exact client and language; which extra data structure to show; script vs notebook.

### Deferred Ideas (OUT OF SCOPE)
- Pub/sub, sessions, rate limiting, production patterns — later phases.

</user_constraints>

## Standard Stack

### Core
| Library   | Version | Purpose                          | Why Standard                                      |
|----------|---------|----------------------------------|---------------------------------------------------|
| redis    | 5.x–7.x | Official Redis client for Python | Official client; sync/async; RESP2/RESP3; docs on redis.io and readthedocs. |

- **Current stable:** 7.2.1 on PyPI (Feb 2025). For Phase 1, pin `redis>=5.0,<8` (or `redis~=5.0` for minimal surface).
- **Python:** 3.9+ (redis-py 6.2+); 3.8 supported up to redis-py 6.1.

### Supporting
| Tool / practice | Purpose                    | When to use                          |
|-----------------|----------------------------|--------------------------------------|
| `decode_responses=True` | Get strings instead of bytes | Always for learner-facing examples   |
| `REDIS_URL` / `from_url()` | Connection from env / URL  | When documenting “local or cloud”    |
| `pip install redis`      | Install client             | Prerequisites section                |

### Alternatives Considered
| Instead of | Could use   | Tradeoff |
|------------|-------------|----------|
| redis-py (Python) | ioredis / node-redis (Node) | Node: async by default; ioredis deprecated in favor of node-redis. Python + redis-py is simpler for “one script, run it.” |
| redis-py           | Jedis / Lettuce (Java)     | Java needs build/classpath; heavier for “one runnable example.” |
| Script              | Jupyter notebook           | Script is easier “run from CLI and see output”; notebook optional later. |

**Installation:**
```bash
pip install redis
# Optional faster parser (no code change):
pip install "redis[hiredis]"
```

## Architecture Patterns

### Recommended project layout (Phase 1)
```
redis-tutorial/
├── .planning/
├── README.md              # Prerequisites: Redis running, pip install redis
├── requirements.txt       # redis>=5.0
└── 01_foundation.py       # or scripts/01_foundation.py — single runnable script
```

### Pattern 1: Create client and ping
**What:** Construct client and verify connectivity with `ping()`.  
**When:** Start of every example.  
**Example:**
```python
# Source: https://redis.io/docs/latest/develop/clients/redis-py/connect
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.ping()  # True
```

### Pattern 2: Set and get string
**What:** Basic write/read.  
**When:** Required minimum for Phase 1.  
**Example:**
```python
# Source: https://redis.io/docs/latest/develop/clients/redis-py/connect
r.set('foo', 'bar')   # True
r.get('foo')          # 'bar' (string if decode_responses=True)
```

### Pattern 3: Connect from URL / env
**What:** Use `REDIS_URL` for local or cloud.  
**When:** Documenting “local or cloud” connection.  
**Example:**
```python
# Source: redis.readthedocs.io connection_examples.html + common practice
import os
import redis
url = os.getenv('REDIS_URL', 'redis://localhost:6379')
r = redis.from_url(url, decode_responses=True)
r.ping()
```

### Pattern 4: Optional — hash
**What:** One extra structure: hash (e.g. user-session style).  
**Example:**
```python
# Source: https://redis.io/docs/latest/develop/clients/redis-py/connect
r.hset('user-session:123', mapping={'name': 'John', 'age': 29})
r.hgetall('user-session:123')  # {'name': 'John', 'age': '29'}
```

### Pattern 5: Optional — TTL
**What:** setex + ttl so learner sees expiration.  
**Example:**
```python
# Source: redis.readthedocs.io set_and_get_examples.html
r.setex('important_key', 100, 'important_value')  # 100 seconds
r.ttl('important_key')  # 100
```

### Anti-patterns to avoid
- **Omitting `decode_responses=True`:** Default is bytes; learners get `b'bar'` and confusion. Set it on the client (or on the pool if using a custom ConnectionPool).
- **Using a custom ConnectionPool but passing `decode_responses` only to `Redis()`:** Pool wins; pass `decode_responses=True` to `ConnectionPool(...)` when using a pool.
- **Pub/sub or connection pools in Phase 1:** Deferred; keep the script to connect + set/get + one optional structure.

## Don't Hand-Roll

| Problem              | Don't build              | Use instead     | Why                          |
|----------------------|--------------------------|-----------------|------------------------------|
| Parsing Redis URL    | Manual host/port/password parsing | `redis.from_url()` | Handles redis://, rediss://, query params. |
| Connection retries   | Custom backoff loop      | redis-py built-in retries (v6+) | Default retries; no extra code. |
| RESP protocol        | Raw socket protocol      | redis-py        | Full command set, encoding.  |

**Key insight:** Redis URL parsing and connection behavior are standardized; use the client’s `from_url()` and default options.

## Common Pitfalls

### Pitfall 1: Bytes vs string responses
**What goes wrong:** `r.get('foo')` returns `b'bar'`; comparisons or print look wrong.  
**Why:** Default is `decode_responses=False`.  
**How to avoid:** Always pass `decode_responses=True` for learner-facing code.  
**Warning signs:** Byte literals in output or string comparison errors.

### Pitfall 2: decode_responses ignored with custom ConnectionPool
**What goes wrong:** You pass `decode_responses=True` to `Redis(connection_pool=pool)` but still get bytes.  
**Why:** Connection options are taken from the pool, not from the client.  
**How to avoid:** Pass `decode_responses=True` to `ConnectionPool(...)` when creating the pool. For Phase 1, avoid custom pools; use `Redis(...)` or `from_url(...)` only.

### Pitfall 3: Redis not running
**What goes wrong:** ConnectionRefusedError or similar on run.  
**Why:** Redis server not started or wrong host/port.  
**How to avoid:** Document in README: “Start Redis (e.g. `docker run -p 6379:6379 redis:latest` or local install).” Script can catch connection errors and print a clear “Is Redis running?” message.

## Code Examples

Verified patterns from official sources:

### Minimal runnable script (connect + set + get)
```python
# Sources: redis.io redis-py connect, redis.readthedocs.io set_and_get_examples
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.ping()

r.set('foo', 'bar')
print(r.get('foo'))  # bar
```

### With REDIS_URL and optional hash
```python
import os
import redis

r = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'), decode_responses=True)
r.ping()

r.set('greeting', 'Hello, Redis!')
print(r.get('greeting'))

r.hset('user:1', mapping={'name': 'Alice', 'role': 'learner'})
print(r.hgetall('user:1'))
```

### With TTL (setex + ttl)
```python
r.setex('temp_key', 60, 'expires in 60 seconds')
print(r.ttl('temp_key'))  # 60
```

## State of the Art

| Old / alternative     | Current for Phase 1      | Note                    |
|-----------------------|-------------------------|-------------------------|
| StrictRedis            | redis.Redis             | StrictRedis alias; use Redis. |
| Manual URL parsing     | redis.from_url()        | Standard for REDIS_URL. |
| RESP 2 only            | RESP 2 default; protocol=3 optional | Phase 1 stays default. |
| ioredis (Node)         | node-redis              | For Node; not needed for Phase 1. |

**Deprecated / out of scope for Phase 1:** Pub/sub in this phase; production TLS/pools; clustering.

## Open Questions

1. **Script vs notebook**  
   - **Known:** Script is simpler for “run once, see output.”  
   - **Recommendation:** Single script (e.g. `01_foundation.py`); notebook can be a later phase if desired.

2. **Which optional structure (list / hash / TTL)**  
   - **Known:** Hash and TTL are both one extra concept; list is also simple (lpush/lrange).  
   - **Recommendation:** Either **hash** (hset/hgetall) or **TTL** (setex/ttl). Hash shows a second structure; TTL shows expiration. Planner can pick one.

## Sources

### Primary (HIGH confidence)
- [Redis redis-py connect](https://redis.io/docs/latest/develop/clients/redis-py/connect) — basic connection, set/get, hash, pool, URL.
- [redis-py set and get examples](https://redis.readthedocs.io/en/stable/examples/set_and_get_examples.html) — set, get, setex, ttl, mset, mget.
- [redis-py connection examples](https://redis.readthedocs.io/en/stable/examples/connection_examples.html) — default, from_url, credentials.
- [redis-py GitHub README](https://github.com/redis/redis-py#readme) — install, usage, supported Redis versions.
- PyPI redis 7.2.1 — current stable version.

### Secondary (MEDIUM confidence)
- WebSearch: redis-py vs ioredis / Node; REDIS_URL + from_url; list/hash/TTL API patterns — confirmed against official docs.
- Stack Overflow / Lightrun: decode_responses and ConnectionPool — behavior confirmed from official connection docs.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — redis-py is official, PyPI and docs checked.
- Architecture: HIGH — single script, connect/set/get + one optional structure, from_url and decode_responses verified.
- Pitfalls: HIGH — decode_responses and pool behavior documented in official and community sources.

**Research date:** 2026-02-25  
**Valid until:** ~30 days for redis-py (stable API).

---

## RESEARCH COMPLETE

**Phase:** 1 - Foundation  
**Confidence:** HIGH

### Key findings
- **redis-py** is the standard Python client; use it for a single runnable script (connect, set, get, optional hash or TTL).
- Always use **decode_responses=True** in examples; support **REDIS_URL** via **redis.from_url()** for “local or cloud.”
- One optional structure is enough: **hash** (hset/hgetall) or **TTL** (setex/ttl); both are simple and documented.
- Avoid custom ConnectionPool in Phase 1; if used later, set decode_responses on the pool.

### File created
`redis-tutorial/.planning/phases/01-foundation/01-RESEARCH.md`

### Confidence assessment
| Area           | Level | Reason |
|----------------|-------|--------|
| Standard stack | HIGH  | Official client, PyPI 7.2.1, docs verified. |
| Architecture   | HIGH  | Single script + URL/env pattern from official examples. |
| Pitfalls       | HIGH  | decode_responses and pool behavior documented. |

### Open questions
- None blocking. Planner can choose script name, optional structure (hash vs TTL), and exact README wording.

### Ready for planning
Research complete. Planner can create PLAN.md from this file.
