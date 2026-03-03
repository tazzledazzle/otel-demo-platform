"""Optional integration test: calls local Ollama if OLLAMA_URL is set."""

import os

import pytest

# Skip entire module unless OLLAMA_URL is set
pytestmark = pytest.mark.skipif(
    not os.environ.get("OLLAMA_URL"),
    reason="Set OLLAMA_URL to run integration tests",
)


@pytest.mark.asyncio
async def test_ollama_responds() -> None:
    from config.settings import Settings
    from ai_app.llm.openai_compat import OpenAICompatClient
    from ai_app.llm.base import Message

    url = os.environ.get("OLLAMA_URL", "http://localhost:11434/v1")
    client = OpenAICompatClient(
        base_url=url,
        api_key="placeholder",
        model=os.environ.get("LLM_MODEL", "llama3.2:3b"),
        default_max_tokens=50,
    )
    messages = [Message(role="user", content="Say OK in one word.")]
    reply = await client.generate(messages)
    assert isinstance(reply, str)
    assert len(reply) >= 1
