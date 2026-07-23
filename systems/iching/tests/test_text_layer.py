from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from systems.iching.engine import cast
from systems.iching.text_layer import build_classical_layer, select_reading_units

ROOT = Path(__file__).resolve().parent / "extension_cases"


def cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "text_layer").glob("*.json"))
    ]


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_text_layer_cases_replay(case: dict) -> None:
    source_cast = cast(case["raw_input"])
    original = deepcopy(source_cast)
    result = build_classical_layer(source_cast, policy_id=case["policy_id"])
    assert {
        "selection": result["selection"],
        "editions": result["editions"],
        "version_comparison": result["version_comparison"],
    } == case["expected_output"]
    assert source_cast == original


@pytest.mark.parametrize("count", range(7))
def test_count_policy_covers_every_moving_line_count(count: int) -> None:
    source_cast = cast({"seed_hex": "88" * 32})
    source_cast["computed_facts"]["moving_line_positions"] = list(range(1, count + 1))
    result = select_reading_units(
        source_cast,
        policy_id="zhu-xi-count-routing-v0.2",
    )
    assert result["moving_line_count"] == count
    assert result["selected_units"]


def test_classical_layer_never_bundles_text_or_invents_variants() -> None:
    result = build_classical_layer(cast({"seed_hex": "99" * 32}))
    assert result["version_comparison"]["status"] == "not_collated"
    assert result["version_comparison"]["differences"] == []
    assert all(
        locator["text_included"] is False
        for edition in result["editions"]
        for locator in edition["selected_passage_locators"]
    )


def test_policy_case_gates() -> None:
    assert len(list((ROOT / "text_layer").glob("*.json"))) == 50
    disputes = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "policy_disputes").glob("*.json"))
    ]
    assert len(disputes) == 20
    assert all(
        item["expected_handling"] == "return_separate_outputs_without_merging"
        for item in disputes
    )


def test_unknown_policy_fails_closed() -> None:
    with pytest.raises(ValueError, match="policy_id"):
        select_reading_units(cast({"seed_hex": "77" * 32}), policy_id="blended")
