#!/usr/bin/env python3
"""Phase 1 foundation: connect to Redis, set/get, and TTL (setex/ttl)."""

import os
import sys

import redis

def main():
    url = os.getenv("REDIS_URL", "redis://localhost:6379")
    r = redis.from_url(url, decode_responses=True)

    try:
        r.ping()
    except redis.ConnectionError:
        print(
            "Could not connect to Redis. Is Redis running? "
            "Try: docker run -p 6379:6379 redis:latest"
        )
        sys.exit(1)

    r.set("greeting", "Hello, Redis!")
    print(r.get("greeting"))

    r.setex("temp_key", 60, "expires in 60 seconds")
    print(r.ttl("temp_key"))

if __name__ == "__main__":
    main()
