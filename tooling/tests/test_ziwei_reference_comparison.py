from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tooling" / "scripts" / "compare_ziwei_reference.py"
SPEC = importlib.util.spec_from_file_location("compare_ziwei_reference", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_comparator_is_non_authoritative_and_classifies_all_paths() -> None:
    native = {"palaces": [{"name": "命宫", "stars": ["紫微"]}], "policy": "current_day"}
    reference = {
        "palaces": [{"name": "命宮", "stars": ["紫微"]}],
        "policy": "next_day",
        "extra": True,
    }
    report = MODULE.compare(
        native,
        reference,
        {
            "palaces.0.name": "display_name_difference",
            "policy": "boundary_policy_difference",
        },
    )
    assert report["authoritative"] is False
    assert report["runtime_dependency"] is False
    assert report["counts"] == {
        "boundary_policy_difference": 1,
        "display_name_difference": 1,
        "exact_match": 1,
        "project_missing": 1,
    }


def test_comparator_never_promotes_unclassified_difference_to_error() -> None:
    report = MODULE.compare({"x": 1}, {"x": 2})
    assert report["differences"][0]["classification"] == "pending_research"
    with pytest.raises(ValueError):
        MODULE.compare({"x": 1}, {"x": 2}, {"x": "automatic_truth"})
