from __future__ import annotations

from typing import Any, Dict, Optional, Set

from .schemas import NormalizedAlert

_seen_ids: Set[str] = set()


def seen(external_id: str) -> bool:
    return external_id in _seen_ids


def mark_seen(external_id: str) -> None:
    _seen_ids.add(external_id)


def parse_pagerduty(body: Dict[str, Any]) -> Optional[NormalizedAlert]:
    if not isinstance(body, dict):
        return None

    event_action = body.get("event_action")
    payload = body.get("payload") or {}
    dedup_key = body.get("dedup_key") or payload.get("dedup_key")

    if not event_action or not isinstance(payload, dict):
        return None

    external_id = dedup_key or (
        payload.get("custom_details", {}).get("incident_id")
        if isinstance(payload.get("custom_details"), dict)
        else None
    )
    if not external_id:
        return None

    summary = payload.get("summary") or ""
    custom_details = payload.get("custom_details") or {}
    service = custom_details.get("service") or "unknown-service"
    alert_type = custom_details.get("alert_type") or summary or "pagerduty-alert"
    severity = payload.get("severity") or "unknown"

    links_container = payload.get("links") or []
    links = []
    if isinstance(links_container, list):
        for link in links_container:
            href = None
            if isinstance(link, dict):
                href = link.get("href") or link.get("url")
            if isinstance(href, str):
                links.append(href)

    return NormalizedAlert(
        service=service,
        alert_type=alert_type,
        severity=severity,
        source="pagerduty",
        external_id=str(external_id),
        links=links,
        raw=body,
    )


def parse_datadog(body: Dict[str, Any]) -> Optional[NormalizedAlert]:
    if not isinstance(body, dict):
        return None

    external_id = body.get("id")
    title = body.get("title") or ""
    alert_type = body.get("alert_type") or title or "datadog-alert"
    severity = body.get("severity") or "unknown"
    tags = body.get("tags") or []

    if not external_id:
        return None

    service = "unknown-service"
    if isinstance(tags, list):
        for tag in tags:
            if isinstance(tag, str) and tag.startswith("service:"):
                service = tag.split(":", 1)[1] or service
                break

    link = body.get("url") or body.get("link")
    links = [link] if isinstance(link, str) else []

    return NormalizedAlert(
        service=service,
        alert_type=alert_type,
        severity=severity,
        source="datadog",
        external_id=str(external_id),
        links=links,
        raw=body,
    )


def normalize(body: Dict[str, Any]) -> NormalizedAlert:
    pd = parse_pagerduty(body)
    if pd is not None:
        return pd

    dd = parse_datadog(body)
    if dd is not None:
        return dd

    raise ValueError("Unsupported or invalid alert payload")

