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


@lru_cache(maxsize=1)
def items() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parent / "data" / "deck.json"
    return json.loads(path.read_text(encoding="utf-8"))


def draw(payload: dict[str, Any]) -> dict[str, Any]:
    return draw_symbols(
        payload,
        system="lenormand",
        lineage=(
            "lenormand-36-project-v0.2"
            if payload.get("spread") == "grand-tableau"
            else "lenormand-36-project-v0.1"
        ),
        items=items(),
        spreads=SPREADS,
        source_id=SOURCE,
    )


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
