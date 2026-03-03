# Integration / E2E

Full run order and verification steps for the demo. See the [root README](../README.md) for prerequisites and architecture. Env vars and defaults: [CONFIG.md](../CONFIG.md).

## Run order

Preferred ports: **API 8080**, **Agent 8000**. If a port is in use, the process fails with a clear message (no automatic fallback). See [CONFIG.md](../CONFIG.md) for env vars.

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

Use port **8080** (not 8880). More examples in `test-data/sample_requests.json`.

## View one trace in Grafana

- Open http://localhost:3000 (admin / admin).
- Go to **Explore** → select **Tempo**.
- Find the trace: in **TraceQL** use `resource.service.name="otel-demo-api"` (service names are `otel-demo-api`, `otel-demo-worker`, `otel-demo-agent`). If you get "unknown identifier", add quotes; if you get 0 series, use `otel-demo-api` not `api`.
- You should see one trace with spans for API, worker, and agent.

Expect a JSON response with `reply` from the curl above; the  same flow appears as one end-to-end trace in Tempo.
