"""
Minimal PostgreSQL example: connect using DATABASE_URL and run a query.
Run with: python postgres_example.py
Requires: DATABASE_URL in environment or defaults to postgresql://localhost/postgres
"""
import os
import psycopg

dsn = os.environ.get("DATABASE_URL", "postgresql://localhost/postgres")

with psycopg.connect(dsn) as conn:
    row = conn.execute("SELECT now()").fetchone()
    print("PostgreSQL server time:", row[0])
