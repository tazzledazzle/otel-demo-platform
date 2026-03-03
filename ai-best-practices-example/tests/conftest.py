"""Pytest fixtures: fake LLM, temp prompts_dir."""

import tempfile
from pathlib import Path

import pytest

from ai_app.llm.base import BaseLLMClient, Message


class FakeLLM(BaseLLMClient):
    """Returns fixed strings for testing without calling a real API."""

    def __init__(self, response: str = "Fake response") -> None:
        self.response = response
        self.last_messages: list[Message] | None = None

    async def generate(
        self,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs: object,
    ) -> str:
        self.last_messages = list(messages)
        return self.response


@pytest.fixture
def fake_llm() -> FakeLLM:
    return FakeLLM(response="Fake assistant reply")


@pytest.fixture
def prompts_dir(tmp_path: Path) -> Path:
    """Temporary prompts dir with a minimal index and template."""
    (tmp_path / "index.yaml").write_text(
        "chat_system:\n  template: chat_system.jinja2\nrag_qa:\n  template: rag_qa.jinja2\n"
    )
    (tmp_path / "chat_system.jinja2").write_text("You are a test assistant. {{ instructions }}\n")
    (tmp_path / "rag_qa.jinja2").write_text("Context:\n{{ context }}\n\nQuestion: {{ question }}\n\nAnswer:\n")
    return tmp_path
