from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.qimen.full_chart import (
    DOOR_ELEMENT,
    ELEMENT_CONTROLS,
    HEAVEN_TOMB_PALACE_BY_STEM,
    PALACE_ELEMENT,
    calculate_full,
)

ROOT = Path(__file__).resolve().parent / "extension_cases"


def replay_cases() -> list[dict]:
    paths = [*(ROOT / "full").glob("*.json"), *(ROOT / "boundaries").glob("*.json")]
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(paths)]


def summary(result: dict) -> dict:
    return {
        "rotation": result["rotation"],
        "void_branches": result["void_branches"],
        "palaces": result["palaces"],
    }


@pytest.mark.parametrize("case", replay_cases(), ids=lambda case: case["case_id"])
def test_full_chart_cases_replay(case: dict) -> None:
    assert summary(calculate_full(case["raw_input"])) == case["expected_output"]


def test_full_plate_is_a_complete_bounded_permutation() -> None:
    result = calculate_full(
        {"local_datetime": "2026-07-23T12:00:00", "timezone": "Asia/Shanghai"}
    )
    palaces = result["palaces"]
    assert [item["palace"] for item in palaces] == list(range(1, 10))
    assert sum(len(item["heaven_stems"]) for item in palaces) == 9
    assert sum(len(item["stars"]) for item in palaces) == 9
    assert sum(len(item["doors"]) for item in palaces) == 8
    assert sum(len(item["spirits"]) for item in palaces) == 8
    assert sum(item["is_void"] for item in palaces) >= 1
    assert all(item["fact_id"] and item["rule_ids"] for item in palaces)


def test_foundation_is_retained_without_mutation() -> None:
    result = calculate_full(
        {"local_datetime": "2026-01-10T12:00:00", "timezone": "Asia/Shanghai"}
    )
    original = deepcopy(result["foundation"]["computed_facts"])
    assert result["foundation"]["computed_facts"] == original
    assert "infer direction" in result["conclusions"][0]["statement"]


def test_state_markers_follow_declared_classical_direction() -> None:
    for case in replay_cases():
        result = calculate_full(case["raw_input"])
        for palace in result["palaces"]:
            for marker in palace["tomb_entries"]:
                assert marker["layer"] == "heaven"
                assert HEAVEN_TOMB_PALACE_BY_STEM[marker["stem"]] == palace["palace"]
            for marker in palace["door_oppressions"]:
                assert (
                    ELEMENT_CONTROLS[PALACE_ELEMENT[palace["palace"]]]
                    == DOOR_ELEMENT[marker["door"]]
                )


def test_duty_door_center_landing_is_disclosed_and_hosted_in_kun() -> None:
    center_case = next(
        result
        for case in replay_cases()
        if (result := calculate_full(case["raw_input"]))["rotation"][
            "duty_door_logical_palace"
        ]
        == 5
    )
    assert center_case["rotation"]["duty_door_target_palace"] == 2
    duty_doors = [
        (palace["palace"], door)
        for palace in center_case["palaces"]
        for door in palace["doors"]
        if door["duty"]
    ]
    assert len(duty_doors) == 1
    assert duty_doors[0][0] == 2


def test_case_gate_counts() -> None:
    assert len(list((ROOT / "full").glob("*.json"))) == 50
    assert len(list((ROOT / "boundaries").glob("*.json"))) == 30
    disputes = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "disputes").glob("*.json"))
    ]
    assert len(disputes) == 20
    assert all(
        item["expected_decision"] == "lineage_mismatch_requires_separate_calculator"
        for item in disputes
    )
