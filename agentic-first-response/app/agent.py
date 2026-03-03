from .schemas import NormalizedAlert, StubTriageResponse


def run_triage(alert: NormalizedAlert) -> StubTriageResponse:
    return StubTriageResponse(
        hypothesis="Stub: no analysis yet",
        confidence=0.0,
        suggested_action="escalate_to_human",
        risk_level="unknown",
    )

