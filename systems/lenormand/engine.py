from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from divination_skills.auditable_draw import build_symbol_report, draw_symbols

SPREADS = {
    "single": ("focus",),
    "three-card": ("context", "development", "focus"),
    "nine-card": tuple(f"p{number}" for number in range(1, 10)),
    "grand-tableau": tuple(f"p{number}" for number in range(1, 37)),
}
SOURCE = "SRC-LENORMAND-PROJECT-SPEC-001"
HISTORICAL_SOURCE = "SRC-LENORMAND-BM-HOPE-001"
PLAYING_CARDS = (
    "9-hearts",
    "6-diamonds",
    "10-spades",
    "king-hearts",
    "7-hearts",
    "king-clubs",
    "queen-clubs",
    "9-diamonds",
    "queen-spades",
    "jack-diamonds",
    "jack-clubs",
    "7-diamonds",
    "jack-spades",
    "9-clubs",
    "10-clubs",
    "6-hearts",
    "queen-hearts",
    "10-hearts",
    "6-spades",
    "8-spades",
    "8-clubs",
    "queen-diamonds",
    "7-clubs",
    "jack-hearts",
    "ace-clubs",
    "10-diamonds",
    "7-spades",
    "ace-hearts",
    "ace-spades",
    "king-spades",
    "ace-diamonds",
    "8-hearts",
    "8-diamonds",
    "king-diamonds",
    "9-spades",
    "6-clubs",
)


@lru_cache(maxsize=1)
def items() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parent / "data" / "deck.json"
    return json.loads(path.read_text(encoding="utf-8"))


def draw(payload: dict[str, Any]) -> dict[str, Any]:
    result = draw_symbols(
        payload,
        system="lenormand",
        lineage="lenormand-36-project-v0.3",
        items=items(),
        spreads=SPREADS,
        source_id=SOURCE,
        draw_rule_id="LENORMAND-DRAW-UNIQUE-001",
        identity_rule_id="LENORMAND-CARD-IDENTITY-001",
    )
    result["schema_version"] = "0.3.0"
    result["engine"]["version"] = "0.3.0"
    result["engine"]["source_ids"] = [SOURCE, HISTORICAL_SOURCE]
    by_id = {item["symbol_id"]: item for item in items()}
    for fact in result["computed_facts"]["symbols"]:
        item = by_id[fact["symbol_id"]]
        number = item["number"]
        fact["card_number"] = number
        fact["playing_card"] = PLAYING_CARDS[number - 1]
        fact["identity_lineage"] = "game-of-hope-identity-v0.3"
        fact["source_ids"] = [SOURCE, HISTORICAL_SOURCE]
    return result


def explain(value: dict[str, Any]) -> dict[str, Any]:
    return build_symbol_report(
        value,
        items=items(),
        system="lenormand",
        source_id=SOURCE,
        orientation_rule="LENORMAND-CARD-UPRIGHT-001",
        position_rule="LENORMAND-POSITION-001",
        sequence_rule="LENORMAND-SEQUENCE-001",
    )
