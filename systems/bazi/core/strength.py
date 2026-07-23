"""Explicitly selected, bounded seasonal-support feature model."""

from __future__ import annotations

from typing import Any

LINEAGE = "project-seasonal-support-v0.1"
ELEMENTS = ("wood", "fire", "earth", "metal", "water")


def seasonal_support_features(chart: dict[str, Any]) -> dict[str, Any]:
    """Calculate the project-authored feature vector from immutable chart facts."""

    facts = chart["computed_facts"]
    day_element = facts["day_master"]["element"]
    day_index = ELEMENTS.index(day_element)
    resource_element = ELEMENTS[(day_index - 1) % len(ELEMENTS)]
    supportive_elements = {day_element, resource_element}

    month_main_stem = facts["pillars"]["month"]["branch"]["hidden_stems"][0]
    month_main_element = _stem_element(month_main_stem)

    seasonal_points = 2 if month_main_element in supportive_elements else 0
    root_positions = [
        position
        for position, pillar in facts["pillars"].items()
        if any(_stem_element(stem) == day_element for stem in pillar["branch"]["hidden_stems"])
    ]
    visible_support_positions = [
        position
        for position, pillar in facts["pillars"].items()
        if position != "day" and pillar["stem"]["element"] in supportive_elements
    ]
    total = seasonal_points + len(root_positions) + len(visible_support_positions)
    return {
        "lineage": LINEAGE,
        "day_element": day_element,
        "resource_element": resource_element,
        "month_main_stem": month_main_stem,
        "month_main_element": month_main_element,
        "seasonal_points": seasonal_points,
        "root_positions": root_positions,
        "visible_support_positions": visible_support_positions,
        "total_score": total,
    }


def _stem_element(stem: str) -> str:
    stems = "甲乙丙丁戊己庚辛壬癸"
    return ELEMENTS[stems.index(stem) // 2]
