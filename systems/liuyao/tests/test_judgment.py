from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.liuyao.engine import calculate
from systems.liuyao.judgment import QUESTION_PACKS, analyze

ROOT = Path(__file__).resolve().parent


def cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "extension_cases" / "judgment").glob("*.json"))
    ]


def _summary(result: dict) -> dict:
    return {
        "status": result["status"],
        "candidate_line_fact_ids": result["use_deity"]["candidate_line_fact_ids"],
        "line_strength": result["line_strength"],
        "moving_changes": result["moving_changes"],
        "timing_pack": result["timing_pack"],
    }


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_judgment_cases_replay(case: dict) -> None:
    chart = calculate(case["raw_input"])
    original = deepcopy(chart)
    result = analyze(chart, **case["arguments"])
    assert _summary(result) == case["expected_output"]
    assert chart == original


def test_all_question_packs_are_explicit_and_timing_is_opt_in() -> None:
    chart = calculate(
        {
            "seed_hex": "12" * 32,
            "local_datetime": "2026-07-23T12:00:00",
            "timezone": "Asia/Shanghai",
        }
    )
    for category in QUESTION_PACKS:
        result = analyze(chart, question_category=category)
        assert result["question_category"] == category
        assert result["timing_pack"]["enabled"] is False
        assert result["timing_pack"]["candidates"] == []


def test_expert_queue_has_fifty_unaccepted_candidates() -> None:
    queue = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "evaluations"
            / "judgment_expert_candidates.json"
        ).read_text(encoding="utf-8")
    )
    assert queue["candidate_count"] == len(queue["candidates"]) == 50
    assert queue["status"] == "pending_expert_review"
    assert all(
        item["accepted"] is False
        and item["review"]["decision"] == "pending"
        and item["review"]["reviewer_id"] is None
        for item in queue["candidates"]
    )


def test_invalid_category_fails_closed() -> None:
    chart = calculate(
        {
            "seed_hex": "34" * 32,
            "local_datetime": "2026-07-23T12:00:00",
            "timezone": "Asia/Shanghai",
        }
    )
    with pytest.raises(ValueError, match="question_category"):
        analyze(chart, question_category="unregistered")
