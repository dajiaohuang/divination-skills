from __future__ import annotations

import json
from pathlib import Path

from systems.ziwei.engine import calculate

CASE = Path(__file__).resolve().parent / "external_references" / "CASE-ZIWEI-WENMO-001.json"


def _load_case() -> dict:
    return json.loads(CASE.read_text(encoding="utf-8"))


def _names(palace: dict, group: str) -> list[str]:
    return [star["name"] for star in palace[group]]


def test_wenmo_reference_matches_project_structural_subset() -> None:
    case = _load_case()
    expected = case["expected"]
    chart = calculate(case["input"])
    facts = chart["computed_facts"]
    palaces = {palace["earthlyBranch"]: palace for palace in facts["palaces"]}

    assert facts["lunar_date"] == expected["lunar_date"]
    assert facts["time_label"] == expected["time_label"]
    assert facts["five_elements_class"] == expected["five_elements_class"]
    assert facts["soul_palace_branch"] == expected["soul_palace_branch"]
    assert facts["body_palace_branch"] == expected["body_palace_branch"]
    assert facts["soul_ruler"] == expected["soul_ruler"]
    assert facts["body_ruler"] == expected["body_ruler"]
    assert facts["cause_palace"]["palace_name"] == expected["cause_palace"]

    for branch, palace in palaces.items():
        reference_name = expected["palace_names_by_branch"][branch]
        canonical_name = case["display_aliases"].get(reference_name, reference_name)
        assert palace["name"] == canonical_name
        assert palace["heavenlyStem"] == expected["palace_stems_by_branch"][branch]
        assert _names(palace, "majorStars") == expected["major_stars_by_branch"][branch]
        assert _names(palace, "minorStars") == expected["minor_stars_by_branch"][branch]
        assert [
            palace["decadal"]["start_age"],
            palace["decadal"]["end_age"],
        ] == expected["decadal_by_branch"][branch]
        assert palace["minor_limit_ages"][:5] == expected["minor_limit_prefix_by_branch"][branch]


def test_wenmo_reference_matches_selected_auxiliaries_and_birth_transformations() -> None:
    case = _load_case()
    expected = case["expected"]
    chart = calculate(case["input"])
    palaces = {palace["earthlyBranch"]: palace for palace in chart["computed_facts"]["palaces"]}

    for branch, names in expected["selected_auxiliary_stars_by_branch"].items():
        actual = set(_names(palaces[branch], "auxiliaryStars"))
        assert set(names) <= actual

    actual_transformations = {
        star["name"]: star["mutagen"]
        for palace in palaces.values()
        for group in ("majorStars", "minorStars")
        for star in palace[group]
        if star["mutagen"] is not None
    }
    assert actual_transformations == expected["transformations"]


def test_wenmo_civil_and_reported_true_solar_times_keep_the_same_hour_branch() -> None:
    case = _load_case()
    civil = calculate(
        {
            **case["input"],
            "local_datetime": case["reported_input"]["civil_datetime"],
        }
    )
    reported_true_solar = calculate(case["input"])

    assert civil["normalized_input"]["time_index"] == 10
    assert reported_true_solar["normalized_input"]["time_index"] == 10
    assert civil["computed_facts"] == reported_true_solar["computed_facts"]
