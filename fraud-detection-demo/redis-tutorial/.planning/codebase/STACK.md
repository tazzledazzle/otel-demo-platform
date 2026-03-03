# Technology Stack

**Analysis Date:** 2025-02-25

## Languages

**Primary (intended):**
- Not fixed. PROJECT.md specifies “client of choice (e.g. redis-py, Jedis)”—so Python or Java are implied options; others possible.

**Secondary:**
- Markdown for planning (`.planning/*.md`).

## Runtime

**Environment:**
- Redis (standalone or cluster) as the target backend. No runtime for tutorial code until phases add scripts/notebooks.

**Package Manager:**
- None in repo. When code is added: use project-appropriate manager (e.g. pip/uv for Python, npm/yarn for Node, Maven/Gradle for Java).
- Lockfile: Not present.

## Frameworks

**Core:**
- Redis (server). Client TBD per phase (e.g. redis-py, Jedis).

**Testing:**
- Not selected.

**Build/Dev:**
- GSD workflow driven by `config.json` (planning, plan-check, verifier, research).

## Key Dependencies

**Critical (when implemented):**
- Redis server (local or provided).
- Redis client library (e.g. redis-py, Jedis)—version to be pinned.

**Infrastructure:**
- None. Optional: Docker/Compose for Redis in dev or CI.

## Configuration

**Environment:**
- No .env or env docs yet. Future: REDIS_URL or REDIS_HOST/PORT/PASSWORD for connection.
- Key configs: Redis connection parameters when code exists.

**Build:**
- No build config. Add pyproject.toml, package.json, or similar when introducing code.

## Platform Requirements

**Development:**
- Redis available (local install or container). Client SDK for chosen language.

**Production:**
- Tutorial only; no production deployment. Examples may assume local Redis.

---

*Stack analysis: 2025-02-25*
