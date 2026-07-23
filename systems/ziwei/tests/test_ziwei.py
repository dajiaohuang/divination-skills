from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from divination_skills.contracts import canonical_json

from systems.ziwei.engine import ZiweiError, _time_index, calculate, structural_report
from systems.ziwei.star_catalog import BRIGHTNESS_BY_BRANCH


def golden_cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((Path(__file__).resolve().parent / "golden").glob("*.json"))
    ]


@pytest.mark.parametrize(
    ("hour", "expected"),
    [(0, 0), (1, 1), (2, 1), (3, 2), (22, 11), (23, 12)],
)
def test_time_index_boundaries(hour: int, expected: int) -> None:
    assert _time_index(hour) == expected


@pytest.mark.parametrize("case", golden_cases(), ids=lambda case: case["case_id"])
def test_golden_chart_replays(case: dict) -> None:
    result = calculate(case["raw_input"])
    digest = hashlib.sha256(canonical_json(result["computed_facts"])).hexdigest()
    assert digest == case["expected_output"]["computed_facts_sha256"]
    assert len(result["computed_facts"]["palaces"]) == case["expected_output"]["palace_count"]


def test_chart_has_twelve_unique_palaces_and_star_facts() -> None:
    result = calculate(
        {
            "local_datetime": "2000-08-16T03:20:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "female",
        }
    )
    palaces = result["computed_facts"]["palaces"]
    assert len(palaces) == 12
    assert {palace["index"] for palace in palaces} == set(range(12))
    assert len({palace["name"] for palace in palaces}) == 12
    assert all(palace["fact_id"] and palace["source_ids"] for palace in palaces)
    stars = [
        star
        for palace in palaces
        for group in ("majorStars", "minorStars", "adjectiveStars")
        for star in palace[group]
    ]
    assert stars and all(star["fact_id"] and star["source_ids"] for star in stars)


def test_classical_brightness_matrix_has_one_grade_per_possible_placement() -> None:
    assert set(BRIGHTNESS_BY_BRANCH) == set("子丑寅卯辰巳午未申酉戌亥")
    assert all(len(stars) == 20 for stars in BRIGHTNESS_BY_BRANCH.values())
    assert {grade for stars in BRIGHTNESS_BY_BRANCH.values() for grade in stars.values()} == {
        "庙",
        "旺",
        "得",
        "利",
        "平",
        "不",
        "陷",
    }
    assert hashlib.sha256(canonical_json(BRIGHTNESS_BY_BRANCH)).hexdigest() == (
        "17e06cd41036f18b20fdddb7d13a6c63d8f5abc2074a08fd18bcd60b5a0e921f"
    )


def test_report_is_structural_and_immutable() -> None:
    result = calculate(
        {
            "local_datetime": "2026-07-23T12:00:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male",
        }
    )
    original = deepcopy(result["computed_facts"])
    report = structural_report(result)
    assert result["computed_facts"] == original == report["computed_facts"]
    assert "does not assign life-event meanings" in report["narrative"]["structure"]["statement"]


def test_leap_month_label_is_not_duplicated_and_policy_is_explicit() -> None:
    result = calculate(
        {
            "local_datetime": "1982-06-17T11:00:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male",
            "leap_month_policy": "split_after_15",
        }
    )
    assert result["computed_facts"]["lunar_date"] == "1982年闰四月廿六"
    assert result["normalized_input"]["calendar_leap_month"] is True
    assert result["normalized_input"]["effective_lunar_month"] == 5


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "missing_fields"),
        (
            {"local_datetime": "bad", "timezone": "Asia/Shanghai", "calculation_gender": "male"},
            "invalid_local_datetime",
        ),
        (
            {
                "local_datetime": "2026-01-01T00:00:00",
                "timezone": "Bad/Zone",
                "calculation_gender": "male",
            },
            "unknown_timezone",
        ),
        (
            {
                "local_datetime": "2026-01-01T00:00:00",
                "timezone": "Asia/Shanghai",
                "calculation_gender": "other",
            },
            "invalid_calculation_gender",
        ),
        (
            {
                "local_datetime": "1800-01-01T00:00:00",
                "timezone": "Asia/Shanghai",
                "calculation_gender": "female",
            },
            "unsupported_year",
        ),
        (
            {
                "local_datetime": "2026-01-01T00:00:00",
                "timezone": "Asia/Shanghai",
                "calculation_gender": "male",
                "extra": 1,
            },
            "unknown_fields",
        ),
        (
            {
                "local_datetime": "2026-01-01T00:00:00",
                "timezone": "Asia/Shanghai",
                "calculation_gender": "male",
                "time_basis": "apparent_solar",
            },
            "longitude_required",
        ),
        (
            {
                "calendar_type": "lunar",
                "lunar_date": "2026-01-01",
                "is_leap_month": False,
                "time_index": 0,
                "timezone": "Asia/Shanghai",
                "calculation_gender": "male",
                "time_basis": "apparent_solar",
                "longitude": 120.0,
            },
            "solar_time_requires_solar_input",
        ),
    ],
)
def test_invalid_input_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(ZiweiError) as captured:
        calculate(payload)
    assert captured.value.code == code
