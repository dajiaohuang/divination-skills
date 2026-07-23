from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.runes.engine import draw
from systems.runes.layers import OLD_ENGLISH_COGNATES, build_layers

ROOT = Path(__file__).resolve().parent / "extension_cases"


def cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "layers").glob("*.json"))
    ]


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_layer_cases_replay(case: dict) -> None:
    source_draw = draw(case["raw_input"])
    original = deepcopy(source_draw)
    result = build_layers(source_draw)
    assert {
        "historical_evidence": result["historical_evidence"],
        "modern_reflection": result["modern_reflection"],
        "cross_layer_policy": result["cross_layer_policy"],
    } == case["expected_output"]
    assert source_draw == original


def test_all_twenty_four_names_have_historical_cognate_metadata() -> None:
    assert len(OLD_ENGLISH_COGNATES) == 24
    assert all(OLD_ENGLISH_COGNATES.values())
    result = build_layers(draw({"spread": "three-rune", "seed_hex": "ab" * 32}))
    assert all(
        item["historical_divinatory_meaning_claimed"] is False
        and item["source_ids"] == ["SRC-RUNES-EARLE-17101"]
        for item in result["historical_evidence"]
    )
    assert all(
        item["source_ids"] == ["SRC-RUNES-PROJECT-SPEC-001"]
        for item in result["modern_reflection"]
    )


def test_layer_case_gates() -> None:
    assert len(list((ROOT / "layers").glob("*.json"))) == 50
    disputes = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "layer_disputes").glob("*.json"))
    ]
    assert len(disputes) == 20
    assert all(
        item["expected_handling"] == "reject_cross_layer_inference"
        for item in disputes
    )
