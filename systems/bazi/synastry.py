"""Directional and symmetric Bazi comparison facts."""

from __future__ import annotations

from typing import Any

from divination_skills.contracts import stable_identifier

from systems.bazi.calculator.engine import PAIR_RELATIONS, STEMS, _ten_god


def _chart_id(chart: dict[str, Any]) -> str:
    return stable_identifier(
        "CHART-BAZI",
        {"engine": chart["engine"], "normalized_input": chart["normalized_input"]},
    )


def _directional(
    source: dict[str, Any],
    target: dict[str, Any],
    label: str,
) -> list[dict[str, Any]]:
    source_day = source["computed_facts"]["pillars"]["day"]["stem"]["name"]
    day_index = STEMS.index(source_day)
    facts = []
    for position, pillar in target["computed_facts"]["pillars"].items():
        target_stem = pillar["stem"]["name"]
        facts.append(
            {
                "fact_id": f"bazi.synastry.{label}.{position}.visible-ten-god",
                "direction": label,
                "source_day_master_fact_id": source["computed_facts"]["day_master"]["fact_id"],
                "target_pillar_fact_id": pillar["fact_id"],
                "target_position": position,
                "target_stem": target_stem,
                "ten_god": _ten_god(day_index, STEMS.index(target_stem)),
                "rule_ids": ["BAZI-SYNASTRY-DIRECTIONAL-001"],
                "source_ids": ["SRC-BAZI-PROJECT-SPEC-001"],
            }
        )
    return facts


def compare_charts(chart_a: dict[str, Any], chart_b: dict[str, Any]) -> dict[str, Any]:
    for label, chart in (("A", chart_a), ("B", chart_b)):
        if chart.get("validation", {}).get("status") != "valid":
            raise ValueError(f"Chart {label} must be valid.")
    symmetric = []
    for position_a, pillar_a in chart_a["computed_facts"]["pillars"].items():
        branch_a = pillar_a["branch"]["name"]
        for position_b, pillar_b in chart_b["computed_facts"]["pillars"].items():
            branch_b = pillar_b["branch"]["name"]
            for relation, pairs in PAIR_RELATIONS.items():
                if tuple(sorted((branch_a, branch_b))) in {
                    tuple(sorted(pair)) for pair in pairs
                }:
                    symmetric.append(
                        {
                            "fact_id": f"bazi.synastry.symmetric.{len(symmetric) + 1:03d}",
                            "relation": relation,
                            "a_position": position_a,
                            "a_branch": branch_a,
                            "b_position": position_b,
                            "b_branch": branch_b,
                            "rule_ids": ["BAZI-SYNASTRY-SYMMETRIC-001"],
                            "source_ids": ["SRC-BAZI-PROJECT-SPEC-001"],
                        }
                    )
    return {
        "schema_version": "0.2.0",
        "system": "bazi",
        "lineage": "ziping-calculation-baseline",
        "chart_refs": {"A": _chart_id(chart_a), "B": _chart_id(chart_b)},
        "directional": {
            "A_to_B": _directional(chart_a, chart_b, "A_to_B"),
            "B_to_A": _directional(chart_b, chart_a, "B_to_A"),
        },
        "symmetric": symmetric,
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "structural_relationship_only",
                    "message": (
                        "Cross-chart facts do not reveal compatibility, intent, fidelity, "
                        "or relationship outcomes."
                    ),
                }
            ],
        },
    }
