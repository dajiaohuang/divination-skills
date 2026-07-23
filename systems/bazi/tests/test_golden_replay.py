"""Replay the stored Bazi development set against the current engine."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from systems.bazi.calculator.comparator import sxtwl_modern_reference
from systems.bazi.calculator.engine import calculate_chart

ROOT = Path(__file__).resolve().parent


def load_cases(directory: str) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / directory).glob("*.json"))
    ]


def simple_pillars(chart: dict[str, Any]) -> dict[str, str]:
    return {
        position: pillar["ganzhi"]
        for position, pillar in chart["computed_facts"]["pillars"].items()
    }


@pytest.mark.parametrize("case", load_cases("golden"), ids=lambda case: case["case_id"])
def test_standard_golden_case_replays(case: dict[str, Any]) -> None:
    chart = calculate_chart(case["raw_input"])
    assert simple_pillars(chart) == case["expected_output"]["computed_facts"]["pillars"]


@pytest.mark.parametrize("case", load_cases("edge_cases"), ids=lambda case: case["case_id"])
def test_edge_case_replays(case: dict[str, Any]) -> None:
    chart = calculate_chart(case["raw_input"])
    expected = case["expected_output"]
    if "computed_facts" in expected:
        assert simple_pillars(chart) == expected["computed_facts"]["pillars"]
    if "normalized_input" in expected:
        for key, value in expected["normalized_input"].items():
            assert chart["normalized_input"][key] == value


def test_independent_sxtwl_comparator_agrees_away_from_boundary_dates() -> None:
    cases = load_cases("golden")
    compared = 0
    skipped_boundary_dates: list[str] = []
    for case in cases:
        chart = calculate_chart(case["raw_input"])
        local_date = case["raw_input"]["local_datetime"][:10]
        boundary_dates = {
            chart["computed_facts"]["previous_month_boundary"]["beijing_datetime"][:10],
            chart["computed_facts"]["next_month_boundary"]["beijing_datetime"][:10],
        }
        if local_date in boundary_dates:
            skipped_boundary_dates.append(case["case_id"])
            continue
        assert sxtwl_modern_reference(case["raw_input"]) == simple_pillars(chart)
        compared += 1

    assert compared == len(cases) - 3
    assert skipped_boundary_dates == [
        "CASE-BAZI-STANDARD-001",
        "CASE-BAZI-STANDARD-005",
        "CASE-BAZI-STANDARD-018",
    ]


def _baseline_value(chart: dict[str, Any], field_path: str) -> Any:
    aliases = {
        "computed_facts.day_pillar": chart["computed_facts"]["pillars"]["day"]["ganzhi"],
        "computed_facts.month_pillar": chart["computed_facts"]["pillars"]["month"]["ganzhi"],
    }
    if field_path in aliases:
        return aliases[field_path]
    value: Any = chart
    for part in field_path.split("."):
        value = value[part]
    return value


@pytest.mark.parametrize("case", load_cases("disputes"), ids=lambda case: case["case_id"])
def test_baseline_outcome_is_explicitly_allowed_in_dispute_cases(case: dict[str, Any]) -> None:
    chart = calculate_chart(case["raw_input"])
    for disagreement in case["allowed_disagreements"]:
        assert _baseline_value(chart, disagreement["field_path"]) in disagreement["allowed_values"]
