"""
Model service: HTTP POST /score accepts an event (or features) and returns a numeric score.
Uses a simple deterministic stub so scores are reproducible for the tutorial.
Replace with a real model (e.g. sklearn, ONNX) for production.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI()

# Stub scoring: different event types get different score bands (0–1)
EVENT_TYPE_BASE: dict[str, float] = {
    "click": 0.3,
    "view": 0.2,
    "purchase": 0.9,
    "signup": 0.7,
}


class ScoreRequest(BaseModel):
    event: dict[str, Any]


def _score_event(event: dict[str, Any]) -> float:
    """Compute a deterministic score from event (stub)."""
    base = EVENT_TYPE_BASE.get(event.get("event_type", ""), 0.2)
    payload = event.get("payload") or {}
    # Slight variation from payload count so we see different scores
    count = payload.get("count", 0)
    jitter = (count % 10) / 100.0
    score = min(1.0, base + jitter)
    return round(score, 4)


@app.post("/score")
def score(req: ScoreRequest):
    """Return a numeric score in [0, 1] for the given event."""
    s = _score_event(req.event)
    return {"score": s}


@app.get("/health")
def health():
    return {"status": "ok"}
