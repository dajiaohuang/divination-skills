"""Structural multi-card Tarot relations."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from systems.tarot.draw.engine import load_deck

SOURCE_ID = "SRC-TAROT-DECK-SPEC-001"
ELEMENT_RELATION = {
    frozenset(("fire", "air")): "complementary",
    frozenset(("water", "earth")): "complementary",
    frozenset(("fire", "water")): "contrasting",
    frozenset(("air", "earth")): "contrasting",
    frozenset(("fire", "earth")): "mixed",
    frozenset(("air", "water")): "mixed",
}


def _pair_relation(left: dict[str, Any], right: dict[str, Any], number: int) -> dict[str, Any]:
    relation = "unclassified"
    if left["element"] and right["element"]:
        relation = (
            "same_element"
            if left["element"] == right["element"]
            else ELEMENT_RELATION[frozenset((left["element"], right["element"]))]
        )
    return {
        "fact_id": f"tarot.combination.pair.{number:03d}",
        "left_card_id": left["card_id"],
        "right_card_id": right["card_id"],
        "arcana_relation": (
            "same_arcana" if left["arcana"] == right["arcana"] else "mixed_arcana"
        ),
        "element_relation": relation,
        "same_suit": bool(left["suit"] and left["suit"] == right["suit"]),
        "same_rank": left["rank"] == right["rank"],
        "rule_ids": ["TAROT-COMBINATION-RELATION-001"],
        "source_ids": [SOURCE_ID],
    }


def analyze_combinations(draw: dict[str, Any]) -> dict[str, Any]:
    if draw.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Tarot draw is required.")
    original = deepcopy(draw["computed_facts"])
    catalog = {card["card_id"]: card for card in load_deck()["cards"]}
    facts = draw["computed_facts"]["cards"]
    cards = [catalog[fact["card_id"]] for fact in facts]
    pairs = [
        _pair_relation(cards[index], cards[index + 1], index + 1)
        for index in range(len(cards) - 1)
    ]
    arcana_counts = {
        arcana: sum(card["arcana"] == arcana for card in cards)
        for arcana in ("major", "minor")
    }
    suit_counts = {
        suit: sum(card["suit"] == suit for card in cards)
        for suit in ("wands", "cups", "swords", "pentacles")
    }
    element_counts = {
        element: sum(card["element"] == element for card in cards)
        for element in ("fire", "water", "air", "earth")
    }
    rank_groups: dict[str, list[str]] = {}
    for card in cards:
        rank_groups.setdefault(card["rank"], []).append(card["card_id"])
    repeated_ranks = {
        rank: card_ids for rank, card_ids in rank_groups.items() if len(card_ids) > 1
    }
    if draw["computed_facts"] != original:
        raise AssertionError("Combination analysis must not mutate draw facts.")
    return {
        "schema_version": "0.2.0",
        "system": "tarot",
        "lineage": "rws-text-baseline-v0.2",
        "spread": draw["computed_facts"]["spread"],
        "pairs": pairs,
        "distribution": {
            "arcana_counts": arcana_counts,
            "suit_counts": suit_counts,
            "element_counts": element_counts,
            "repeated_ranks": repeated_ranks,
        },
        "conclusions": [
            {
                "conclusion_id": "tarot.combination.structure.001",
                "statement": (
                    "The result describes visible card relations and counts only; "
                    "it does not establish causation, hidden facts, or a fixed future."
                ),
                "fact_ids": [fact["fact_id"] for fact in facts],
                "rule_ids": ["TAROT-COMBINATION-RELATION-001"],
                "source_ids": [SOURCE_ID],
                "support": ["Relations use only disclosed deck metadata and draw order."],
                "counterevidence": ["Symbol combinations have no demonstrated causal force."],
                "limitations": ["No relationship intent, diagnosis, or event outcome is inferred."],
            }
        ],
        "validation": {"status": "valid", "warnings": []},
    }
