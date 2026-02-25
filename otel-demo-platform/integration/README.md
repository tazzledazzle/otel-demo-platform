# Integration / E2E

Full run order and verification steps for the demo. See the [root README](../README.md) for prerequisites and architecture.

## Run order

1. **Infrastructure:** `docker compose up -d` (from repo root)
2. **Agent:** `cd agent && pip install -r requirements.txt && python -m agent.main` (Ollama + model required)
3. **Worker:** `cd worker && ./gradlew run`
4. **API:** `cd api && ./gradlew run`

## Smoke check

Confirm services before sending chat:

- **API:** `GET http://localhost:8080/health`
- **Agent:** `GET http://localhost:8000/health`

Example: `curl -s http://localhost:8080/health && curl -s http://localhost:8000/health`

## Send a request

```bash
curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"message":"Hello"}'
```

More examples (e.g. "What is 2 + 2?") are in `test-data/sample_requests.json`.

## View one trace in Grafana

- Open http://localhost:3000 (admin / admin).
- Go to **Explore** → select **Tempo**.
- Find the trace by service name (e.g. `api` or `otel-demo-api`) or time range.
- You should see one trace with spans for **API**, **worker**, and **agent**.

Expect a JSON response with `reply` from the curl above; the same flow appears as one end-to-end trace in Tempo.
