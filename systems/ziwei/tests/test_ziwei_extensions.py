from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from divination_skills.contracts import canonical_json
from jsonschema import Draft202012Validator, FormatChecker

from systems.ziwei.analyzer import (
    find_star,
    is_empty_palace,
    palace,
    palace_stem_transformation_paths,
    surrounded_palaces,
    transformation_paths,
)
from systems.ziwei.core import analyze_core
from systems.ziwei.engine import LINEAGE, ZiweiError, calculate
from systems.ziwei.reader import read_and_compare, read_structured
from systems.ziwei.star_catalog import STAR_METADATA
from systems.ziwei.timing import calculate_timing
from systems.ziwei.validator import compare_chart

ROOT = Path(__file__).resolve().parents[3]
CASE_ROOT = Path(__file__).resolve().parent


def _chart() -> dict:
    return calculate(
        {
            "local_datetime": "2000-08-16T03:20:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "female",
        }
    )


def _case_files(folder: str) -> list[Path]:
    return sorted((CASE_ROOT / folder).glob("CASE-ZIWEI-*.json"))


@pytest.mark.parametrize("path", _case_files("edge_cases"), ids=lambda path: path.stem)
def test_boundary_case_replays(path: Path) -> None:
    case = json.loads(path.read_text(encoding="utf-8"))
    result = calculate(case["raw_input"])
    actual = hashlib.sha256(canonical_json(result["computed_facts"])).hexdigest()
    assert actual == case["expected_output"]["computed_facts_sha256"]


@pytest.mark.parametrize("path", _case_files("disputes"), ids=lambda path: path.stem)
def test_dispute_case_replays(path: Path) -> None:
    case = json.loads(path.read_text(encoding="utf-8"))
    result = calculate(case["raw_input"])
    actual = hashlib.sha256(canonical_json(result["computed_facts"])).hexdigest()
    assert actual == case["expected_output"]["computed_facts_sha256"]


def test_solar_and_lunar_inputs_replay_same_chart() -> None:
    solar = calculate(
        {
            "local_datetime": "2026-07-23T11:00:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male",
        }
    )
    lunar = calculate(
        {
            "calendar_type": "lunar",
            "lunar_date": "2026-06-10",
            "is_leap_month": False,
            "time_index": 6,
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male",
        }
    )
    assert solar["computed_facts"] == lunar["computed_facts"]


def test_late_zi_policy_is_explicit_and_changes_basis() -> None:
    common = {
        "local_datetime": "2026-07-23T23:30:00",
        "timezone": "Asia/Shanghai",
        "calculation_gender": "male",
    }
    current = calculate({**common, "late_zi_policy": "current_day"})
    following = calculate({**common, "late_zi_policy": "next_day"})
    assert (
        current["normalized_input"]["local_datetime"]
        == following["normalized_input"]["local_datetime"]
    )
    assert current["computed_facts"]["solar_date"] != following["computed_facts"]["solar_date"]


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("calendar_type", "other", "invalid_calendar_type"),
        ("late_zi_policy", "other", "invalid_late_zi_policy"),
        ("year_boundary", "other", "invalid_year_boundary"),
        ("leap_month_policy", "other", "invalid_leap_month_policy"),
    ],
)
def test_invalid_policy_fails_closed(field: str, value: str, code: str) -> None:
    payload = {
        "local_datetime": "2026-07-23T12:00:00",
        "timezone": "Asia/Shanghai",
        "calculation_gender": "male",
        field: value,
    }
    with pytest.raises(ZiweiError) as captured:
        calculate(payload)
    assert captured.value.code == code


def test_every_catalogued_star_has_a_direct_placement_case() -> None:
    observed: set[str] = set()
    for path in _case_files("golden"):
        case = json.loads(path.read_text(encoding="utf-8"))
        observed.update(
            key.split(":", 1)[1] for key in case["expected_intermediate"]["star_placements"]
        )
    assert set(STAR_METADATA) <= observed


