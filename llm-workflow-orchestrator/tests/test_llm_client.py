"""Tests for LLM client abstraction."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from llm_workflow_orchestrator.llm.client import LLMClient


@pytest.mark.asyncio
async def test_complete_returns_content_from_openai_compatible_api() -> None:
    """Complete sends messages and returns assistant content."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Hello, world!"
    mock_response.choices[0].message.tool_calls = None

    with patch("llm_workflow_orchestrator.llm.client.AsyncOpenAI") as mock_cls:
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_cls.return_value = mock_client

        client = LLMClient(base_url="https://api.openai.com/v1", api_key="sk-test", model="gpt-4o-mini")
        result = await client.complete("Say hello")

    assert result.content == "Hello, world!"
    assert result.tool_calls is None
    mock_client.chat.completions.create.assert_called_once()
    call_kw = mock_client.chat.completions.create.call_args[1]
    assert call_kw["model"] == "gpt-4o-mini"
    assert [m["content"] for m in call_kw["messages"]] == ["Say hello"]


@pytest.mark.asyncio
async def test_complete_with_system_message_and_tools() -> None:
    """Complete accepts system message and tool definitions."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = None
    tool_call = MagicMock()
    tool_call.id = "tc_1"
    tool_call.function.name = "get_weather"
    tool_call.function.arguments = '{"q":"weather"}'
    mock_response.choices[0].message.tool_calls = [tool_call]

    with patch("llm_workflow_orchestrator.llm.client.AsyncOpenAI") as mock_cls:
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_cls.return_value = mock_client

        client = LLMClient(base_url="https://api.example.com", api_key="key", model="gpt-4o")
        result = await client.complete(
            "What's the weather?",
            system_message="You are a helpful assistant.",
            tools=[{"type": "function", "function": {"name": "get_weather", "description": "Get weather"}}],
        )

    assert result.tool_calls is not None
    assert len(result.tool_calls) == 1
    assert result.tool_calls[0]["name"] == "get_weather"
    assert result.tool_calls[0]["arguments"] == '{"q":"weather"}'
    call_kw = mock_client.chat.completions.create.call_args[1]
    assert call_kw["messages"][0]["role"] == "system"
    assert call_kw["messages"][0]["content"] == "You are a helpful assistant."
    assert "tools" in call_kw
