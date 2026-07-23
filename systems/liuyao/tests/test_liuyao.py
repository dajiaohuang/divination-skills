from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.liuyao.engine import (
    BRANCH_ELEMENT,
    NAJIA,
    PALACE_SEQUENCES,
    LiuyaoError,
    calculate,
    explain,
    palace_for,
    six_relative,
    void_branches,
)


def golden_cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((Path(__file__).resolve().parent / "golden").glob("*.json"))
    ]


def test_eight_palaces_cover_every_hexagram_once() -> None:
    numbers = [number for sequence in PALACE_SEQUENCES.values() for number in sequence]
    assert len(numbers) == 64
    assert set(numbers) == set(range(1, 65))
    assert len(numbers) == len(set(numbers))


def test_known_palace_and_shiying_stages() -> None:
    assert palace_for(1) == ("qian", 0)
    assert palace_for(44) == ("qian", 1)
    assert palace_for(35) == ("qian", 6)
    assert palace_for(14) == ("qian", 7)


def test_najia_tables_have_six_valid_assignments_per_trigram() -> None:
    for table in NAJIA.values():
        values = [*table["inner"], *table["outer"]]
        assert len(values) == 6
        assert all(len(value) == 2 and value[1] in BRANCH_ELEMENT for value in values)


def test_six_relatives_cover_five_element_relations() -> None:
    assert six_relative("wood", "wood") == "兄弟"
    assert six_relative("wood", "water") == "父母"
    assert six_relative("wood", "fire") == "子孙"
    assert six_relative("wood", "earth") == "妻财"
    assert six_relative("wood", "metal") == "官鬼"


@pytest.mark.parametrize(
    ("day_index", "expected"),
    [
        (0, ["戌", "亥"]),
        (10, ["申", "酉"]),
        (20, ["午", "未"]),
        (30, ["辰", "巳"]),
        (40, ["寅", "卯"]),
        (50, ["子", "丑"]),
    ],
)
def test_void_branches_for_six_xun(day_index: int, expected: list[str]) -> None:
    assert void_branches(day_index) == expected


@pytest.mark.parametrize("case", golden_cases(), ids=lambda case: case["case_id"])
def test_golden_case_replays(case: dict) -> None:
    result = calculate(case["raw_input"])
    assert result["audit"]["cast_id"] == case["expected_output"]["audit"]["cast_id"]
    assert result["computed_facts"] == case["expected_output"]["computed_facts"]


def test_calculation_has_six_lines_and_one_shi_ying() -> None:
    result = calculate(
        {
            "seed_hex": "50" * 32,
            "local_datetime": "2026-07-23T12:00:00",
            "timezone": "Asia/Shanghai",
        }
    )
    lines = result["computed_facts"]["lines"]
    assert len(lines) == 6
    assert [line["role"] for line in lines].count("shi") == 1
    assert [line["role"] for line in lines].count("ying") == 1
    assert all(line["six_relative"] and line["six_spirit"] for line in lines)


def test_classical_provenance_and_apparent_solar_time_are_explicit() -> None:
    result = calculate(
        {
            "seed_hex": "51" * 32,
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
        "SRC-LIUYAO-ZENGSHAN-001" in line["source_ids"]
        for line in result["computed_facts"]["lines"]
    )
    assert result["computed_facts"]["calendar_context"]["six_spirit_start"]["first_spirit"]


def test_report_preserves_facts_and_marks_structural_boundary() -> None:
    result = calculate(
        {
            "seed_hex": "60" * 32,
            "local_datetime": "2026-07-23T12:00:00",
            "timezone": "Asia/Shanghai",
        }
    )
    original = deepcopy(result["computed_facts"])
    report = explain(result)
    assert result["computed_facts"] == original == report["computed_facts"]
    assert "does not select 用神" in report["narrative"]["limitations"][0]


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "missing_time"),
        (
            {"local_datetime": "2026-01-01T00:00:00", "timezone": "Asia/Shanghai", "extra": 1},
            "unknown_fields",
        ),
        ({"local_datetime": "bad", "timezone": "Asia/Shanghai"}, "invalid_local_datetime"),
        ({"local_datetime": "2026-01-01T00:00:00", "timezone": "Bad/Zone"}, "unknown_timezone"),
        (
            {
                "local_datetime": "2026-01-01T00:00:00",
                "timezone": "Asia/Shanghai",
                "seed_hex": "bad",
            },
            "invalid_seed",
        ),
    ],
)
def test_invalid_input_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(LiuyaoError) as captured:
        calculate(payload)
    assert captured.value.code == code
