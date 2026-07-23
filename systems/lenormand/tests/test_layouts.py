from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.lenormand.engine import draw
from systems.lenormand.layouts import analyze_layout

ROOT = Path(__file__).resolve().parent / "extension_cases"


def cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "layouts").glob("*.json"))
    ]


def compact(result: dict) -> dict:
    return {
        "spread": result["spread"],
        "pairs": result["pairs"],
        "nine_card": result["nine_card"],
        "grand_tableau": result["grand_tableau"],
    }


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_layout_cases_replay(case: dict) -> None:
    source_draw = draw(case["raw_input"])
    original = deepcopy(source_draw)
    result = analyze_layout(source_draw, significator=case["significator"])
    assert compact(result) == case["expected_output"]
    assert source_draw == original


def test_nine_card_and_grand_tableau_geometry() -> None:
    nine = analyze_layout(draw({"spread": "nine-card", "seed_hex": "aa" * 32}))
    assert len(nine["pairs"]) == 8
    assert len(nine["nine_card"]["lines"]) == 8
    assert len(nine["nine_card"]["mirrors"]) == 4
    grand = analyze_layout(
        draw({"spread": "grand-tableau", "seed_hex": "bb" * 32}),
        significator="woman",
    )
    assert len(grand["pairs"]) == 35
    assert len(grand["grand_tableau"]["houses"]) == 36
    assert grand["grand_tableau"]["significator"]["status"] == "located"


def test_layout_case_gates() -> None:
    assert len(list((ROOT / "layouts").glob("*.json"))) == 50
    disputes = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "layout_disputes").glob("*.json"))
    ]
    assert len(disputes) == 20
    assert all(
        item["expected_handling"] == "separate_lineage_not_silent_merge"
        for item in disputes
    )


def test_invalid_significator_fails_closed() -> None:
    source_draw = draw({"spread": "grand-tableau", "seed_hex": "cc" * 32})
    with pytest.raises(ValueError, match="significator"):
        analyze_layout(source_draw, significator="querent")
