from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .agent import run_triage
from .schemas import NormalizedAlert, StubTriageResponse
from .webhook import mark_seen, normalize, seen


app = FastAPI(title="Agentic First Response Triage Service")


@app.get("/")
def root() -> Dict[str, str]:
    return {"service": "agentic-first-response", "docs": "/docs"}


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "triage-agent"}


@app.post("/webhook/alert", response_model=StubTriageResponse)
def webhook_alert(body: Dict[str, Any]) -> StubTriageResponse:
    try:
        alert: NormalizedAlert = normalize(body)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail="Unsupported or invalid alert payload",
        ) from exc

    if seen(alert.external_id):
        # Idempotent behavior: return the same stub response without re-processing.
        return StubTriageResponse(
            hypothesis="Stub: no analysis yet",
            confidence=0.0,
            suggested_action="escalate_to_human",
            risk_level="unknown",
        )

    response = run_triage(alert)
    mark_seen(alert.external_id)
    return response

