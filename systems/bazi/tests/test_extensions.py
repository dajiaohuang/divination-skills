from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from divination_skills.contracts import canonical_json
from jsonschema import Draft202012Validator, FormatChecker

from systems.bazi.calculator.engine import calculate_chart
from systems.bazi.reader import read_structured
from systems.bazi.rectifier import scan_candidates
from systems.bazi.synastry import compare_charts
from systems.bazi.timing import calculate_timing
from systems.bazi.validator import compare_chart

ROOT = Path(__file__).resolve().parents[3]


def _chart(
    local_datetime: str = "2000-01-01T12:00:00",
    direction: str = "forward",
) -> dict:
    return calculate_chart(
        {
            "local_datetime": local_datetime,
            "timezone": "Asia/Shanghai",
            "day_boundary": "midnight",
            "luck_cycle_direction": direction,
        }
    )


def _events() -> list[dict[str, str]]:
    return [
        {
            "event_id": f"event-{index}",
            "start_date": f"{2010 + index:04d}-06-01",
            "end_date": f"{2010 + index:04d}-06-30",
            "split": "training" if index < 4 else "holdout",
        }
        for index in range(5)
    ]


def test_reader_accepts_json_and_four_pillar_text() -> None:
    chart = _chart()
    imported = read_structured(json.dumps(chart, ensure_ascii=False))
    assert imported["native_facts_overwritten"] is False
    symbols = [
        chart["computed_facts"]["pillars"][position]["stem"]["name"]
        + chart["computed_facts"]["pillars"][position]["branch"]["name"]
        for position in ("year", "month", "day", "hour")
    ]
    text = read_structured(" ".join(symbols), format="four_pillar_text")
    assert set(text["imported_chart"]["computed_facts"]["pillars"]) == {
        "year",
        "month",
        "day",
        "hour",
    }
    with pytest.raises(ValueError):
        read_structured("甲子 乙丑", format="four_pillar_text")
    with pytest.raises(ValueError, match="exactly four"):
        read_structured(
            "命盘是 " + " ".join(symbols),
            format="four_pillar_text",
        )


def test_validator_reports_differences_without_mutation() -> None:
    chart = _chart()
    original = deepcopy(chart)
    assert compare_chart(chart, chart)["status"] == "match"
    imported = deepcopy(chart)
    imported["computed_facts"]["pillars"]["hour"]["branch"]["name"] = "子"
    report = compare_chart(chart, imported)
    assert report["status"] == "different"
    assert report["native_chart_unchanged"] is True
    assert chart == original


def test_timing_is_deterministic_and_uses_shared_timeline() -> None:
    chart = _chart()
    kwargs = {
        "target_local_datetime": "2026-07-23T12:00:00",
        "timezone": "Asia/Shanghai",
    }
    first = calculate_timing(chart, **kwargs)
    second = calculate_timing(chart, **kwargs)
    assert canonical_json(first) == canonical_json(second)
    schema = json.loads(
        (ROOT / "common" / "schemas" / "timeline.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(first["timeline"])
    assert first["active_luck_cycle"] is not None
    assert set(first["period_pillars"]) == {"year", "month"}
    assert first["validation"]["status"] == "valid"
    year_entry = next(
        entry for entry in first["timeline"]["entries"] if entry["scope"] == "year"
    )
    month_entry = next(
        entry for entry in first["timeline"]["entries"] if entry["scope"] == "month"
    )
    assert year_entry["start"] == "2026-02-03T20:02:08+00:00"
    assert year_entry["end"] == "2027-02-04T01:46:18+00:00"
    assert month_entry["start"] != "2026-07-01T00:00:00+08:00"


def test_timing_requires_explicit_luck_direction() -> None:
    chart = calculate_chart(
        {
            "local_datetime": "2000-01-01T12:00:00",
            "timezone": "Asia/Shanghai",
        }
    )
    with pytest.raises(ValueError, match="luck-cycle direction"):
        calculate_timing(
            chart,
            target_local_datetime="2026-07-23T12:00:00",
            timezone="Asia/Shanghai",
        )


def test_synastry_keeps_directional_and_symmetric_facts_separate() -> None:
    chart_a = _chart("2000-01-01T12:00:00", "forward")
    chart_b = _chart("2001-02-03T14:00:00", "reverse")
    report = compare_charts(chart_a, chart_b)
    assert len(report["directional"]["A_to_B"]) == 4
    assert len(report["directional"]["B_to_A"]) == 4
    assert all(
        item["direction"] == "A_to_B" for item in report["directional"]["A_to_B"]
    )
    assert all(
        item["direction"] == "B_to_A" for item in report["directional"]["B_to_A"]
    )
    assert report["chart_refs"]["A"] != report["chart_refs"]["B"]
    assert report["validation"]["status"] == "valid"


def test_rectifier_requires_five_events_and_holdout() -> None:
    with pytest.raises(ValueError, match="at least five"):
        scan_candidates(
            birth_date="2000-01-01",
            timezone="Asia/Shanghai",
            events=_events()[:4],
        )
    no_holdout = [{**event, "split": "training"} for event in _events()]
    with pytest.raises(ValueError, match="holdout"):
        scan_candidates(
            birth_date="2000-01-01",
            timezone="Asia/Shanghai",
            events=no_holdout,
        )
    personality = _events()
    personality[0]["event_type"] = "personality"
    with pytest.raises(ValueError, match="personality"):
        scan_candidates(
            birth_date="2000-01-01",
            timezone="Asia/Shanghai",
            events=personality,
        )
    duplicate = _events()
    duplicate[1]["event_id"] = duplicate[0]["event_id"]
    with pytest.raises(ValueError, match="unique"):
        scan_candidates(
            birth_date="2000-01-01",
            timezone="Asia/Shanghai",
            events=duplicate,
        )


def test_rectifier_returns_ranked_ranges_never_a_unique_minute() -> None:
    report = scan_candidates(
        birth_date="2000-01-01",
        timezone="Asia/Shanghai",
        events=_events(),
    )
    assert report["event_date_policy"] == "start_date_at_local_noon"
    assert any(
        warning["code"] == "event_range_start_policy"
        for warning in report["validation"]["warnings"]
    )
    assert report["status"] in {"ranked_candidates", "underdetermined"}
    assert len(report["candidates"]) == 13
    assert report["precision"] == "double_hour_range"
    assert all("birth_minute" not in candidate for candidate in report["candidates"])
    assert report["event_counts"] == {"training": 4, "holdout": 1}
    assert {
        warning["code"] for warning in report["validation"]["warnings"]
    } >= {"no_unique_birth_time_claim", "personality_tiebreaker_forbidden"}
