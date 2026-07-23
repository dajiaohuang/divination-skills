from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from divination_skills.auditable_draw import AuditableDrawError

from systems.lenormand.engine import PLAYING_CARDS, draw, explain, items


def golden_cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((Path(__file__).resolve().parent / "golden").glob("*.json"))
    ]


def test_deck_has_36_unique_ordered_symbols() -> None:
    deck = items()
    assert len(deck) == 36
    assert len({item["symbol_id"] for item in deck}) == 36
    assert [item["number"] for item in deck] == list(range(1, 37))


def test_historical_playing_card_correspondences_are_complete_and_traced() -> None:
    assert len(PLAYING_CARDS) == 36
    assert len(set(PLAYING_CARDS)) == 36
    result = draw({"spread": "grand-tableau", "seed_hex": "00" * 32})
    for fact in result["computed_facts"]["symbols"]:
        assert fact["playing_card"] == PLAYING_CARDS[fact["card_number"] - 1]
        assert fact["identity_lineage"] == "game-of-hope-identity-v0.3"
        assert fact["rule_ids"] == ["LENORMAND-CARD-IDENTITY-001"]
        assert "SRC-LENORMAND-BM-HOPE-001" in fact["source_ids"]


@pytest.mark.parametrize("case", golden_cases(), ids=lambda case: case["case_id"])
def test_golden_draw_replays_exactly(case: dict) -> None:
    result = draw(case["raw_input"])
    assert result["audit"]["selection_policy"] == "without_replacement"
    assert result["audit"]["rule_ids"] == ["LENORMAND-DRAW-UNIQUE-001"]
    assert result["audit"]["draw_id"] == case["expected_output"]["audit"]["draw_id"]
    assert result["computed_facts"] == case["expected_output"]["computed_facts"]


def test_draw_without_replacement_and_generated_seed_replays() -> None:
    first = draw({"spread": "nine-card"})
    symbols = first["computed_facts"]["symbols"]
    assert len({symbol["symbol_id"] for symbol in symbols}) == 9
    replay = draw({"spread": "nine-card", "seed_hex": first["audit"]["seed_hex"]})
    assert replay["computed_facts"] == first["computed_facts"]


def test_report_preserves_facts_and_links_evidence() -> None:
    result = draw({"spread": "three-card", "seed_hex": "10" * 32})
    original = deepcopy(result["computed_facts"])
    report = explain(result)
    assert result["computed_facts"] == original == report["computed_facts"]
    for statement in [*report["narrative"]["symbols"], report["narrative"]["sequence"]]:
        assert statement["fact_ids"] and statement["rule_ids"]


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "invalid_spread"),
        ({"spread": "four-card"}, "invalid_spread"),
        ({"spread": "single", "seed_hex": "zz" * 32}, "invalid_seed"),
        ({"spread": "single", "allow_reversals": True}, "reversals_unsupported"),
        ({"spread": "single", "extra": 1}, "unknown_fields"),
    ],
)
def test_invalid_input_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(AuditableDrawError) as captured:
        draw(payload)
    assert captured.value.code == code
