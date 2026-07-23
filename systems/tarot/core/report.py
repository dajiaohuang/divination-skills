"""Interpret validated draw facts without modifying or predicting beyond them."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from systems.tarot.draw.engine import load_deck

POSITION_PROMPTS = {
    "focus": "Use this theme as a reflective focus.",
    "situation": "Consider how this theme describes the current situation.",
    "challenge": "Consider where this theme may complicate or test the situation.",
    "guidance": "Consider one small action or question suggested by this theme.",
    "option_a": "Use this theme to examine option A without treating it as a verdict.",
    "option_b": "Use this theme to examine option B without treating it as a verdict.",
    "decision_focus": "Use this theme to identify the value or tradeoff needing attention.",
}


def build_report(draw: dict[str, Any]) -> dict[str, Any]:
    if draw.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Tarot draw is required.")
    report = deepcopy(draw)
    original = deepcopy(draw["computed_facts"])
    deck = {card["card_id"]: card for card in load_deck()["cards"]}
    findings = []
    explanations = []

    for number, fact in enumerate(report["computed_facts"]["cards"], start=1):
        card = deck[fact["card_id"]]
        orientation_rule = (
            "TAROT-ORIENTATION-REVERSED-001"
            if fact["orientation"] == "reversed"
            else "TAROT-ORIENTATION-UPRIGHT-001"
        )
        keywords = card[fact["orientation"]]
        position_prompt = POSITION_PROMPTS.get(
            fact["position"],
            "Use this position as a bounded reflective prompt.",
        )
        finding_id = f"tarot.finding.card.{number:03d}"
        findings.append(
            {
                "finding_id": finding_id,
                "fact_ids": [fact["fact_id"]],
                "rule_ids": [orientation_rule, "TAROT-POSITION-001"],
                "position": fact["position"],
                "card_id": fact["card_id"],
                "orientation": fact["orientation"],
                "keywords": keywords,
                "confidence": "low",
                "source_ids": ["SRC-TAROT-DECK-SPEC-001"],
            }
        )
        explanations.append(
            {
                "fact_ids": [fact["fact_id"]],
                "rule_ids": [orientation_rule, "TAROT-POSITION-001"],
                "statement": (
                    f"{fact['position']}: {fact['name']} {fact['orientation']} highlights "
                    f"{', '.join(keywords)}. "
                    f"{position_prompt}"
                ),
            }
        )

    sequence_fact_ids = [fact["fact_id"] for fact in report["computed_facts"]["cards"]]
    sequence = {
        "fact_ids": sequence_fact_ids,
        "rule_ids": ["TAROT-NARRATIVE-001"],
        "statement": (
            "Read the positions in their listed order as prompts for reflection; "
            "the sequence does not establish hidden facts or a fixed future."
        ),
    }
    findings.append(
        {
            "finding_id": "tarot.finding.sequence.001",
            "fact_ids": sequence_fact_ids,
            "rule_ids": ["TAROT-NARRATIVE-001"],
            "confidence": "low",
            "value": "reflective_not_predictive",
            "source_ids": ["SRC-TAROT-DECK-SPEC-001"],
        }
    )
    report["derived_findings"] = findings
    report["narrative"] = {
        "cards": explanations,
        "sequence": sequence,
        "limitations": [
            "This is symbolic reflection, not evidence or a guaranteed prediction.",
            (
                "For high-impact decisions, use relevant qualified professional advice "
                "and real-world evidence."
            ),
        ],
    }
    if report["computed_facts"] != original:
        raise AssertionError("Tarot interpretation must not mutate draw facts.")
    return report