def test_every_catalogued_star_has_a_direct_known_position_assertion() -> None:
    chart = calculate(
        {
            "local_datetime": "1900-02-04T00:17:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male",
        }
    )
    expected = {
        "紫微": 0,
        "天机": 11,
        "太阳": 9,
        "武曲": 8,
        "天同": 7,
        "廉贞": 4,
        "天府": 0,
        "太阴": 1,
        "贪狼": 2,
        "巨门": 3,
        "天相": 4,
        "天梁": 5,
        "七杀": 6,
        "破军": 10,
        "文昌": 8,
        "文曲": 2,
        "左辅": 2,
        "右弼": 8,
        "天魁": 11,
        "天钺": 5,
        "禄存": 6,
        "擎羊": 7,
        "陀罗": 5,
        "天马": 0,
        "火星": 0,
        "铃星": 8,
        "地劫": 9,
        "地空": 9,
        "天刑": 7,
        "天姚": 11,
        "三台": 6,
        "八座": 4,
        "天哭": 4,
        "天虚": 4,
        "龙池": 2,
        "凤阁": 8,
        "台辅": 4,
        "封诰": 0,
        "红鸾": 1,
        "天喜": 7,
        "天德": 7,
        "月德": 3,
        "年解": 8,
        "解神": 6,
        "天伤": 5,
        "天使": 7,
        "恩光": 11,
        "天贵": 5,
        "孤辰": 0,
        "寡宿": 8,
        "天才": 0,
        "天寿": 0,
        "天厨": 0,
        "蜚廉": 6,
        "破碎": 3,
        "天官": 9,
        "天福": 4,
        "天空": 11,
        "截空": 4,
        "旬空": 2,
        "阴煞": 0,
        "天月": 8,
        "天巫": 3,
    }
    actual = {}
    for item in chart["computed_facts"]["palaces"]:
        for group in ("majorStars", "minorStars", "auxiliaryStars"):
            for star in item[group]:
                if star["name"] in STAR_METADATA:
                    actual[star["name"]] = item["index"]
    assert expected == actual


def test_palace_queries_are_exhaustive_and_stable() -> None:
    chart = _chart()
    for index in range(12):
        item = palace(chart, index)
        query = surrounded_palaces(chart, index)
        expected = {index, (index + 4) % 12, (index + 6) % 12, (index + 8) % 12}
        assert {value["index"] for value in query["palaces"].values()} == expected
        assert palace(chart, item["name"]) == item
        assert palace(chart, item["earthlyBranch"]) == item
        assert isinstance(is_empty_palace(chart, index)["is_empty_major_palace"], bool)


def test_star_and_transformation_queries_trace_to_facts() -> None:
    chart = _chart()
    assert len(find_star(chart, "紫微")) == 1
    paths = transformation_paths(chart)
    palace_paths = palace_stem_transformation_paths(chart)
    assert paths
    assert palace_paths
    valid_star_ids = {
        star["fact_id"]
        for item in chart["computed_facts"]["palaces"]
        for group in ("majorStars", "minorStars", "auxiliaryStars")
        for star in item[group]
    }
    assert all(path["target_star_fact_id"] in valid_star_ids for path in paths)
    assert all(path["target_star_fact_id"] in valid_star_ids for path in palace_paths)
    assert all(path["origin_palace_fact_id"] for path in palace_paths)


def test_timing_is_repeatable_and_matches_shared_timeline_schema() -> None:
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
    assert set(first["layers"]) == {
        "decadal",
        "minor_limit",
        "annual",
        "monthly",
        "daily",
        "hourly",
    }
    assert all(
        path["origin_palace_fact_id"] and path["target_palace_fact_id"]
        for layer in first["layers"].values()
        for path in layer["transformations"]
    )
    assert all(
        len(layer["flow_stars"]) == 4
        and all(star["palace_fact_id"] for star in layer["flow_stars"])
        for layer in first["layers"].values()
    )
    year_entry = next(
        entry for entry in first["timeline"]["entries"] if entry["scope"] == "year"
    )
    month_entry = next(
        entry for entry in first["timeline"]["entries"] if entry["scope"] == "month"
    )
    assert year_entry["start"] == "2026-02-17T00:00:00+08:00"
    assert year_entry["end"] == "2027-02-06T00:00:00+08:00"
    assert month_entry["start"] == "2026-07-14T00:00:00+08:00"
    assert month_entry["end"] == "2026-08-13T00:00:00+08:00"


