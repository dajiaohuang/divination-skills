from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from systems.western_astrology.calculator import AstrologyError, calculate_chart
from systems.western_astrology.calculator.engine import traditional_condition
from systems.western_astrology.core import build_report

SYSTEM = Path(__file__).resolve().parents[1]


def cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((Path(__file__).resolve().parent / "golden").glob("*.json"))
    ]


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_golden_natal_chart_replays(case: dict) -> None:
    chart = calculate_chart(case["raw_input"])
    assert chart["computed_facts"] == case["expected_output"]["computed_facts"]


def test_j2000_positions_pin_engine_reference_values() -> None:
    chart = calculate_chart(cases()[0]["raw_input"])
    positions = {item["body"]: item for item in chart["computed_facts"]["positions"]}
    assert positions["sun"]["longitude_degrees"] == pytest.approx(280.36873864, abs=1e-8)
    assert positions["moon"]["longitude_degrees"] == pytest.approx(223.32389113, abs=1e-8)
    assert positions["mars"]["longitude_degrees"] == pytest.approx(327.96389908, abs=1e-8)


def test_traditional_conditions_are_unscored_and_exclude_outer_planets() -> None:
    assert traditional_condition("sun", "Aries")["statuses"] == ["exaltation"]
    assert traditional_condition("sun", "Libra")["statuses"] == ["fall"]
    assert traditional_condition("saturn", "Libra")["statuses"] == ["exaltation"]
    assert traditional_condition("saturn", "Aries")["statuses"] == ["fall"]
    assert traditional_condition("uranus", "Aquarius") is None
    chart = calculate_chart(cases()[0]["raw_input"])
    positions = {item["body"]: item for item in chart["computed_facts"]["positions"]}
    assert "traditional_condition" in positions["sun"]
    assert positions["sun"]["traditional_condition"]["scoring_applied"] is False
    assert "SRC-WESTERN-PTOLEMY-001" in positions["sun"]["traditional_condition"]["source_ids"]
    assert "traditional_condition" not in positions["uranus"]


def test_house_cusps_are_exactly_thirty_degrees_apart() -> None:
    for case in cases():
        chart = calculate_chart(case["raw_input"])
        cusps = chart["computed_facts"]["house_cusps"]
        for left, right in zip(cusps, [*cusps[1:], cusps[0]], strict=True):
            assert (right["longitude_degrees"] - left["longitude_degrees"]) % 360 == pytest.approx(
                30
            )


def test_whole_sign_and_equal_houses_are_explicitly_different() -> None:
    payload = cases()[0]["raw_input"]
    whole = calculate_chart({**payload, "house_system": "whole_sign"})
    equal = calculate_chart({**payload, "house_system": "equal"})
    assert whole["computed_facts"]["house_cusps"][0]["longitude_degrees"] == 0
    assert equal["computed_facts"]["house_cusps"][0]["longitude_degrees"] == pytest.approx(
        equal["computed_facts"]["angles"]["ascendant"]["longitude_degrees"]
    )


def test_aspects_are_unique_and_within_configured_orb() -> None:
    chart = calculate_chart(cases()[0]["raw_input"])
    pairs = set()
    for aspect in chart["computed_facts"]["aspects"]:
        pair = tuple(sorted((aspect["body_a"], aspect["body_b"])))
        assert pair not in pairs
        pairs.add(pair)
        assert aspect["orb_degrees"] <= aspect["allowed_orb_degrees"]


def test_report_preserves_computed_facts_and_links_statements() -> None:
    chart = calculate_chart(cases()[0]["raw_input"])
    original = deepcopy(chart["computed_facts"])
    report = build_report(chart)
    assert chart["computed_facts"] == original
    assert report["computed_facts"] == original
    explanations = [
        *report["narrative"]["angles"],
        *report["narrative"]["placements"],
        *report["narrative"]["aspects"],
    ]
    assert explanations
    assert all(item["fact_ids"] and item["rule_ids"] for item in explanations)


def test_output_contract_schema() -> None:
    schema = json.loads((SYSTEM / "calculator" / "output.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(calculate_chart(cases()[0]["raw_input"]))


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "missing_local_datetime"),
        (
            {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "longitude": 0},
            "missing_latitude",
        ),
        (
            {
                "local_datetime": "2024-01-01T00:00:00",
                "timezone": "UTC",
                "longitude": 181,
                "latitude": 0,
            },
            "invalid_longitude",
        ),
        (
            {
                "local_datetime": "2024-01-01T00:00:00",
                "timezone": "UTC",
                "longitude": 0,
                "latitude": 0,
                "house_system": "placidus",
            },
            "invalid_house_system",
        ),
        (
            {
                "local_datetime": "2024-03-10T02:30:00",
                "timezone": "America/New_York",
                "longitude": -74,
                "latitude": 40.7,
            },
            "nonexistent_local_time",
        ),
    ],
)
def test_invalid_input_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(AstrologyError) as captured:
        calculate_chart(payload)
    assert captured.value.code == code
