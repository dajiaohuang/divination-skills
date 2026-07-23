from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.qimen.engine import (
    EARTH_STEMS,
    JU_TABLE,
    QimenError,
    calculate,
    earth_plate,
    explain,
    yuan_from_day_index,
)


def golden_cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((Path(__file__).resolve().parent / "golden").glob("*.json"))
    ]


def test_24_solar_terms_have_three_valid_ju_numbers() -> None:
    assert len(JU_TABLE) == 24
    assert all(
        len(values) == 3 and set(values) <= set(range(1, 10)) for values in JU_TABLE.values()
    )


@pytest.mark.parametrize(
    ("day_index", "name", "head"),
    [(0, "upper", "甲子"), (5, "middle", "己巳"), (10, "lower", "甲戌"), (55, "lower", "己未")],
)
def test_yuan_fu_heads(day_index: int, name: str, head: str) -> None:
    result = yuan_from_day_index(day_index)
    assert result["name"] == name
    assert result["fu_head"] == head


@pytest.mark.parametrize("dun", ["yang", "yin"])
@pytest.mark.parametrize("ju", range(1, 10))
def test_earth_plate_is_a_nine_palace_permutation(dun: str, ju: int) -> None:
    plate = earth_plate(dun, ju)
    assert [item["palace"] for item in plate] == list(range(1, 10))
    assert {item["earth_stem"] for item in plate} == set(EARTH_STEMS)
    assert next(item for item in plate if item["earth_stem"] == "戊")["palace"] == ju


@pytest.mark.parametrize("case", golden_cases(), ids=lambda case: case["case_id"])
def test_golden_case_replays(case: dict) -> None:
    result = calculate(case["raw_input"])
    assert result["computed_facts"] == case["expected_output"]["computed_facts"]


def test_known_solstice_seasons_change_dun() -> None:
    winter = calculate({"local_datetime": "2026-01-10T12:00:00", "timezone": "Asia/Shanghai"})
    summer = calculate({"local_datetime": "2026-07-10T12:00:00", "timezone": "Asia/Shanghai"})
    assert winter["computed_facts"]["dun"] == "yang"
    assert summer["computed_facts"]["dun"] == "yin"


def test_classical_provenance_and_apparent_solar_time_are_explicit() -> None:
    result = calculate(
        {
            "local_datetime": "1999-09-15T19:05:00",
            "timezone": "Asia/Shanghai",
            "time_basis": "apparent_solar",
            "longitude": 119.917,
            "latitude": 31.30,
        }
    )
    assert result["normalized_input"]["time_basis"] == "apparent_solar"
    assert result["normalized_input"]["calculation_datetime"] != "1999-09-15T19:05:00"
    assert result["normalized_input"]["solar_time_correction"]["total_correction_minutes"] != 0
    assert all(
        "SRC-QIMEN-BAOJIAN-001" in palace["source_ids"]
        for palace in result["computed_facts"]["earth_plate"]
    )


def test_report_is_immutable_and_explicitly_incomplete() -> None:
    result = calculate({"local_datetime": "2026-07-23T12:00:00", "timezone": "Asia/Shanghai"})
    original = deepcopy(result["computed_facts"])
    report = explain(result)
    assert result["computed_facts"] == original == report["computed_facts"]
    assert "No heaven" in report["narrative"]["limitations"][0]


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "missing_time"),
        ({"local_datetime": "bad", "timezone": "Asia/Shanghai"}, "invalid_local_datetime"),
        ({"local_datetime": "2026-01-01T00:00:00", "timezone": "Bad/Zone"}, "unknown_timezone"),
        (
            {"local_datetime": "2026-01-01T00:00:00", "timezone": "Asia/Shanghai", "extra": 1},
            "unknown_fields",
        ),
    ],
)
def test_invalid_input_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(QimenError) as captured:
        calculate(payload)
    assert captured.value.code == code
