#!/usr/bin/env python3
"""RAG demo: ingest a few documents into Chroma, then run a query (retrieve → prompt → LLM)."""

import asyncio
import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config.settings import Settings
from ai_app.llm.openai_compat import OpenAICompatClient
from ai_app.services.rag import RAGService


def _sample_documents() -> list[str]:
    return [
        "The AI best practices repo uses a provider-agnostic LLM layer with OpenAI-compatible API.",
        "Ollama runs locally on port 11434. Use LLM_BASE_URL=http://localhost:11434/v1 for the client.",
        "Prompts are stored in config/prompts as YAML and Jinja2 templates for easy iteration.",
    ]


async def main() -> None:
    settings = Settings()
    llm_client = OpenAICompatClient(
        base_url=settings.llm_base_url,
        api_key=settings.openai_api_key,
        model=settings.llm_model,
        default_temperature=0.3,
        default_max_tokens=settings.max_tokens,
    )
    # Same client for embeddings (Ollama/OpenAI); use an embedding model name
    embedding_client = OpenAICompatClient(
        base_url=settings.llm_base_url,
        api_key=settings.openai_api_key,
        model="nomic-embed-text",
        default_temperature=0,
        default_max_tokens=0,
    )
    service = RAGService(
        llm=llm_client,
        prompts_dir=settings.prompts_dir,
        embedding_client=embedding_client,
        top_k=2,
    )
    print("Ingesting sample documents...")
    service.ingest(_sample_documents())
    print("Ask a question about the docs (or empty line to exit).")
    while True:
        try:
            question = input("Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            break
        answer = await service.query(question)
        print("Answer:", answer)
        print()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
