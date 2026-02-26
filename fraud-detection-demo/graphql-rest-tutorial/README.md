# GraphQL & REST Tutorial — Phase 1

One runnable REST API (Phase 1 of the tutorial). Minimal FastAPI app with two GET operations and interactive docs.

## Prerequisites

- Python 3.10+
- pip

## Install

```bash
pip install -r requirements.txt
```

## Run

From the project root:

```bash
fastapi dev main.py
```

Server listens on http://127.0.0.1:8000.

## Test

- **Root:** `curl http://127.0.0.1:8000` — returns JSON with a message.
- **Greeting:** `curl http://127.0.0.1:8000/greeting` — returns JSON greeting; add `?name=Alice` for a personalized greeting.
- **Interactive docs:** Open http://127.0.0.1:8000/docs in a browser for Swagger UI.
