from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.iching.engine import PAIR_TO_NUMBER, CastError, cast, explain, hexagrams, identify


def golden_cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((Path(__file__).resolve().parent / "golden").glob("*.json"))
    ]


def test_all_64_pairs_and_identifiers_are_unique() -> None:
    assert len(PAIR_TO_NUMBER) == 64
    assert set(PAIR_TO_NUMBER.values()) == set(range(1, 65))
    assert set(hexagrams()) == set(range(1, 65))


def test_hexagram_identity_uses_independent_classical_locators() -> None:
    result = cast({"seed_hex": "00" * 32})
    facts = result["computed_facts"]
    expected = {"SRC-ICHING-LOC-17845", "SRC-ICHING-GUTENBERG-25501"}
    assert set(facts["primary_hexagram"]["source_ids"]) == expected
    assert set(facts["changed_hexagram"]["source_ids"]) == expected
    assert all(line["source_ids"] == ["SRC-ICHING-PROJECT-SPEC-001"] for line in facts["lines"])
    assert result["audit"]["rule_ids"] == ["ICHING-CAST-THREE-COIN-001"]
    assert all("ICHING-CAST-THREE-COIN-001" in line["rule_ids"] for line in facts["lines"])
    assert all(
        "ICHING-CANONICAL-IDENTITY-001" in hexagram["rule_ids"]
        for hexagram in (facts["primary_hexagram"], facts["changed_hexagram"])
    )


@pytest.mark.parametrize(
    ("bits", "number"),
    [
        ([1, 1, 1, 1, 1, 1], 1),
        ([0, 0, 0, 0, 0, 0], 2),
        ([1, 0, 0, 0, 1, 0], 3),
        ([1, 0, 1, 0, 1, 0], 63),
        ([0, 1, 0, 1, 0, 1], 64),
    ],
)
def test_known_line_patterns(bits: list[int], number: int) -> None:
    assert identify(bits)["number"] == number


@pytest.mark.parametrize("case", golden_cases(), ids=lambda case: case["case_id"])
def test_golden_cast_replays(case: dict) -> None:
    result = cast(case["raw_input"])
    assert result["audit"]["cast_id"] == case["expected_output"]["audit"]["cast_id"]
    assert result["computed_facts"] == case["expected_output"]["computed_facts"]


def test_line_values_and_change_are_self_consistent() -> None:
    result = cast({"question": "synthetic", "seed_hex": "30" * 32})
    facts = result["computed_facts"]
    assert all(line["value"] in (6, 7, 8, 9) for line in facts["lines"])
    for line, primary, changed in zip(
        facts["lines"],
        facts["primary_hexagram"]["lines_bottom_to_top"],
        facts["changed_hexagram"]["lines_bottom_to_top"],
        strict=True,
    ):
        assert changed == (1 - primary if line["moving"] else primary)


def test_generated_seed_replays_and_question_is_not_retained() -> None:
    first = cast({"question": "private synthetic wording"})
    replay = cast({"question": "private synthetic wording", "seed_hex": first["audit"]["seed_hex"]})
    assert replay["computed_facts"] == first["computed_facts"]
    assert "private synthetic wording" not in json.dumps(first)


def test_report_is_evidence_linked_and_immutable() -> None:
    result = cast({"seed_hex": "40" * 32})
    original = deepcopy(result["computed_facts"])
    report = explain(result)
    assert result["computed_facts"] == original == report["computed_facts"]
    for section in (report["narrative"]["primary"], report["narrative"]["change"]):
        assert section["fact_ids"] and section["rule_ids"]


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({"extra": 1}, "unknown_fields"),
        ({"seed_hex": "bad"}, "invalid_seed"),
        ({"seed_hex": "z" * 64}, "invalid_seed"),
        ({"question": 1}, "invalid_question"),
    ],
)
def test_invalid_cast_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(CastError) as captured:
        cast(payload)
    assert captured.value.code == code