def test_timing_boundaries_change_only_at_declared_boundary() -> None:
    chart = _chart()
    before = calculate_timing(
        chart,
        target_local_datetime="2026-07-23T22:59:59",
        timezone="Asia/Shanghai",
    )
    after = calculate_timing(
        chart,
        target_local_datetime="2026-07-23T23:00:00",
        timezone="Asia/Shanghai",
    )
    assert before["layers"]["daily"]["palace_index"] == after["layers"]["daily"]["palace_index"]
    assert before["layers"]["hourly"]["palace_index"] != after["layers"]["hourly"]["palace_index"]


def test_day_and_month_boundaries_are_explicit() -> None:
    chart = _chart()
    day_before = calculate_timing(
        chart,
        target_local_datetime="2026-02-16T23:59:59",
        timezone="Asia/Shanghai",
    )
    day_after = calculate_timing(
        chart,
        target_local_datetime="2026-02-17T00:00:00",
        timezone="Asia/Shanghai",
    )
    assert (
        day_before["layers"]["daily"]["palace_index"]
        != day_after["layers"]["daily"]["palace_index"]
    )
    assert (
        day_before["layers"]["monthly"]["palace_index"]
        != day_after["layers"]["monthly"]["palace_index"]
    )
    assert day_before["timeline"]["entries"] != day_after["timeline"]["entries"]


def test_decadal_boundary_changes_at_nominal_year_boundary() -> None:
    chart = _chart()
    current = next(
        item for item in chart["computed_facts"]["palaces"] if item["decadal"]["start_age"] > 1
    )
    birth_year = int(chart["computed_facts"]["solar_date"][:4])
    boundary_year = birth_year + current["decadal"]["start_age"] - 1
    before = calculate_timing(
        chart,
        target_local_datetime=f"{boundary_year - 1:04d}-12-31T23:59:59",
        timezone="Asia/Shanghai",
    )
    after = calculate_timing(
        chart,
        target_local_datetime=f"{boundary_year:04d}-01-01T00:00:00",
        timezone="Asia/Shanghai",
    )
    assert before["layers"]["decadal"]["palace_index"] != after["layers"]["decadal"]["palace_index"]


def test_reader_and_validator_never_overwrite_native_facts() -> None:
    chart = _chart()
    original = deepcopy(chart)
    read = read_and_compare(json.dumps(chart, ensure_ascii=False), chart)
    assert read["comparison"]["status"] == "match"
    assert read["native_facts_overwritten"] is False
    assert chart == original
    modified = deepcopy(chart)
    modified["computed_facts"]["palaces"][0]["name"] = "changed"
    comparison = compare_chart(chart, modified)
    assert comparison["status"] == "different"
    assert comparison["native_chart_unchanged"] is True
    with pytest.raises(ValueError):
        read_structured("not json")


def test_validator_reports_brightness_self_transformation_and_time_basis_paths() -> None:
    chart = _chart()
    modified = deepcopy(chart)
    star = next(
        star
        for palace in modified["computed_facts"]["palaces"]
        for group in ("majorStars", "minorStars", "auxiliaryStars")
        for star in palace[group]
        if star["brightness"] is not None and star["self_transformations"]
    )
    star["brightness"] = "changed"
    star["self_transformations"] = []
    modified["normalized_input"]["time_basis"] = "apparent_solar"

    comparison = compare_chart(chart, modified)
    classifications = {item["classification"] for item in comparison["differences"]}
    assert "brightness_difference" in classifications
    assert "self_transformation_difference" in classifications
    assert "time_basis_difference" in classifications


def test_core_is_experimental_cited_and_non_mutating() -> None:
    chart = _chart()
    original = deepcopy(chart)
    report = analyze_core(chart, locale="en")
    assert report["status"] == "experimental"
    assert len(report["findings"]) == 12
    assert chart == original
    assert all(
        finding["fact_ids"] and finding["rule_ids"] and finding["source_ids"]
        for finding in report["findings"]
    )
    assert report["validation"]["citation_completeness"] == 1.0
    assert report["validation"]["fact_reference_validity"] == 1.0
    assert report["lineage"] == LINEAGE
