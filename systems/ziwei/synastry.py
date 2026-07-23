"""Directional and symmetric structural comparison for two Ziwei charts."""

from __future__ import annotations

from typing import Any

from divination_skills.contracts import stable_identifier

from systems.ziwei.analyzer import find_star
from systems.ziwei.engine import (
    LINEAGE,
    TRANSFORMATION_LABELS,
    TRANSFORMATIONS,
)


def _chart_id(chart: dict[str, Any]) -> str:
    return stable_identifier(
        "CHART-ZIWEI",
        {"engine": chart["engine"], "normalized_input": chart["normalized_input"]},
    )


def _directional(
    source: dict[str, Any],
    target: dict[str, Any],
    direction: str,
) -> list[dict[str, Any]]:
    stem = source["computed_facts"]["raw_dates"]["year_stem"]
    facts = []
    for star_name, transformation in zip(
        TRANSFORMATIONS[stem],
        TRANSFORMATION_LABELS,
        strict=True,
    ):
        for match in find_star(target, star_name):
            facts.append(
                {
                    "fact_id": (
                        f"ziwei.synastry.{direction}.transformation."
                        f"{len(facts) + 1:03d}"
                    ),
                    "direction": direction,
                    "source_year_stem": stem,
                    "target_star": star_name,
                    "target_star_fact_id": match["star"]["fact_id"],
                    "target_palace_name": match["palace_name"],
                    "target_palace_fact_id": match["palace_fact_id"],
                    "transformation": transformation,
                    "rule_ids": ["ZIWEI-SYNASTRY-DIRECTIONAL-001"],
                    "source_ids": [
                        "SRC-ZIWEI-PROJECT-SPEC-001",
                        "SRC-ZIWEI-QUANSHU-001",
                    ],
                }
            )
    return facts


def _symmetric(chart_a: dict[str, Any], chart_b: dict[str, Any]) -> list[dict[str, Any]]:
    by_role_a = {
        palace["name"]: palace for palace in chart_a["computed_facts"]["palaces"]
    }
    by_role_b = {
        palace["name"]: palace for palace in chart_b["computed_facts"]["palaces"]
    }
    facts = []
    for role in sorted(by_role_a):
        palace_a = by_role_a[role]
        palace_b = by_role_b[role]
        stars_a = {star["name"]: star for star in palace_a["majorStars"]}
        stars_b = {star["name"]: star for star in palace_b["majorStars"]}
        for star_name in sorted(set(stars_a) & set(stars_b)):
            facts.append(
                {
                    "fact_id": f"ziwei.synastry.symmetric.{len(facts) + 1:03d}",
                    "palace_name": role,
                    "shared_major_star": star_name,
                    "a_palace_fact_id": palace_a["fact_id"],
                    "a_star_fact_id": stars_a[star_name]["fact_id"],
                    "b_palace_fact_id": palace_b["fact_id"],
                    "b_star_fact_id": stars_b[star_name]["fact_id"],
                    "rule_ids": ["ZIWEI-SYNASTRY-SYMMETRIC-001"],
                    "source_ids": ["SRC-ZIWEI-PROJECT-SPEC-001"],
                }
            )
    return facts


def compare_charts(chart_a: dict[str, Any], chart_b: dict[str, Any]) -> dict[str, Any]:
    for label, chart in (("A", chart_a), ("B", chart_b)):
        if chart.get("validation", {}).get("status") != "valid":
            raise ValueError(f"Chart {label} must be valid.")
        if chart.get("normalized_input", {}).get("lineage") != LINEAGE:
            raise ValueError(f"Chart {label} must use lineage {LINEAGE}.")
    return {
        "schema_version": "0.4.0",
        "system": "ziwei",
        "lineage": LINEAGE,
        "chart_refs": {"A": _chart_id(chart_a), "B": _chart_id(chart_b)},
        "directional": {
            "A_to_B": _directional(chart_a, chart_b, "A_to_B"),
            "B_to_A": _directional(chart_b, chart_a, "B_to_A"),
        },
        "symmetric": _symmetric(chart_a, chart_b),
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "structural_relationship_only",
                    "message": (
                        "Cross-chart transformations and shared stars do not reveal "
                        "compatibility, intent, fidelity, or outcomes."
                    ),
                }
            ],
        },
    }
