"""Create evidence-linked structural natal explanations."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

PLANET_THEMES = {
    "sun": "identity and vitality",
    "moon": "needs and habitual response",
    "mercury": "thinking and communication",
    "venus": "relating and valuation",
    "mars": "assertion and effort",
    "jupiter": "growth and meaning",
    "saturn": "limits and responsibility",
    "uranus": "change and autonomy",
    "neptune": "imagination and permeability",
    "pluto": "power and deep revision",
}
HOUSE_THEMES = {
    1: "approach and self-presentation",
    2: "resources and priorities",
    3: "learning and local exchange",
    4: "home and foundations",
    5: "creation and play",
    6: "workflows and maintenance",
    7: "one-to-one relationship",
    8: "shared resources and vulnerability",
    9: "worldview and long-distance learning",
    10: "public role and responsibility",
    11: "groups and future aims",
    12: "withdrawal and unseen maintenance",
}
ASPECT_THEMES = {
    "conjunction": "concentrates",
    "sextile": "offers a cooperative opening between",
    "square": "creates friction between",
    "trine": "supports an easy flow between",
    "opposition": "sets up a polarity between",
}


def build_report(chart: dict[str, Any]) -> dict[str, Any]:
    if chart.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Western natal chart is required.")
    report = deepcopy(chart)
    original = deepcopy(chart["computed_facts"])
    placements = []
    findings = []
    house_rule = (
        "WESTERN-HOUSE-WHOLE-001"
        if chart["normalized_input"]["house_system"] == "whole_sign"
        else "WESTERN-HOUSE-EQUAL-001"
    )
    for position in chart["computed_facts"]["positions"]:
        motion = "retrograde apparent motion" if position["retrograde"] else "direct motion"
        placements.append(
            {
                "fact_ids": [position["fact_id"]],
                "rule_ids": [
                    "WESTERN-CAL-POSITION-001",
                    house_rule,
                    "WESTERN-INTERPRET-STRUCTURE-001",
                ],
                "statement": (
                    f"{position['body'].title()} is at {position['degree_in_sign']:.2f}° "
                    f"{position['sign']} in house {position['house']} ({motion}). "
                    f"Reflect on {PLANET_THEMES[position['body']]} through "
                    f"{HOUSE_THEMES[position['house']]}; this is symbolic, not a factual verdict."
                ),
            }
        )
    aspect_explanations = []
    for aspect in chart["computed_facts"]["aspects"]:
        aspect_explanations.append(
            {
                "fact_ids": [aspect["fact_id"]],
                "rule_ids": ["WESTERN-ASPECT-MAJOR-001", "WESTERN-INTERPRET-STRUCTURE-001"],
                "statement": (
                    f"{aspect['body_a'].title()} {aspect['aspect']} {aspect['body_b'].title()} "
                    f"with {aspect['orb_degrees']:.2f}° orb "
                    f"{ASPECT_THEMES[aspect['aspect']]} their symbolic themes."
                ),
            }
        )
    for number, explanation in enumerate([*placements, *aspect_explanations], start=1):
        findings.append(
            {
                "finding_id": f"western.finding.{number:03d}",
                "fact_ids": explanation["fact_ids"],
                "rule_ids": explanation["rule_ids"],
                "confidence": "low",
                "statement": explanation["statement"],
                "source_ids": ["SRC-WESTERN-PROJECT-SPEC-001"],
            }
        )
    angles = chart["computed_facts"]["angles"]
    angle_explanations = [
        {
            "fact_ids": [angles["ascendant"]["fact_id"]],
            "rule_ids": ["WESTERN-CAL-ANGLES-001"],
            "statement": (
                f"Ascendant is {angles['ascendant']['degree_in_sign']:.2f}° "
                f"{angles['ascendant']['sign']}."
            ),
        },
        {
            "fact_ids": [angles["midheaven"]["fact_id"]],
            "rule_ids": ["WESTERN-CAL-ANGLES-001"],
            "statement": (
                f"Midheaven is {angles['midheaven']['degree_in_sign']:.2f}° "
                f"{angles['midheaven']['sign']}."
            ),
        },
    ]
    report["derived_findings"] = findings
    report["narrative"] = {
        "angles": angle_explanations,
        "placements": placements,
        "aspects": aspect_explanations,
        "limitations": [
            "Astrological symbolism is not empirical evidence or a guaranteed prediction.",
            "No unsupported house system, dignity, transit, synastry, or event claim is added.",
        ],
    }
    if report["computed_facts"] != original:
        raise AssertionError("Interpretation must not mutate astronomical facts.")
    return report
