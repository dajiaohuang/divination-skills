from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.numerology.calculator import NumerologyError, calculate_profile
from systems.numerology.core import build_report

ROOT = Path(__file__).resolve().parent


def cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "golden").glob("*.json"))
    ]


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_golden_profiles_replay(case: dict) -> None:
    assert (
        calculate_profile(case["raw_input"])["computed_facts"]
        == case["expected_output"]["computed_facts"]
    )


def test_accents_normalize_without_guessing_transliteration() -> None:
    profile = calculate_profile({"name": "Renée Élise", "birth_date": "1988-11-11"})
    assert profile["normalized_input"]["name_letters"] == "RENEEELISE"
    with pytest.raises(NumerologyError) as captured:
        calculate_profile({"name": "测试名字", "birth_date": "1988-11-11"})
    assert captured.value.code == "transliteration_required"


def test_master_number_is_not_reduced_further() -> None:
    profile = calculate_profile({"name": "Test Person", "birth_date": "2009-09-18"})
    for name, fact in profile["computed_facts"].items():
        if name.endswith("_trace"):
            continue
        if fact["value"] in {11, 22, 33}:
            assert fact["master_number"]


def test_chaldean_profile_exposes_cheiro_sourced_character_trace() -> None:
    profile = calculate_profile(
        {"name": "Robert Example", "birth_date": "1988-11-11", "mapping": "chaldean"}
    )
    trace = profile["computed_facts"]["name_trace"]
    assert [item["value"] for item in trace["letters"][:6]] == [2, 7, 2, 5, 2, 4]
    assert trace["raw_total"] == sum(item["value"] for item in trace["letters"])
    assert "SRC-NUMEROLOGY-CHEIRO-001" in trace["source_ids"]
    assert profile["normalized_input"]["mapping_lineage"] == "chaldean-name-cheiro-v0.3"


def test_report_is_traceable_and_immutable() -> None:
    profile = calculate_profile(cases()[0]["raw_input"])
    original = deepcopy(profile["computed_facts"])
    report = build_report(profile)
    assert report["computed_facts"] == original
    assert profile["computed_facts"] == original
    assert all(item["fact_ids"] and item["rule_ids"] for item in report["narrative"]["numbers"])
    assert all(
        "theme" not in fact for name, fact in original.items() if not name.endswith("_trace")
    )
    assert all(item["theme"] for item in report["derived_findings"])


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "missing_fields"),
        ({"name": "123", "birth_date": "2000-01-01"}, "unsupported_name_script"),
        ({"name": "Rhythms", "birth_date": "2000-01-01"}, "insufficient_name_parts"),
        ({"name": "Example Name", "birth_date": "1800-01-01"}, "date_out_of_range"),
    ],
)
def test_invalid_input_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(NumerologyError) as captured:
        calculate_profile(payload)
    assert captured.value.code == code
