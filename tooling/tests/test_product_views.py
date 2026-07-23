from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from divination_skills.product_views import (
    answer_fact_question,
    build_product_view,
    build_timing_view,
)

from systems.bazi.calculator.engine import calculate_chart as calculate_bazi
from systems.bazi.timing import calculate_timing as calculate_bazi_timing
from systems.western_astrology.calculator.engine import (
    calculate_chart as calculate_western,
)
from systems.western_astrology.timing import calculate_timing as calculate_western_timing
from systems.ziwei.engine import calculate as calculate_ziwei
from systems.ziwei.timing import calculate_timing as calculate_ziwei_timing

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def charts() -> dict[str, dict]:
    return {
        "bazi": calculate_bazi(
            {
                "local_datetime": "2000-01-01T12:00:00",
                "timezone": "Asia/Shanghai",
                "luck_cycle_direction": "forward",
            }
        ),
        "western-astrology": calculate_western(
            {
                "local_datetime": "2000-01-01T12:00:00",
                "timezone": "UTC",
                "longitude": 0.0,
                "latitude": 51.4779,
            }
        ),
        "ziwei": calculate_ziwei(
            {
                "local_datetime": "2000-01-01T12:00:00",
                "timezone": "Asia/Shanghai",
                "calculation_gender": "male",
            }
        ),
    }


@pytest.mark.parametrize("system", ["bazi", "western-astrology", "ziwei"])
@pytest.mark.parametrize("view", ["career", "relationship"])
def test_product_views_reuse_existing_facts_and_rules(
    charts: dict[str, dict],
    system: str,
    view: str,
) -> None:
    chart = charts[system]
    original = deepcopy(chart)
    report = build_product_view(system=system, chart=chart, view=view)
    conclusion = report["conclusions"][0]
    assert conclusion["fact_ids"]
    assert conclusion["rule_ids"]
    assert conclusion["source_ids"]
    assert conclusion["support"]
    assert conclusion["counterevidence"]
    assert conclusion["limitations"]
    assert chart == original


def test_high_impact_view_is_downgraded(charts: dict[str, dict]) -> None:
    report = build_product_view(
        system="bazi",
        chart=charts["bazi"],
        view="career",
        high_impact_domain="employment_selection",
    )
    assert report["mode"] == "reflective_information_only"
    assert report["high_impact"]["downgraded"] is True


def test_qa_returns_only_requested_existing_facts(charts: dict[str, dict]) -> None:
    report = answer_fact_question(
        system="western-astrology",
        chart=charts["western-astrology"],
        requested_fact_ids=["western.position.sun", "western.position.not-real"],
    )
    assert report["matched_fact_ids"] == ["western.position.sun"]
    assert report["missing_fact_ids"] == ["western.position.not-real"]
    assert [fact["fact_id"] for fact in report["facts"]] == ["western.position.sun"]


@pytest.mark.parametrize("system", ["bazi", "western-astrology", "ziwei"])
def test_timing_view_reuses_existing_timeline(
    charts: dict[str, dict],
    system: str,
) -> None:
    calculators = {
        "bazi": calculate_bazi_timing,
        "western-astrology": calculate_western_timing,
        "ziwei": calculate_ziwei_timing,
    }
    timing = calculators[system](
        charts[system],
        target_local_datetime="2026-07-23T12:00:00",
        timezone="Asia/Shanghai" if system != "western-astrology" else "UTC",
    )
    original = deepcopy(timing)
    report = build_timing_view(system=system, timing=timing)
    conclusion = report["conclusions"][0]
    assert report["timeline"] == timing["timeline"]
    assert conclusion["fact_ids"]
    assert conclusion["rule_ids"]
    assert conclusion["support"]
    assert conclusion["counterevidence"]
    assert conclusion["limitations"]
    assert timing == original


def test_timing_view_rejects_system_mismatch(charts: dict[str, dict]) -> None:
    timing = calculate_bazi_timing(
        charts["bazi"],
        target_local_datetime="2026-07-23T12:00:00",
        timezone="Asia/Shanghai",
    )
    with pytest.raises(ValueError, match="does not match"):
        build_timing_view(system="ziwei", timing=timing)


def test_product_view_config_declares_required_evidence() -> None:
    config = json.loads(
        (ROOT / "common" / "report-spec" / "PRODUCT_VIEWS.json").read_text(
            encoding="utf-8"
        )
    )
    assert set(config["systems"]) == {"bazi", "western-astrology", "ziwei"}
    assert all(
        {"support", "counterevidence", "limitations"}
        <= set(config["views"][view]["required_evidence"])
        for view in ("career", "relationship", "timing")
    )
