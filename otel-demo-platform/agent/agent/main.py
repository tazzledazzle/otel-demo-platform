"""FastAPI app: POST /invoke for the Kotlin worker."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

from agent.chain import get_agent_executor
from agent.telemetry import setup_telemetry, instrument_app


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
    import uvicorn
    port = int(os.environ.get("AGENT_PORT", "8000"))
    uvicorn.run("agent.main:app", host="0.0.0.0", port=port, reload=False)
