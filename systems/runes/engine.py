from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from divination_skills.auditable_draw import build_symbol_report, draw_symbols

SPREADS = {"single": ("focus",), "three-rune": ("context", "tension", "practice")}
SOURCE = "SRC-RUNES-PROJECT-SPEC-001"


@lru_cache(maxsize=1)
def items() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parent / "data" / "deck.json"
    return json.loads(path.read_text(encoding="utf-8"))


def draw(payload: dict[str, Any]) -> dict[str, Any]:
    return draw_symbols(
        payload,
        system="runes",
        lineage="elder-futhark-project-v0.1",
        items=items(),
        spreads=SPREADS,
        source_id=SOURCE,
    )


def explain(value: dict[str, Any]) -> dict[str, Any]:
    return build_symbol_report(
        value,
        items=items(),
        system="runes",
        source_id=SOURCE,
        orientation_rule="RUNES-SYMBOL-UPRIGHT-001",
        position_rule="RUNES-POSITION-001",
        sequence_rule="RUNES-SEQUENCE-001",
    )
