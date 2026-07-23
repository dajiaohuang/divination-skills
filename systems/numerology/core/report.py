from __future__ import annotations

from copy import deepcopy
from typing import Any


def build_report(profile: dict[str, Any]) -> dict[str, Any]:
    if profile.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid numerology profile is required.")
    report = deepcopy(profile)
    original = deepcopy(profile["computed_facts"])
    explanations = []
    for name, fact in profile["computed_facts"].items():
        calculation_rule = (
            "NUMEROLOGY-CAL-DATE-001"
            if name in {"life_path", "birthday"}
            else "NUMEROLOGY-CAL-NAME-001"
        )
        explanations.append(
            {
                "fact_ids": [fact["fact_id"]],
                "rule_ids": [calculation_rule, "NUMEROLOGY-INTERPRET-THEME-001"],
                "statement": (
                    f"{name.replace('_', ' ').title()} reduces through {fact['reduction_steps']} "
                    f"to {fact['value']}; the project theme '{fact['theme']}' is a reflective "
                    "prompt, not an identity fact or prediction."
                ),
            }
        )
    report["derived_findings"] = [
        {
            "finding_id": f"numerology.finding.{index:03d}",
            "fact_ids": item["fact_ids"],
            "rule_ids": item["rule_ids"],
            "confidence": "low",
            "statement": item["statement"],
            "source_ids": ["SRC-NUMEROLOGY-PROJECT-SPEC-001"],
        }
        for index, item in enumerate(explanations, start=1)
    ]
    report["narrative"] = {
        "numbers": explanations,
        "limitations": [
            "Numerology is symbolic and does not measure personality, ability, or future outcomes.",
            "No transliteration, Chaldean mapping, compatibility, or forecast was applied.",
        ],
    }
    if report["computed_facts"] != original:
        raise AssertionError("Interpretation must not mutate number facts.")
    return report
