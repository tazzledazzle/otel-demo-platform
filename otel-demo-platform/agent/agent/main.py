"""FastAPI app: POST /invoke for the Kotlin worker."""
import os
import socket
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

from agent.chain import get_agent_executor
from agent.telemetry import setup_telemetry, instrument_app


def _port_available(host: str, port: int) -> bool:
    """Return True if the port can be bound (not in use)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


class InvokeRequest(BaseModel):
    message: str


class InvokeResponse(BaseModel):
    reply: str


def create_app(agent=None) -> FastAPI:
    """Create FastAPI app. Pass agent= for testing to skip real LLM."""
    otlp = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    if otlp:
        setup_telemetry("otel-demo-agent", otlp)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.agent = agent if agent is not None else get_agent_executor()
        yield
        app.state.agent = None

    app = FastAPI(title="OTel Demo Agent", lifespan=lifespan)
    instrument_app(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/invoke", response_model=InvokeResponse)
    def invoke(req: InvokeRequest):
        agent_obj = app.state.agent
        result = agent_obj.invoke({"input": req.message})
        reply = result.get("output", str(result))
        return InvokeResponse(reply=reply)

    return app


app = create_app()

if __name__ == "__main__":
    import sys
    import uvicorn
    agent_port_env = os.environ.get("AGENT_PORT")
    if agent_port_env:
        try:
            port = int(agent_port_env)
        except ValueError:
            port = 8000
    else:
        port = 8000
    host = "0.0.0.0"
    if agent_port_env is None and not _port_available(host, 8000):
        sys.stderr.write(
            "Agent could not bind to port 8000. Set AGENT_PORT to a different port or stop the other process.\n"
        )
        sys.exit(1)
    uvicorn.run("agent.main:app", host=host, port=port, reload=False)
