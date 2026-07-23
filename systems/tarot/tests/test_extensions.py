from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from systems.tarot.combinations import analyze_combinations
from systems.tarot.core import build_report
from systems.tarot.draw.engine import draw_cards
from systems.tarot.journal import (
    JournalError,
    append_entry,
    descriptive_statistics,
    load_entries,
)

ROOT = Path(__file__).resolve().parent


def cases() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "extension_cases" / "spreads").glob("*.json"))
    ]


def compact(draw: dict, combinations: dict) -> dict:
    return {
        "computed_facts": draw["computed_facts"],
        "pairs": combinations["pairs"],
        "distribution": combinations["distribution"],
    }


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_extension_cases_replay(case: dict) -> None:
    draw = draw_cards(case["raw_input"])
    original = deepcopy(draw)
    combinations = analyze_combinations(draw)
    assert compact(draw, combinations) == case["expected_output"]
    assert draw == original


def test_all_new_spreads_build_reports_and_match_schema() -> None:
    schema = json.loads((ROOT.parent / "draw" / "output.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    expected_sizes = {
        "elemental-five": 5,
        "relationship-six": 6,
        "horseshoe-seven": 7,
        "celtic-cross": 10,
    }
    for spread, size in expected_sizes.items():
        draw = draw_cards({"spread": spread, "seed_hex": "dd" * 32})
        validator.validate(draw)
        assert len(draw["computed_facts"]["cards"]) == size
        assert len(build_report(draw)["narrative"]["cards"]) == size


def test_journal_requires_consent_omits_raw_question_and_counts(tmp_path: Path) -> None:
    journal = tmp_path / "journal.jsonl"
    draw = draw_cards(
        {
            "spread": "elemental-five",
            "question": "private question text",
            "seed_hex": "ee" * 32,
        }
    )
    with pytest.raises(JournalError) as captured:
        append_entry(
            journal,
            draw,
            reflection="reflection",
            consent_to_store=False,
        )
    assert captured.value.code == "storage_consent_required"
    first = append_entry(
        journal,
        draw,
        reflection="First reflection",
        tags=["weekly"],
        consent_to_store=True,
        occurred_at="2026-07-23T12:00:00+00:00",
    )
    second = append_entry(
        journal,
        draw,
        reflection="Second reflection",
        tags=["weekly", "review"],
        consent_to_store=True,
        occurred_at="2026-07-24T12:00:00+00:00",
    )
    assert first["entry_id"] != second["entry_id"]
    stored_text = journal.read_text(encoding="utf-8")
    assert "private question text" not in stored_text
    entries = load_entries(journal)
    stats = descriptive_statistics(entries)
    assert stats["entry_count"] == 2
    assert first["rule_ids"] == ["TAROT-JOURNAL-PRIVACY-001"]
    assert stats["rule_ids"] == ["TAROT-JOURNAL-STATS-001"]
    assert stats["spread_counts"] == {"elemental-five": 2}
    assert stats["tag_counts"] == {"review": 1, "weekly": 2}
    assert "predictive accuracy" in stats["limitations"][0]


def test_extension_case_gates_and_no_image_assets() -> None:
    assert len(list((ROOT / "extension_cases" / "spreads").glob("*.json"))) == 50
    disputes = list((ROOT / "extension_cases" / "spread_disputes").glob("*.json"))
    assert len(disputes) == 20
    forbidden = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
    assert not [
        path
        for path in ROOT.parent.rglob("*")
        if path.is_file() and path.suffix.lower() in forbidden
    ]
