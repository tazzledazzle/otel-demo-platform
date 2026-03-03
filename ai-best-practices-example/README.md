# AI Best Practices Example

Example repository for **AI-powered applications**, **generative AI integration**, and **local AI infrastructure**. One Python-first project with a provider-agnostic LLM layer, config-driven prompts, retries, token awareness, and a local “cluster” via Docker Compose (Ollama, optional vector DB and app).

## Goals

- **AI-powered applications**: Production-style, testable example apps (chat CLI, RAG).
- **Generative AI integration**: Provider-agnostic client (OpenAI SDK with `base_url`), config-driven prompts, tenacity retries, token counting.
- **AI infrastructure**: Local cluster = Docker Compose (Ollama + optional app). No Kubernetes in initial scope.

## Prerequisites

- **Python 3.11+**
- **Docker** (for Ollama)
- **uv** (recommended) or pip

## Setup

1. **Clone and install**

   ```bash
   cd ai-best-practices-example
   uv sync
   # or: pip install -e .
   ```

2. **Environment**

   ```bash
   cp .env.example .env
   ```

   For local Ollama use:

   - `LLM_BASE_URL=http://localhost:11434/v1`
   - `OPENAI_API_KEY=placeholder`
   - `LLM_MODEL=llama3.2:3b` (or any model you pull)

3. **Start Ollama (Docker)**

   ```bash
   docker compose up -d ollama
   ollama pull llama3.2:3b
   ```

## Quick start

- **Chat CLI**

  ```bash
  uv run python examples/chat_cli.py
  ```

  (Or from project root: `python examples/chat_cli.py` — ensure project root is on `PYTHONPATH`, or run with `uv run`.)

- **RAG demo**

  Ingests a few sample documents into in-process Chroma, then answers questions:

  ```bash
  uv run python examples/rag_demo.py
  ```

  Requires an embedding model (e.g. `ollama pull nomic-embed-text` if using Ollama).

- **Optional API**

  ```bash
  uv run uvicorn ai_app.api.app:app --reload --host 0.0.0.0 --port 8000
  ```

  Endpoints: `POST /chat`, `POST /rag`, `GET /health`.

## Configuration and prompts

- **Config**: Single source of truth in `config/settings.py` (Pydantic Settings from env and `.env`). No secrets in code. See `.env.example` for variables.
- **Prompts**: Stored in `config/prompts/` as YAML (registry in `index.yaml`) and Jinja2 templates. Used by services only; iterate and review there.

## Tests

- **Unit tests** (mock LLM, no network):

  ```bash
  uv run pytest tests/ -v
  ```

  Run from project root so `config` and `ai_app` are importable (e.g. `uv run` adds the package to the path).

- **Integration test** (optional): Set `OLLAMA_URL` (e.g. `http://localhost:11434/v1`) to run the test that calls local Ollama. Otherwise it is skipped.

## Layout

- `config/` — settings and prompt templates
- `src/ai_app/` — LLM layer (`llm/`), prompts loader (`prompts/`), services (`services/`), optional API (`api/`)
- `examples/` — `chat_cli.py`, `rag_demo.py`
- `tests/` — `conftest.py`, unit tests, optional integration test
- `docker-compose.yml` — Ollama; optional app service (see comments)
- `docs/ARCHITECTURE.md` — short architecture overview

## License

MIT (see LICENSE file if present).
