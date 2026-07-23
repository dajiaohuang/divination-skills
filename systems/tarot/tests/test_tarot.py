from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from systems.tarot.core import build_report
from systems.tarot.draw.engine import DrawError, draw_cards, load_deck

SYSTEM = Path(__file__).resolve().parents[1]


def golden_cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((Path(__file__).resolve().parent / "golden").glob("*.json"))
    ]


def test_deck_has_78_unique_schema_valid_cards() -> None:
    deck = load_deck()
    schema = json.loads((SYSTEM / "data" / "deck.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(deck)
    assert len(deck["cards"]) == 78
    assert len({card["card_id"] for card in deck["cards"]}) == 78
    assert [card["index"] for card in deck["cards"]] == list(range(78))


def test_rws_identity_is_complete_and_source_traced() -> None:
    draw = draw_cards({"spread": "celtic-cross", "seed_hex": "00" * 32})
    for fact in draw["computed_facts"]["cards"]:
        assert fact["deck_index"] == fact["card_index"]
        assert fact["identity_lineage"] == "rws-identity-v0.3"
        assert fact["rule_ids"] == ["TAROT-CARD-IDENTITY-001"]
        assert "SRC-TAROT-WAITE-WIKISOURCE-001" in fact["source_ids"]
        if fact["arcana"] == "major":
            assert fact["suit"] is None and fact["element"] is None
        else:
            assert fact["suit"] and fact["rank"] and fact["element"]


@pytest.mark.parametrize("case", golden_cases(), ids=lambda case: case["case_id"])
def test_golden_draw_replays_exactly(case: dict) -> None:
    draw = draw_cards(case["raw_input"])
    assert draw["audit"]["draw_id"] == case["expected_output"]["audit"]["draw_id"]
    assert draw["computed_facts"] == case["expected_output"]["computed_facts"]


def test_draw_is_without_replacement_and_reversals_can_be_disabled() -> None:
    draw = draw_cards(
        {
            "spread": "situation-challenge-guidance",
            "seed_hex": "ab" * 32,
            "allow_reversals": False,
        }
    )
    cards = draw["computed_facts"]["cards"]
    assert len({card["card_id"] for card in cards}) == 3
    assert {card["orientation"] for card in cards} == {"upright"}
    assert draw["audit"]["selection_policy"] == "without_replacement"
    assert draw["audit"]["rule_ids"] == ["TAROT-DRAW-UNIQUE-001"]


def test_generated_seed_is_disclosed_and_replays() -> None:
    first = draw_cards({"spread": "single"})
    replay = draw_cards(
        {
            "spread": "single",
            "seed_hex": first["audit"]["seed_hex"],
            "allow_reversals": True,
        }
    )
    assert replay["computed_facts"] == first["computed_facts"]


def test_first_card_distribution_smoke_covers_full_deck() -> None:
    counts = {index: 0 for index in range(78)}
    for value in range(3900):
        draw = draw_cards({"spread": "single", "seed_hex": f"{value:064x}"})
        counts[draw["computed_facts"]["cards"][0]["card_index"]] += 1
    assert all(25 <= count <= 80 for count in counts.values())


def test_report_keeps_draw_facts_and_links_every_statement() -> None:
    draw = draw_cards({"spread": "situation-challenge-guidance", "seed_hex": "01" * 32})
    original = deepcopy(draw["computed_facts"])
    report = build_report(draw)
    assert draw["computed_facts"] == original
    assert report["computed_facts"] == original
    explanations = [*report["narrative"]["cards"], report["narrative"]["sequence"]]
    for explanation in explanations:
        assert explanation["fact_ids"] and explanation["rule_ids"]
    assert "fixed future" in report["narrative"]["sequence"]["statement"]


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({}, "invalid_spread"),
        ({"spread": "unregistered-spread"}, "invalid_spread"),
        ({"spread": "single", "seed_hex": "zz" * 32}, "invalid_seed"),
        ({"spread": "single", "allow_reversals": "yes"}, "invalid_reversal_policy"),
    ],
)
def test_bad_input_fails_closed(payload: dict, code: str) -> None:
    with pytest.raises(DrawError) as captured:
        draw_cards(payload)
    assert captured.value.code == code


def test_draw_output_schema() -> None:
    schema = json.loads((SYSTEM / "draw" / "output.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(draw_cards({"spread": "single", "seed_hex": "00" * 32}))
