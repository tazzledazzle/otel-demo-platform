"""Tests for FastAPI app."""
import os
os.environ.pop("OTEL_EXPORTER_OTLP_ENDPOINT", None)

import pytest
from unittest.mock import MagicMock, patch
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
