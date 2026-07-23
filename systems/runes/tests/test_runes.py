from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from divination_skills.auditable_draw import AuditableDrawError

from systems.runes.engine import draw, explain, items


def golden_cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((Path(__file__).resolve().parent / "golden").glob("*.json"))
    ]


def test_deck_has_24_unique_ordered_symbols() -> None:
    deck = items()
    assert len(deck) == 24
    assert len({item["symbol_id"] for item in deck}) == 24
    assert [item["number"] for item in deck] == list(range(1, 25))


@pytest.mark.parametrize("case", golden_cases(), ids=lambda case: case["case_id"])
def test_golden_draw_replays_exactly(case: dict) -> None:
    result = draw(case["raw_input"])
    assert result["audit"]["draw_id"] == case["expected_output"]["audit"]["draw_id"]
    assert result["computed_facts"] == case["expected_output"]["computed_facts"]


def test_draw_without_replacement_and_generated_seed_replays() -> None:
    first = draw({"spread": "three-rune"})
    symbols = first["computed_facts"]["symbols"]
    assert len({symbol["symbol_id"] for symbol in symbols}) == 3
    replay = draw({"spread": "three-rune", "seed_hex": first["audit"]["seed_hex"]})
    assert replay["computed_facts"] == first["computed_facts"]


def test_report_preserves_facts_and_links_evidence() -> None:
    result = draw({"spread": "three-rune", "seed_hex": "20" * 32})
    original = deepcopy(result["computed_facts"])
    report = explain(result)
    assert result["computed_facts"] == original == report["computed_facts"]
    for statement in [*report["narrative"]["symbols"], report["narrative"]["sequence"]]:
        assert statement["fact_ids"] and statement["rule_ids"]


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "invalid_spread"),
        ({"spread": "five-rune"}, "invalid_spread"),
        ({"spread": "single", "seed_hex": "x" * 64}, "invalid_seed"),
        ({"spread": "single", "allow_reversals": True}, "reversals_unsupported"),
        ({"spread": "single", "question": 42}, "invalid_question"),
    ],
)
def test_invalid_input_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(AuditableDrawError) as captured:
        draw(payload)
    assert captured.value.code == code
