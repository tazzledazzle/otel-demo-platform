# GraphQL & REST Tutorial — Phase 1

One runnable REST API (Phase 1 of the tutorial). Minimal FastAPI app with two GET endpoints and interactive docs.

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

Or with uvicorn:

```bash
uvicorn main:app --reload
```

Server listens at **http://127.0.0.1:8000**.

## Test

- **Root:** `curl http://127.0.0.1:8000` — returns JSON with a message.
- **Greeting:** `curl http://127.0.0.1:8000/greeting` — returns a default greeting.
- **Greeting with name:** `curl "http://127.0.0.1:8000/greeting?name=Alice"` — returns a personalized greeting.
- **Interactive API docs:** Open **http://127.0.0.1:8000/docs** in your browser for Swagger UI.
