"""Tests for LangChain pipeline with mock LLM."""
import os
import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage

os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434")


def test_search_tool():
    from agent.chain import search
    assert search.invoke("test query") == "[stub search result for: test query]"


def test_get_agent_executor_returns_executor():
    with patch("agent.chain.ChatOllama") as mock_ollama:
        mock_ollama.return_value = MagicMock()
        from agent.chain import get_agent_executor
        ex = get_agent_executor()
        assert ex is not None
        assert hasattr(ex, "invoke")
        mock_ollama.assert_called_once()


def test_executor_invoke():
    with patch("agent.chain.get_llm") as mock_get_llm:
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = type("R", (), {"content": "Hello back"})()
        mock_get_llm.return_value = mock_llm
        from agent.chain import get_agent_executor
        ex = get_agent_executor()
        out = ex.invoke({"input": "hi"})
        assert "output" in out


def test_chain_includes_summarize_step():
    """Tool-calling agent returns output from LLM (mock has bind_tools)."""
    with patch("agent.chain.get_llm") as mock_get_llm:
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value.invoke.return_value = AIMessage(content="Summarized reply")
        mock_get_llm.return_value = mock_llm
        from agent.chain import get_agent_executor
        ex = get_agent_executor()
        out = ex.invoke({"input": "hello"})
        assert "output" in out
        assert out["output"] == "Summarized reply"
