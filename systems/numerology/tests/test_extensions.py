from __future__ import annotations

import json
from pathlib import Path

import pytest

from systems.numerology.calculator import (
    CHALDEAN_VALUES,
    NumerologyError,
    calculate_profile,
)
from systems.numerology.core import build_report

ROOT = Path(__file__).resolve().parent / "extension_cases"


def cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "chaldean").glob("*.json"))
    ]


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_chaldean_cases_replay(case: dict) -> None:
    result = calculate_profile(case["raw_input"])
    assert {
        "normalized_input": result["normalized_input"],
        "computed_facts": result["computed_facts"],
    } == case["expected_output"]
    assert build_report(result)["narrative"]["numbers"]


def test_chaldean_mapping_covers_alphabet_without_nine() -> None:
    assert set(CHALDEAN_VALUES) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert set(CHALDEAN_VALUES.values()) == set(range(1, 9))
    profile = calculate_profile(
        {
            "name": "Example Name",
            "birth_date": "2000-01-01",
            "mapping": "chaldean",
        }
    )
    assert profile["normalized_input"]["masters"] == []
    assert all(fact["master_number"] is False for fact in profile["computed_facts"].values())


def test_non_latin_requires_explicit_complete_transliteration() -> None:
    with pytest.raises(NumerologyError) as missing:
        calculate_profile(
            {"name": "张 Wei", "birth_date": "2000-01-01", "mapping": "chaldean"}
        )
    assert missing.value.code == "transliteration_required"
    result = calculate_profile(
        {
            "name": "张 Wei",
            "transliteration": "Zhang Wei",
            "birth_date": "2000-01-01",
            "mapping": "chaldean",
        }
    )
    assert result["normalized_input"]["name_letters"] == "ZHANGWEI"
    assert (
        result["normalized_input"]["transliteration_policy"]
        == "user_supplied_latin_transliteration-v0.2"
    )


def test_mapping_case_gates() -> None:
    assert len(list((ROOT / "chaldean").glob("*.json"))) == 50
    disputes = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "mapping_disputes").glob("*.json"))
    ]
    assert len(disputes) == 20
    assert all(
        item["expected_handling"] == "separate_lineage_or_fail_closed"
        for item in disputes
    )


def test_invalid_mapping_and_unexpected_transliteration_fail_closed() -> None:
    with pytest.raises(NumerologyError) as invalid:
        calculate_profile(
            {"name": "Example Name", "birth_date": "2000-01-01", "mapping": "mixed"}
        )
    assert invalid.value.code == "invalid_mapping"
    with pytest.raises(NumerologyError) as unexpected:
        calculate_profile(
            {
                "name": "Example Name",
                "transliteration": "Example Name",
                "birth_date": "2000-01-01",
            }
        )
    assert unexpected.value.code == "unexpected_transliteration"
