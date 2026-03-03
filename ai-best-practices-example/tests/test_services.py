"""Unit tests for ChatService and RAGService (with fake LLM)."""

from pathlib import Path

import pytest

from ai_app.llm.base import Message
from ai_app.services.chat import ChatService
from ai_app.services.rag import RAGService
from tests.conftest import FakeLLM


@pytest.mark.asyncio
async def test_chat_service_returns_llm_reply(fake_llm: FakeLLM, prompts_dir: Path) -> None:
    service = ChatService(fake_llm, prompts_dir)
    reply = await service.chat("Hello")
    assert reply == "Fake assistant reply"
    assert fake_llm.last_messages is not None
    roles = [m.role for m in fake_llm.last_messages]
    assert "system" in roles
    assert "user" in roles


@pytest.mark.asyncio
async def test_chat_messages(fake_llm: FakeLLM, prompts_dir: Path) -> None:
    service = ChatService(fake_llm, prompts_dir)
    messages = [
        Message(role="system", content="You are helpful."),
        Message(role="user", content="Hi"),
    ]
    reply = await service.chat_messages(messages)
    assert reply == "Fake assistant reply"
    assert fake_llm.last_messages == messages


def test_rag_ingest_requires_embedding_client(prompts_dir: Path) -> None:
    fake = FakeLLM(response="RAG answer")
    service = RAGService(fake, prompts_dir, embedding_client=None)
    with pytest.raises(RuntimeError, match="embedding_client"):
        service.ingest(["doc1"])
