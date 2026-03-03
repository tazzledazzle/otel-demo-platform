"""
Decision engine: HTTP POST /decide accepts event + score and returns a decision.
Applies simple rules (event_type and score bands). Extend with more rules or config as needed.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI()


class DecideRequest(BaseModel):
    event: dict[str, Any]
    score: float


def _decide(event: dict[str, Any], score: float) -> dict[str, str]:
    """
    Rules:
    - High score (>= 0.7): offer (e.g. show premium offer).
    - Medium score (0.4–0.7) + purchase/signup: recommend (e.g. cross-sell).
    - Low score (< 0.4): no_op (do nothing).
    - purchase event with any score: always log_high_value (for analytics).
    """
    event_type = event.get("event_type", "")
    if event_type == "purchase":
        return {"action": "log_high_value", "reason": "purchase_event"}
    if score >= 0.7:
        return {"action": "offer", "reason": "high_score"}
    if 0.4 <= score < 0.7 and event_type in ("purchase", "signup"):
        return {"action": "recommend", "reason": "medium_score_conversion"}
    if score < 0.4:
        return {"action": "no_op", "reason": "low_score"}
    return {"action": "no_op", "reason": "default"}


@app.post("/decide")
def decide(req: DecideRequest):
    """Apply rules to event + score and return action and reason."""
    result = _decide(req.event, req.score)
    return result


@app.get("/health")
def health():
    return {"status": "ok"}
