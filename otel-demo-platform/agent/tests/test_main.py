"""Tests for FastAPI app."""
import json
import os
import re
os.environ.pop("OTEL_EXPORTER_OTLP_ENDPOINT", None)

import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {"output": "Echo: hello"}
    from agent.main import create_app
    app = create_app(agent=mock_agent)
    app.state.agent = mock_agent  # set before first request (lifespan may run async)
    return TestClient(app)


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_invoke_returns_reply(client: TestClient):
    r = client.post("/invoke", json={"message": "hello"})
    assert r.status_code == 200
    data = r.json()
    assert "reply" in data
    assert "Echo:" in data["reply"]


def test_invoke_structured_log_trace_id_span_id_are_hex_strings(client: TestClient, capsys: pytest.CaptureFixture):
    """Structured logs must emit trace_id and span_id as strings (hex), not integers."""
    client.post("/invoke", json={"message": "hello"})
    captured = capsys.readouterr()
    stderr = captured.err
    hex_32 = re.compile(r"^[0-9a-f]{32}$")
    hex_16 = re.compile(r"^[0-9a-f]{16}$")
    for line in stderr.strip().split("\n"):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "trace_id" not in obj or "span_id" not in obj:
            continue
        assert isinstance(obj["trace_id"], str), f"trace_id must be string, got {type(obj['trace_id'])}"
        assert isinstance(obj["span_id"], str), f"span_id must be string, got {type(obj['span_id'])}"
        if obj["trace_id"]:
            assert hex_32.match(obj["trace_id"]), f"trace_id must be 32 hex chars, got {obj['trace_id']!r}"
        if obj["span_id"]:
            assert hex_16.match(obj["span_id"]), f"span_id must be 16 hex chars, got {obj['span_id']!r}"


def test_invoke_agent_error_propagates(client: TestClient):
    """When the agent raises, the exception propagates (server would return 500)."""
    client.app.state.agent.invoke.side_effect = RuntimeError("Agent failed")
    with pytest.raises(RuntimeError, match="Agent failed"):
        client.post("/invoke", json={"message": "hello"})
