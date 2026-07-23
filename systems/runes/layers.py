"""Strict separation between historical rune-name evidence and modern reflection."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from systems.runes.engine import items

HISTORICAL_SOURCE = "SRC-RUNES-EARLE-17101"
MODERN_SOURCE = "SRC-RUNES-PROJECT-SPEC-001"
OLD_ENGLISH_COGNATES = {
    "Fehu": "Feoh",
    "Uruz": "Ur",
    "Thurisaz": "Thorn",
    "Ansuz": "Os",
    "Raidho": "Rad",
    "Kenaz": "Cen",
    "Gebo": "Gyfu",
    "Wunjo": "Wynn",
    "Hagalaz": "Haegl",
    "Nauthiz": "Nyd",
    "Isa": "Is",
    "Jera": "Ger",
    "Eihwaz": "Eoh",
    "Perthro": "Peorth",
    "Algiz": "Eolh-secg",
    "Sowilo": "Sigel",
    "Tiwaz": "Tir",
    "Berkano": "Beorc",
    "Ehwaz": "Eh",
    "Mannaz": "Mann",
    "Laguz": "Lagu",
    "Ingwaz": "Ing",
    "Dagaz": "Daeg",
    "Othala": "Ethel",
}


def build_layers(draw: dict[str, Any]) -> dict[str, Any]:
    """Return historical identifiers and modern prompts in disjoint records."""

    if draw.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid rune draw is required.")
    original = deepcopy(draw["computed_facts"])
    catalog = {item["symbol_id"]: item for item in items()}
    historical = []
    modern = []
    for fact in draw["computed_facts"]["symbols"]:
        item = catalog[fact["symbol_id"]]
        historical.append(
            {
                "fact_id": f"runes.historical.{len(historical) + 1:03d}",
                "draw_fact_id": fact["fact_id"],
                "elder_futhark_name": fact["name"],
                "old_english_cognate": OLD_ENGLISH_COGNATES[fact["name"]],
                "evidence_type": "name_and_rune_poem_attestation_locator",
                "source_locator": "Anglo-Saxon Literature, Runic Poem discussion, pp. 239-240",
                "historical_divinatory_meaning_claimed": False,
                "rule_ids": ["RUNES-HISTORICAL-LAYER-001"],
                "source_ids": [HISTORICAL_SOURCE],
            }
        )
        modern.append(
            {
                "fact_id": f"runes.modern.{len(modern) + 1:03d}",
                "draw_fact_id": fact["fact_id"],
                "symbol_id": fact["symbol_id"],
                "keywords": item["upright"],
                "status": "project_authored_modern_reflection",
                "rule_ids": ["RUNES-MODERN-REFLECTION-LAYER-001"],
                "source_ids": [MODERN_SOURCE],
            }
        )
    if draw["computed_facts"] != original:
        raise AssertionError("Rune layer construction must not mutate draw facts.")
    return {
        "schema_version": "0.2.0",
        "system": "runes",
        "lineages": {
            "historical": "anglo-saxon-rune-name-evidence-v0.2",
            "modern": "elder-futhark-project-reflection-v0.2",
        },
        "historical_evidence": historical,
        "modern_reflection": modern,
        "cross_layer_policy": {
            "status": "strictly_separated",
            "historical_source_supports_modern_divination": False,
            "message": (
                "Historical rune-name evidence is not cited as support for modern "
                "divinatory keywords or predictions."
            ),
        },
        "conclusions": [
            {
                "conclusion_id": "runes.layer.boundary.001",
                "statement": (
                    "The historical layer identifies names and attestations; "
                    "the separate modern layer supplies project-authored reflection prompts."
                ),
                "fact_ids": [
                    *[item["fact_id"] for item in historical],
                    *[item["fact_id"] for item in modern],
                ],
                "rule_ids": [
                    "RUNES-HISTORICAL-LAYER-001",
                    "RUNES-MODERN-REFLECTION-LAYER-001",
                ],
                "source_ids": [HISTORICAL_SOURCE, MODERN_SOURCE],
                "support": ["Each layer cites its own source and lineage."],
                "counterevidence": [
                    "The historical source does not document this project's divination practice."
                ],
                "limitations": [
                    "No historical continuity, hidden fact, outcome, or prediction is claimed."
                ],
            }
        ],
        "validation": {"status": "valid", "warnings": []},
    }
