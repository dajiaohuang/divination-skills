"""Deterministic Ziwei chart queries with fact-level provenance."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from systems.ziwei.engine import TRANSFORMATION_LABELS, TRANSFORMATIONS


def _palaces(chart: dict[str, Any]) -> list[dict[str, Any]]:
    palaces = chart.get("computed_facts", {}).get("palaces")
    if not isinstance(palaces, list) or len(palaces) != 12:
        raise ValueError("A valid twelve-palace Ziwei chart is required.")
    return palaces


def palace(chart: dict[str, Any], selector: int | str) -> dict[str, Any]:
    palaces = _palaces(chart)
    if isinstance(selector, int):
        if selector not in range(12):
            raise ValueError("Palace index must be between 0 and 11.")
        return deepcopy(palaces[selector])
    matches = [
        item
        for item in palaces
        if selector in {item["name"], item["earthlyBranch"], item["fact_id"]}
    ]
    if len(matches) != 1:
        raise ValueError(f"Palace selector must resolve exactly once: {selector}")
    return deepcopy(matches[0])


def surrounded_palaces(chart: dict[str, Any], selector: int | str) -> dict[str, Any]:
    target = palace(chart, selector)
    indices = {
        "target": target["index"],
        "trine_forward": (target["index"] + 4) % 12,
        "opposite": (target["index"] + 6) % 12,
        "trine_reverse": (target["index"] + 8) % 12,
    }
    return {
        "query_type": "three_directions_four_alignments",
        "target_fact_id": target["fact_id"],
        "palaces": {name: palace(chart, index) for name, index in indices.items()},
        "fact_ids": [_palaces(chart)[index]["fact_id"] for index in indices.values()],
        "rule_ids": ["ZIWEI-PALACE-SURROUNDED-001"],
    }


def find_star(chart: dict[str, Any], name: str) -> list[dict[str, Any]]:
    matches = []
    for item in _palaces(chart):
        for field in ("majorStars", "minorStars", "adjectiveStars", "auxiliaryStars"):
            for star in item[field]:
                if star["name"] == name:
                    matches.append(
                        {
                            "palace_index": item["index"],
                            "palace_name": item["name"],
                            "palace_fact_id": item["fact_id"],
                            "layer": field,
                            "star": deepcopy(star),
                        }
                    )
    return matches


def is_empty_palace(chart: dict[str, Any], selector: int | str) -> dict[str, Any]:
    item = palace(chart, selector)
    empty = len(item["majorStars"]) == 0
    return {
        "palace_fact_id": item["fact_id"],
        "is_empty_major_palace": empty,
        "major_star_fact_ids": [star["fact_id"] for star in item["majorStars"]],
        "rule_ids": ["ZIWEI-PALACE-EMPTY-001"],
    }


def transformation_paths(chart: dict[str, Any]) -> list[dict[str, Any]]:
    paths = []
    for item in _palaces(chart):
        for field in ("majorStars", "minorStars", "adjectiveStars", "auxiliaryStars"):
            for star in item[field]:
                if star.get("mutagen"):
                    paths.append(
                        {
                            "scope": "birth_year",
                            "origin_palace_fact_id": None,
                            "origin_stem": chart["computed_facts"]["raw_dates"]["year_stem"],
                            "target_star": star["name"],
                            "target_star_fact_id": star["fact_id"],
                            "target_palace_fact_id": item["fact_id"],
                            "transformation": star["mutagen"],
                            "self_transformation": False,
                            "rule_ids": ["ZIWEI-TRANSFORMATION-BIRTH-001"],
                            "source_ids": star["source_ids"],
                        }
                    )
    return paths


def palace_stem_transformation_paths(chart: dict[str, Any]) -> list[dict[str, Any]]:
    """Trace every palace-stem transformation, including self-transformations."""

    paths = []
    for origin in _palaces(chart):
        for star_name, label in zip(
            TRANSFORMATIONS[origin["heavenlyStem"]],
            TRANSFORMATION_LABELS,
            strict=True,
        ):
            for match in find_star(chart, star_name):
                paths.append(
                    {
                        "scope": "palace_stem",
                        "origin_palace_fact_id": origin["fact_id"],
                        "origin_stem": origin["heavenlyStem"],
                        "target_star": star_name,
                        "target_star_fact_id": match["star"]["fact_id"],
                        "target_palace_fact_id": match["palace_fact_id"],
                        "transformation": label,
                        "self_transformation": (
                            origin["fact_id"] == match["palace_fact_id"]
                        ),
                        "rule_ids": ["ZIWEI-TRANSFORMATION-PALACE-STEM-001"],
                        "source_ids": [
                            "SRC-ZIWEI-PROJECT-SPEC-001",
                            "SRC-ZIWEI-QUANSHU-001",
                        ],
                    }
                )
    return paths
