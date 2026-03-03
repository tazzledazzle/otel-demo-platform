# Architecture

## Overview

```
User → CLI / API → Service (Chat / RAG) → LLM client → Ollama or OpenAI
                         ↑
              Config (env) + Prompts (YAML/Jinja2)
```

- **CLI / API**: Thin entrypoints (`examples/chat_cli.py`, `examples/rag_demo.py`, optional FastAPI app). They build the LLM client and services from config and delegate to the service layer.
- **Services**: `ChatService` and `RAGService` use the shared LLM client and prompt manager. They do not call the LLM client directly with hardcoded prompts; prompts come from `config/prompts/`.
- **LLM client**: Provider-agnostic interface in `llm/base.py`; implementation in `llm/openai_compat.py` using the OpenAI SDK with a configurable `base_url`, so the same code works for OpenAI and Ollama.
- **Config / Prompts**: Single source of truth for environment (Pydantic Settings) and for prompt text (YAML registry + Jinja2 templates). No secrets in code; prompts are easy to iterate and review.

## Why provider-agnostic

The LLM layer is abstracted behind a small interface (`generate(messages, **kwargs) -> str`). The implementation uses the OpenAI-compatible API (OpenAI SDK + `base_url`), so you can point at OpenAI or at Ollama (or any compatible server) via configuration only. No code changes for switching providers.

## Why local cluster

The “cluster” here is a set of services on one machine via Docker Compose: Ollama (and optionally the app). This keeps the example simple and runnable without cloud or Kubernetes. For production at scale, you would use the same Docker image and something like KServe/MLServer; see your orchestrator’s docs.

## Components

| Component        | Role |
|-----------------|-----|
| `config/settings.py` | Pydantic Settings from env and `.env` (API key, base URL, model, temperature, max_tokens, paths). |
| `config/prompts/`    | YAML index + Jinja2 templates; loaded by `ai_app.prompts.loader.get_prompt()`. |
| `llm/base.py`       | Abstract `BaseLLMClient` and `Message`. |
| `llm/openai_compat.py` | OpenAI SDK client with retries (tenacity); used for chat (and embeddings in RAG). |
| `llm/token_utils.py`  | Token counting (tiktoken with fallback). |
| `services/chat.py`    | Builds messages (system prompt from template), calls LLM. |
| `services/rag.py`     | Chroma in-process; ingest (with embeddings), retrieve top-k, build RAG prompt, call LLM. |

Observability: structured logging (request/response sizes, model, duration) in the LLM client; no full message bodies in logs. No OpenTelemetry in this example—only logs and a note that you can add observability later.
