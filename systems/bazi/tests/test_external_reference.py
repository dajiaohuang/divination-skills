from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from systems.bazi.calculator.engine import calculate_chart

CASE = Path(__file__).resolve().parent / "external_references" / "CASE-BAZI-USER-001.json"


def _load_case() -> dict:
    return json.loads(CASE.read_text(encoding="utf-8"))


def test_user_reference_matches_bazi_pillars_ten_gods_and_relations() -> None:
    case = _load_case()
    expected = case["expected"]
    chart = calculate_chart(case["input"])
    facts = chart["computed_facts"]

    assert {
        position: pillar["ganzhi"] for position, pillar in facts["pillars"].items()
    } == expected["pillars"]
    assert facts["day_master"]["name"] == expected["day_master"]
    assert facts["ten_gods"]["visible"] == expected["visible_ten_gods"]
    assert {
        position: labels[0]["ten_god"] for position, labels in facts["ten_gods"]["hidden"].items()
    } == expected["primary_hidden_ten_gods"]
    assert {
        position: value["name"] for position, value in facts["nayin"]["by_pillar"].items()
    } == expected["nayin_by_pillar"]
    assert facts["growth_stages"]["day_master_by_pillar"] == expected["day_master_growth_stages"]
    assert facts["growth_stages"]["pillar_self"] == expected["self_growth_stages"]
    assert facts["seasonal_element_states"]["states"] == expected["seasonal_element_states"]
    assert facts["visible_element_counts"]["counts"] == expected["visible_element_counts"]
    assert [
        {
            "type": relation["type"],
            "positions": relation["positions"],
            "branches": relation["branches"],
        }
        for relation in facts["branch_relations"]
    ] == expected["relations"]


def test_user_reference_luck_cycle_sequence_and_display_year_agree() -> None:
    case = _load_case()
    expected = case["expected"]
    chart = calculate_chart(case["input"])
    luck = chart["computed_facts"]["luck_cycles"]
    assert luck is not None

    assert luck["start_age_years"] == pytest.approx(
        expected["luck_cycle_start_age_years"], abs=0.000001
    )
    prefix_count = case["comparison_policy"]["luck_cycle_prefix_count"]
    assert [cycle["pillar"]["ganzhi"] for cycle in luck["cycles"]] == expected[
        "luck_cycle_pillars"
    ][:prefix_count]

    birth = datetime.fromisoformat(chart["normalized_input"]["local_datetime"])
    approximate_start = birth + timedelta(days=luck["start_age_years"] * 365.2425)
    assert approximate_start.year == expected["luck_cycle_display_start_year"]
    assert chart["computed_facts"]["next_month_boundary"]["beijing_datetime"].startswith(
        "1999-10-09"
    )


def test_reported_true_solar_time_is_not_silently_recalculated() -> None:
    case = _load_case()
    chart = calculate_chart(case["input"])
    assert chart["normalized_input"]["true_solar_time_applied"] is False
    assert {warning["code"] for warning in chart["validation"]["warnings"]} == {
        "coordinates_not_applied"
    }


def test_noaa_apparent_solar_time_from_civil_input_preserves_external_pillars() -> None:
    case = _load_case()
    chart = calculate_chart(
        {
            **case["input"],
            "local_datetime": "1999-09-15T19:05:00",
            "time_basis": "apparent_solar",
        }
    )
    assert chart["normalized_input"]["true_solar_time_applied"] is True
    assert chart["normalized_input"]["calculation_datetime"].startswith("1999-09-15T19:09:")
    assert {
        position: pillar["ganzhi"]
        for position, pillar in chart["computed_facts"]["pillars"].items()
    } == case["expected"]["pillars"]
