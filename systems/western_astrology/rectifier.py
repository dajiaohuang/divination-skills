"""Event-retained Western birth-time candidate scanner."""

from __future__ import annotations

from datetime import date
from typing import Any

from systems.western_astrology.calculator.engine import calculate_chart


def _validate_events(events: list[dict[str, Any]]) -> None:
    if len(events) < 5:
        raise ValueError("Rectification requires at least five dated events.")
    if not {"training", "holdout"} <= {event.get("split") for event in events}:
        raise ValueError("Events must include both training and holdout splits.")
    for event in events:
        required = {"event_id", "start_date", "end_date", "split", "evidence_quality"}
        if not required <= set(event):
            raise ValueError("Each event requires id, date range, split, and evidence quality.")
        if event["evidence_quality"] not in {"documented", "reported"}:
            raise ValueError("evidence_quality must be documented or reported.")
        if event.get("event_type") == "personality":
            raise ValueError("Soft personality descriptions cannot be rectification events.")
        if date.fromisoformat(event["end_date"]) < date.fromisoformat(event["start_date"]):
            raise ValueError("Event end_date precedes start_date.")


def _event_charts(
    events: list[dict[str, Any]],
    *,
    timezone: str,
    longitude: float,
    latitude: float,
) -> dict[str, dict[str, Any]]:
    return {
        event["event_id"]: calculate_chart(
            {
                "local_datetime": f"{event['start_date']}T12:00:00",
                "timezone": timezone,
                "longitude": longitude,
                "latitude": latitude,
                "house_system": "whole_sign",
            }
        )
        for event in events
    }


def _score(candidate: dict[str, Any], event_chart: dict[str, Any]) -> int:
    angles = [
        candidate["computed_facts"]["angles"]["ascendant"]["longitude_degrees"],
        candidate["computed_facts"]["angles"]["midheaven"]["longitude_degrees"],
    ]
    score = 0
    for moving in event_chart["computed_facts"]["positions"]:
        for angle in angles:
            separation = abs((moving["longitude_degrees"] - angle + 180) % 360 - 180)
            distance = min(
                abs(separation),
                abs(abs(separation) - 90),
                abs(abs(separation) - 180),
            )
            if distance <= 3:
                score += 3 if distance <= 1 else 1
    return score


def scan_candidates(
    *,
    birth_date: str,
    timezone: str,
    longitude: float,
    latitude: float,
    events: list[dict[str, Any]],
    interval_minutes: int = 30,
) -> dict[str, Any]:
    _validate_events(events)
    if interval_minutes not in {15, 30, 60}:
        raise ValueError("interval_minutes must be 15, 30, or 60.")
    parsed_birth = date.fromisoformat(birth_date)
    event_charts = _event_charts(
        events,
        timezone=timezone,
        longitude=longitude,
        latitude=latitude,
    )
    candidates = []
    for minute_of_day in range(0, 24 * 60, interval_minutes):
        hour, minute = divmod(minute_of_day, 60)
        chart = calculate_chart(
            {
                "local_datetime": (
                    f"{parsed_birth.isoformat()}T{hour:02d}:{minute:02d}:00"
                ),
                "timezone": timezone,
                "longitude": longitude,
                "latitude": latitude,
                "house_system": "whole_sign",
            }
        )
        scores = {
            split: sum(
                _score(chart, event_charts[event["event_id"]])
                for event in events
                if event["split"] == split
            )
            for split in ("training", "holdout")
        }
        end_minutes = minute_of_day + interval_minutes
        end_hour, end_minute = divmod(end_minutes, 60)
        candidates.append(
            {
                "candidate_id": f"WESTERN-TIME-{minute_of_day:04d}",
                "start_local_time": f"{hour:02d}:{minute:02d}",
                "end_local_time": (
                    "24:00"
                    if end_minutes == 24 * 60
                    else f"{end_hour:02d}:{end_minute:02d}"
                ),
                "start_inclusive": True,
                "end_inclusive": False,
                "training_score": scores["training"],
                "holdout_score": scores["holdout"],
                "angle_fact_ids": [
                    chart["computed_facts"]["angles"]["ascendant"]["fact_id"],
                    chart["computed_facts"]["angles"]["midheaven"]["fact_id"],
                ],
                "rule_ids": ["WESTERN-RECTIFIER-EVENT-SCAN-001"],
            }
        )
    candidates.sort(
        key=lambda item: (
            -item["training_score"],
            -item["holdout_score"],
            item["candidate_id"],
        )
    )
    top = candidates[0]
    leaders = [
        candidate
        for candidate in candidates
        if candidate["training_score"] == top["training_score"]
    ]
    status = (
        "ranked_candidates"
        if len(leaders) == 1
        and top["holdout_score"] > 0
        and top["holdout_score"]
        >= max(item["holdout_score"] for item in candidates[1:])
        else "underdetermined"
    )
    return {
        "schema_version": "0.2.0",
        "system": "western-astrology",
        "lineage": "western-event-retained-rectification-v0.2",
        "status": status,
        "birth_date": birth_date,
        "precision": f"{interval_minutes}_minute_range",
        "event_counts": {
            "training": sum(event["split"] == "training" for event in events),
            "holdout": sum(event["split"] == "holdout" for event in events),
        },
        "candidates": candidates,
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "no_unique_birth_time_claim",
                    "message": (
                        "The scan ranks retained intervals and cannot prove a unique "
                        "birth minute."
                    ),
                },
                {
                    "code": "personality_tiebreaker_forbidden",
                    "message": "Soft personality descriptions cannot break a hard-event tie.",
                },
            ],
        },
    }
