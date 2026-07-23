"""Lenormand pair, nine-card, and Grand Tableau structural analysis."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from systems.lenormand.engine import SOURCE, items

LINEAGE = "lenormand-36-project-v0.2"


def _keywords(symbol_id: str) -> list[str]:
    item = next(item for item in items() if item["symbol_id"] == symbol_id)
    return item["upright"]


def _pair(left: dict[str, Any], right: dict[str, Any], number: int) -> dict[str, Any]:
    return {
        "fact_id": f"lenormand.pair.{number:03d}",
        "left_fact_id": left["fact_id"],
        "right_fact_id": right["fact_id"],
        "left_symbol_id": left["symbol_id"],
        "right_symbol_id": right["symbol_id"],
        "ordered_keywords": [_keywords(left["symbol_id"]), _keywords(right["symbol_id"])],
        "rule_ids": ["LENORMAND-PAIR-001"],
        "source_ids": [SOURCE],
    }


def analyze_layout(
    draw: dict[str, Any],
    *,
    significator: str | None = None,
) -> dict[str, Any]:
    """Analyze geometric relations without converting them into hidden facts."""

    if draw.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Lenormand draw is required.")
    if significator not in {None, "man", "woman"}:
        raise ValueError("significator must be man, woman, or omitted.")
    original = deepcopy(draw["computed_facts"])
    symbols = draw["computed_facts"]["symbols"]
    spread = draw["computed_facts"]["spread"]
    pairs = [
        _pair(symbols[index], symbols[index + 1], index + 1)
        for index in range(len(symbols) - 1)
    ]

    nine_card = None
    if spread == "nine-card":
        grid = [symbols[index : index + 3] for index in range(0, 9, 3)]
        lines = []
        line_specs = [
            ("row-1", (0, 1, 2)),
            ("row-2", (3, 4, 5)),
            ("row-3", (6, 7, 8)),
            ("column-1", (0, 3, 6)),
            ("column-2", (1, 4, 7)),
            ("column-3", (2, 5, 8)),
            ("diagonal-1", (0, 4, 8)),
            ("diagonal-2", (2, 4, 6)),
        ]
        for number, (name, indices) in enumerate(line_specs, start=1):
            lines.append(
                {
                    "fact_id": f"lenormand.nine.line.{number:03d}",
                    "name": name,
                    "card_fact_ids": [symbols[index]["fact_id"] for index in indices],
                    "rule_ids": ["LENORMAND-NINE-GRID-001"],
                    "source_ids": [SOURCE],
                }
            )
        nine_card = {
            "rows": [
                [card["fact_id"] for card in row]
                for row in grid
            ],
            "center_fact_id": symbols[4]["fact_id"],
            "lines": lines,
            "mirrors": [
                {
                    "left_fact_id": symbols[left]["fact_id"],
                    "right_fact_id": symbols[right]["fact_id"],
                }
                for left, right in ((0, 8), (1, 7), (2, 6), (3, 5))
            ],
        }

    grand_tableau = None
    if spread == "grand-tableau":
        houses = []
        deck = items()
        for index, card in enumerate(symbols):
            house = deck[index]
            houses.append(
                {
                    "fact_id": f"lenormand.grand.house.{index + 1:03d}",
                    "house_number": index + 1,
                    "house_symbol_id": house["symbol_id"],
                    "occupying_card_fact_id": card["fact_id"],
                    "occupying_symbol_id": card["symbol_id"],
                    "row": index // 9 + 1,
                    "column": index % 9 + 1,
                    "rule_ids": ["LENORMAND-GRAND-TABLEAU-001"],
                    "source_ids": [SOURCE],
                }
            )
        selected_name = significator.capitalize() if significator else None
        selected_index = (
            next(
                (
                    index
                    for index, card in enumerate(symbols)
                    if card["name"] == selected_name
                ),
                None,
            )
            if selected_name
            else None
        )
        relative = []
        if selected_index is not None:
            row, column = divmod(selected_index, 9)
            for index, card in enumerate(symbols):
                if index == selected_index:
                    continue
                other_row, other_column = divmod(index, 9)
                relative.append(
                    {
                        "card_fact_id": card["fact_id"],
                        "row_delta": other_row - row,
                        "column_delta": other_column - column,
                        "manhattan_distance": abs(other_row - row) + abs(other_column - column),
                    }
                )
        grand_tableau = {
            "layout": "four-rows-by-nine-columns",
            "houses": houses,
            "significator": {
                "requested": significator,
                "status": "located" if selected_index is not None else "not_requested",
                "card_fact_id": (
                    symbols[selected_index]["fact_id"] if selected_index is not None else None
                ),
                "row": selected_index // 9 + 1 if selected_index is not None else None,
                "column": selected_index % 9 + 1 if selected_index is not None else None,
                "relative_cards": relative,
            },
            "corners": [
                symbols[index]["fact_id"] for index in (0, 8, 27, 35)
            ],
        }

    if draw["computed_facts"] != original:
        raise AssertionError("Layout analysis must not mutate draw facts.")
    rule_ids = ["LENORMAND-PAIR-001"]
    if nine_card:
        rule_ids.append("LENORMAND-NINE-GRID-001")
    if grand_tableau:
        rule_ids.append("LENORMAND-GRAND-TABLEAU-001")
    return {
        "schema_version": "0.2.0",
        "system": "lenormand",
        "lineage": LINEAGE,
        "spread": spread,
        "pairs": pairs,
        "nine_card": nine_card,
        "grand_tableau": grand_tableau,
        "conclusions": [
            {
                "conclusion_id": "lenormand.layout.structure.001",
                "statement": (
                    "The result exposes ordered and geometric card relations only; "
                    "it does not establish hidden facts or a fixed future."
                ),
                "fact_ids": [card["fact_id"] for card in symbols],
                "rule_ids": rule_ids,
                "source_ids": [SOURCE],
                "support": ["All relations are derived from disclosed card positions."],
                "counterevidence": ["Symbol order has no demonstrated causal force."],
                "limitations": [
                    (
                        "No third-party intent, fidelity, health state, or guaranteed "
                        "event is inferred."
                    )
                ],
            }
        ],
        "validation": {"status": "valid", "warnings": []},
    }
