"""Hour-range Bazi candidate scan with training/holdout separation."""

from __future__ import annotations

from datetime import date
from typing import Any

from systems.bazi.calculator.engine import PAIR_RELATIONS, calculate_chart

HOUR_RANGES = (
    ("00:00", "01:00", 0),
    ("01:00", "03:00", 1),
    ("03:00", "05:00", 3),
    ("05:00", "07:00", 5),
    ("07:00", "09:00", 7),
    ("09:00", "11:00", 9),
    ("11:00", "13:00", 11),
    ("13:00", "15:00", 13),
    ("15:00", "17:00", 15),
    ("17:00", "19:00", 17),
    ("19:00", "21:00", 19),
    ("21:00", "23:00", 21),
    ("23:00", "24:00", 23),
)


def _validate_events(events: list[dict[str, Any]]) -> None:
    if len(events) < 5:
        raise ValueError("Rectification requires at least five dated events.")
    splits = {event.get("split") for event in events}
    if not {"training", "holdout"} <= splits:
        raise ValueError("Events must include both training and holdout splits.")
    for event in events:
        if not {
            "event_id",
            "start_date",
            "end_date",
            "split",
        } <= set(event):
            raise ValueError("Each event requires id, date range, and split.")
        start = date.fromisoformat(event["start_date"])
        end = date.fromisoformat(event["end_date"])
        if end < start:
            raise ValueError("Event end_date precedes start_date.")
        if event["split"] not in {"training", "holdout"}:
            raise ValueError("Event split must be training or holdout.")
        if event.get("event_type") == "personality":
            raise ValueError("Soft personality descriptions cannot be rectification events.")
        if not isinstance(event["event_id"], str) or not event["event_id"].strip():
            raise ValueError("event_id must be a non-empty string.")
    event_ids = [event["event_id"] for event in events]
    if len(event_ids) != len(set(event_ids)):
        raise ValueError("event_id values must be unique.")


def _activation_score(candidate: dict[str, Any], event: dict[str, Any], timezone: str) -> int:
    event_chart = calculate_chart(
        {
            "local_datetime": f"{event['start_date']}T12:00:00",
            "timezone": timezone,
            "day_boundary": candidate["normalized_input"]["day_boundary"],
        }
    )
    candidate_branch = candidate["computed_facts"]["pillars"]["hour"]["branch"]["name"]
    score = 0
    for position in ("year", "month", "day"):
        event_branch = event_chart["computed_facts"]["pillars"][position]["branch"]["name"]
        for relation, pairs in PAIR_RELATIONS.items():
            if tuple(sorted((candidate_branch, event_branch))) in {
                tuple(sorted(pair)) for pair in pairs
            }:
                score += {"combine": 1, "harm": 1, "clash": 2}.get(relation, 1)
    return score


def scan_candidates(
    *,
    birth_date: str,
    timezone: str,
    events: list[dict[str, Any]],
    day_boundary: str = "midnight",
) -> dict[str, Any]:
    _validate_events(events)
    parsed_birth = date.fromisoformat(birth_date)
    candidates = []
    for index, (start, end, hour) in enumerate(HOUR_RANGES):
        chart = calculate_chart(
            {
                "local_datetime": f"{parsed_birth.isoformat()}T{hour:02d}:30:00",
                "timezone": timezone,
                "day_boundary": day_boundary,
            }
        )
        scores = {
            split: sum(
                _activation_score(chart, event, timezone)
                for event in events
                if event["split"] == split
            )
            for split in ("training", "holdout")
        }
        candidates.append(
            {
                "candidate_id": f"BAZI-HOUR-{index:02d}",
                "start_local_time": start,
                "end_local_time": end,
                "start_inclusive": True,
                "end_inclusive": False,
                "hour_pillar": (
                    chart["computed_facts"]["pillars"]["hour"]["stem"]["name"]
                    + chart["computed_facts"]["pillars"]["hour"]["branch"]["name"]
                ),
                "training_score": scores["training"],
                "holdout_score": scores["holdout"],
                "fact_ids": [chart["computed_facts"]["pillars"]["hour"]["fact_id"]],
                "rule_ids": ["BAZI-RECTIFIER-HOUR-SCAN-001"],
            }
        )
    candidates.sort(
        key=lambda item: (
            -item["training_score"],
            -item["holdout_score"],
            item["candidate_id"],
        )
    )
    best_training = candidates[0]["training_score"]
    leaders = [item for item in candidates if item["training_score"] == best_training]
    status = (
        "ranked_candidates"
        if len(leaders) == 1
        and leaders[0]["holdout_score"] > 0
        and leaders[0]["holdout_score"]
        >= max(item["holdout_score"] for item in candidates[1:])
        else "underdetermined"
    )
    return {
        "schema_version": "0.2.0",
        "system": "bazi",
        "lineage": "ziping-calculation-baseline",
        "birth_date": birth_date,
        "precision": "double_hour_range",
        "event_date_policy": "start_date_at_local_noon",
        "status": status,
        "candidates": candidates,
        "event_counts": {
            "training": sum(event["split"] == "training" for event in events),
            "holdout": sum(event["split"] == "holdout" for event in events),
        },
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "no_unique_birth_time_claim",
                    "message": (
                        "Scores rank hour ranges only; they cannot establish a unique "
                        "birth minute or prove event causation."
                    ),
                },
                {
                    "code": "personality_tiebreaker_forbidden",
                    "message": "Soft personality descriptions are not used as tie-breakers.",
                },
                {
                    "code": "event_range_start_policy",
                    "message": (
                        "Each event is calculated at local noon on start_date; end_date "
                        "is retained only as uncertainty metadata."
                    ),
                },
            ],
        },
    }
