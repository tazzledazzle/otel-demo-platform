"""Tests for Temporal activities."""

import pytest
from unittest.mock import AsyncMock, patch

from llm_workflow_orchestrator.activities.call_llm import call_llm
from llm_workflow_orchestrator.activities.call_tool import call_tool
from llm_workflow_orchestrator.llm.client import LLMResponse


@pytest.mark.asyncio
async def test_call_llm_returns_content() -> None:
    """call_llm calls LLM and returns content."""
    with patch("llm_workflow_orchestrator.activities.call_llm._get_client") as mock_get:
        mock_client = AsyncMock()
        mock_client.complete = AsyncMock(return_value=LLMResponse(content="Hi there", tool_calls=None))
        mock_get.return_value = mock_client

        result = await call_llm("Hello")

    assert result["content"] == "Hi there"
    assert result["tool_calls"] is None
    mock_client.complete.assert_called_once_with("Hello", system_message=None, tools=None)


@pytest.mark.asyncio
async def test_call_llm_with_system_and_tools() -> None:
    """call_llm forwards system_message and tools."""
    with patch("llm_workflow_orchestrator.activities.call_llm._get_client") as mock_get:
        mock_client = AsyncMock()
        mock_client.complete = AsyncMock(
            return_value=LLMResponse(content=None, tool_calls=[{"name": "search", "arguments": "{}"}])
        )
        mock_get.return_value = mock_client

        result = await call_llm(
            "Search for X",
            system_message="You are a search assistant.",
            tools=[{"type": "function", "function": {"name": "search"}}],
        )

    assert result["tool_calls"] == [{"name": "search", "arguments": "{}"}]
    mock_client.complete.assert_called_once_with(
        "Search for X",
        system_message="You are a search assistant.",
        tools=[{"type": "function", "function": {"name": "search"}}],
    )


@pytest.mark.asyncio
async def test_call_tool_echo_returns_argument() -> None:
    """call_tool with echo returns arguments as result."""
    result = await call_tool("echo", '{"msg": "hi"}')
    assert result["result"] == '{"msg": "hi"}'


@pytest.mark.asyncio
async def test_call_tool_unknown_returns_not_implemented() -> None:
    """call_tool with unknown tool returns not_implemented."""
    result = await call_tool("unknown_tool", "{}")
    assert result["tool"] == "unknown_tool"
    assert result["result"] == "not_implemented"
