# Agent service (Python)

LangChain + Ollama agent; exposes `POST /invoke`. Run after starting Ollama and pulling a model (e.g. `ollama pull llama3.2`).

```bash
pip install -e ".[dev]"
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 python -m agent.main
```

Default: http://localhost:8000. Set `AGENT_PORT`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL` as needed.
