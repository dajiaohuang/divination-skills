"""Directional overlays and symmetric cross-chart aspects."""

from __future__ import annotations

from typing import Any

from divination_skills.contracts import stable_identifier

from systems.western_astrology.calculator.engine import ASPECTS


def _chart_id(chart: dict[str, Any]) -> str:
    return stable_identifier(
        "CHART-WESTERN",
        {"engine": chart["engine"], "normalized_input": chart["normalized_input"]},
    )


def _separation(left: float, right: float) -> float:
    distance = abs(left - right) % 360
    return min(distance, 360 - distance)


def _cross_aspects(chart_a: dict[str, Any], chart_b: dict[str, Any]) -> list[dict[str, Any]]:
    facts = []
    for position_a in chart_a["computed_facts"]["positions"]:
        for position_b in chart_b["computed_facts"]["positions"]:
            separation = _separation(
                position_a["longitude_degrees"],
                position_b["longitude_degrees"],
            )
            for name, exact, allowed_orb in ASPECTS:
                orb = abs(separation - exact)
                if orb <= allowed_orb:
                    facts.append(
                        {
                            "fact_id": (
                                f"western.synastry.aspect.{len(facts) + 1:03d}"
                            ),
                            "a_body": position_a["body"],
                            "a_fact_id": position_a["fact_id"],
                            "b_body": position_b["body"],
                            "b_fact_id": position_b["fact_id"],
                            "aspect": name,
                            "separation_degrees": round(separation, 8),
                            "orb_degrees": round(orb, 8),
                            "allowed_orb_degrees": allowed_orb,
                            "rule_ids": ["WESTERN-SYNASTRY-ASPECT-001"],
                            "source_ids": ["SRC-WESTERN-PROJECT-SPEC-001"],
                        }
                    )
                    break
    return facts


def _overlays(
    source: dict[str, Any],
    target: dict[str, Any],
    direction: str,
) -> list[dict[str, Any]]:
    first_cusp = target["computed_facts"]["house_cusps"][0]["longitude_degrees"]
    facts = []
    for position in source["computed_facts"]["positions"]:
        house = int((position["longitude_degrees"] - first_cusp) % 360 // 30) + 1
        facts.append(
            {
                "fact_id": f"western.synastry.overlay.{direction}.{position['body']}",
                "direction": direction,
                "source_body": position["body"],
                "source_fact_id": position["fact_id"],
                "target_house": house,
                "target_cusp_fact_id": target["computed_facts"]["house_cusps"][house - 1][
                    "fact_id"
                ],
                "rule_ids": ["WESTERN-SYNASTRY-OVERLAY-001"],
                "source_ids": ["SRC-WESTERN-PROJECT-SPEC-001"],
            }
        )
    return facts


def compare_charts(chart_a: dict[str, Any], chart_b: dict[str, Any]) -> dict[str, Any]:
    for label, chart in (("A", chart_a), ("B", chart_b)):
        if chart.get("validation", {}).get("status") != "valid":
            raise ValueError(f"Chart {label} must be valid.")
    return {
        "schema_version": "0.2.0",
        "system": "western-astrology",
        "lineage": "tropical-geocentric-major-aspects-v0.2",
        "chart_refs": {"A": _chart_id(chart_a), "B": _chart_id(chart_b)},
        "directional": {
            "A_to_B": _overlays(chart_a, chart_b, "A_to_B"),
            "B_to_A": _overlays(chart_b, chart_a, "B_to_A"),
        },
        "symmetric": _cross_aspects(chart_a, chart_b),
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "structural_relationship_only",
                    "message": (
                        "Aspects and overlays do not reveal compatibility, intent, "
                        "fidelity, or relationship outcomes."
                    ),
                }
            ],
        },
    }
