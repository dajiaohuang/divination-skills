from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from divination_skills.contracts import canonical_json
from jsonschema import Draft202012Validator, FormatChecker

from systems.western_astrology.calculator.engine import calculate_chart
from systems.western_astrology.reader import read_structured
from systems.western_astrology.rectifier import scan_candidates
from systems.western_astrology.synastry import compare_charts
from systems.western_astrology.timing import calculate_timing
from systems.western_astrology.validator import compare_chart

ROOT = Path(__file__).resolve().parents[3]


def _chart(local_datetime: str = "2000-01-01T12:00:00") -> dict:
    return calculate_chart(
        {
            "local_datetime": local_datetime,
            "timezone": "UTC",
            "longitude": 0.0,
            "latitude": 51.4779,
            "house_system": "whole_sign",
        }
    )


def _events() -> list[dict[str, str]]:
    return [
        {
            "event_id": f"event-{index}",
            "start_date": f"{2010 + index:04d}-06-01",
            "end_date": f"{2010 + index:04d}-06-30",
            "event_type": "dated_event",
            "evidence_quality": "documented" if index % 2 == 0 else "reported",
            "split": "training" if index < 4 else "holdout",
        }
        for index in range(5)
    ]


def test_reader_accepts_json_and_csv() -> None:
    chart = _chart()
    json_import = read_structured(json.dumps(chart))
    assert json_import["native_facts_overwritten"] is False
    csv_import = read_structured(
        "body,longitude_degrees,house\nsun,280.0,10\nmoon,220.0,8\n",
        format="csv",
    )
    assert len(csv_import["imported_chart"]["computed_facts"]["positions"]) == 2
    with pytest.raises(ValueError, match="requires body"):
        read_structured("name,degree\nsun,10\n", format="csv")
    with pytest.raises(ValueError, match="unique"):
        read_structured(
            "body,longitude_degrees\nsun,10\nsun,20\n",
            format="csv",
        )
    with pytest.raises(ValueError, match="outside 1–12"):
        read_structured(
            "body,longitude_degrees,house\nsun,10,13\n",
            format="csv",
        )


def test_validator_uses_tolerance_and_preserves_native() -> None:
    chart = _chart()
    original = deepcopy(chart)
    assert compare_chart(chart, chart)["status"] == "match"
    imported = deepcopy(chart)
    imported["computed_facts"]["positions"][0]["longitude_degrees"] += 0.02
    report = compare_chart(chart, imported, longitude_tolerance_degrees=0.01)
    assert report["status"] == "different"
    assert report["differences"][0]["classification"] == "position_difference"
    assert chart == original


def test_timing_replays_and_validates_shared_timeline() -> None:
    chart = _chart()
    kwargs = {
        "target_local_datetime": "2026-07-23T12:00:00",
        "timezone": "UTC",
    }
    first = calculate_timing(chart, **kwargs)
    second = calculate_timing(chart, **kwargs)
    assert canonical_json(first) == canonical_json(second)
    schema = json.loads(
        (ROOT / "common" / "schemas" / "timeline.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(first["timeline"])
    assert {
        entry["scope"] for entry in first["timeline"]["entries"]
    } == {"transit", "return"}
    assert first["transit_to_natal_aspects"]
    assert first["validation"]["status"] == "valid"


def test_solar_return_matches_natal_sun_longitude() -> None:
    chart = _chart()
    result = calculate_timing(
        chart,
        target_local_datetime="2026-07-23T12:00:00",
        timezone="UTC",
    )
    natal_sun = next(
        item for item in chart["computed_facts"]["positions"] if item["body"] == "sun"
    )
    return_sun = next(
        item
        for item in result["solar_return"]["chart"]["computed_facts"]["positions"]
        if item["body"] == "sun"
    )
    delta = abs(
        (
            return_sun["longitude_degrees"]
            - natal_sun["longitude_degrees"]
            + 180
        )
        % 360
        - 180
    )
    assert delta < 1e-5


def test_synastry_has_directional_overlays_and_symmetric_aspects() -> None:
    chart_a = _chart("2000-01-01T12:00:00")
    chart_b = _chart("2001-02-03T14:00:00")
    report = compare_charts(chart_a, chart_b)
    assert len(report["directional"]["A_to_B"]) == 10
    assert len(report["directional"]["B_to_A"]) == 10
    assert report["symmetric"]
    assert all(
        fact["direction"] == "A_to_B"
        for fact in report["directional"]["A_to_B"]
    )
    assert report["chart_refs"]["A"] != report["chart_refs"]["B"]


def test_rectifier_requires_hard_events_and_holdout() -> None:
    with pytest.raises(ValueError, match="at least five"):
        scan_candidates(
            birth_date="2000-01-01",
            timezone="UTC",
            longitude=0.0,
            latitude=51.4779,
            events=_events()[:4],
            interval_minutes=60,
        )
    personality = _events()
    personality[0] = {**personality[0], "event_type": "personality"}
    with pytest.raises(ValueError, match="personality"):
        scan_candidates(
            birth_date="2000-01-01",
            timezone="UTC",
            longitude=0.0,
            latitude=51.4779,
            events=personality,
            interval_minutes=60,
        )
    invalid_split = _events()
    invalid_split[0]["split"] = "test"
    with pytest.raises(ValueError, match="split"):
        scan_candidates(
            birth_date="2000-01-01",
            timezone="UTC",
            longitude=0.0,
            latitude=51.4779,
            events=invalid_split,
            interval_minutes=60,
        )
    duplicate = _events()
    duplicate[1]["event_id"] = duplicate[0]["event_id"]
    with pytest.raises(ValueError, match="unique"):
        scan_candidates(
            birth_date="2000-01-01",
            timezone="UTC",
            longitude=0.0,
            latitude=51.4779,
            events=duplicate,
            interval_minutes=60,
        )


def test_rectifier_returns_intervals_and_no_unique_minute() -> None:
    report = scan_candidates(
        birth_date="2000-01-01",
        timezone="UTC",
        longitude=0.0,
        latitude=51.4779,
        events=_events(),
        interval_minutes=60,
    )
    assert report["event_date_policy"] == "start_date_at_local_noon"
    assert any(
        warning["code"] == "event_range_start_policy"
        for warning in report["validation"]["warnings"]
    )
    assert report["status"] in {"ranked_candidates", "underdetermined"}
    assert len(report["candidates"]) == 24
    assert report["precision"] == "60_minute_range"
    assert report["event_counts"] == {"training": 4, "holdout": 1}
    assert all("birth_minute" not in item for item in report["candidates"])
