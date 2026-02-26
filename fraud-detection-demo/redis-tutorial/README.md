# Redis Tutorial

A tutorial for software engineers learning Redis. Phase 1 delivers one runnable example: connect, set/get, and TTL.

## Prerequisites

- **Redis** running (e.g. start with Docker: `docker run -p 6379:6379 redis:latest`, or use a local install).
- **Python 3.9+**
- Install dependencies: `pip install -r requirements.txt` (or use a virtual environment: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`).

## Connection

- Optional: set `REDIS_URL` for a cloud or non-default Redis URL.
- Default: `redis://localhost:6379` if `REDIS_URL` is not set.

## How to run

```bash
python 01_foundation.py
```

The script connects to Redis, performs a set/get, and demonstrates TTL with `setex`/`ttl`. No clustering, pub/sub, or production setup in Phase 1.
