"""Unit tests for LLM layer (mocked)."""

import pytest

from ai_app.llm.base import Message
from ai_app.llm.token_utils import count_tokens, count_message_tokens
from tests.conftest import FakeLLM


@pytest.mark.asyncio
async def test_fake_llm_returns_fixed_string(fake_llm: FakeLLM) -> None:
    messages = [
        Message(role="user", content="Hello"),
    ]
    out = await fake_llm.generate(messages)
    assert out == "Fake assistant reply"
    assert fake_llm.last_messages == messages


@pytest.mark.asyncio
async def test_fake_llm_custom_response() -> None:
    llm = FakeLLM(response="Custom")
    out = await llm.generate([Message(role="user", content="Hi")])
    assert out == "Custom"


def test_count_tokens_basic() -> None:
    n = count_tokens("hello world", model=None)
    assert n >= 1
    assert n <= 10


def test_count_message_tokens() -> None:
    messages = [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}]
    n = count_message_tokens(messages, model=None)
    assert n >= 2
