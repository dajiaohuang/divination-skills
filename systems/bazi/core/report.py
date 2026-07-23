"""Build a bounded evidence report without mutating calculator facts."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from divination_skills.rules import evaluate_rules

from .strength import LINEAGE as STRENGTH_LINEAGE
from .strength import seasonal_support_features

RULES_DIR = Path(__file__).resolve().parents[1] / "rules"


def load_bazi_rules() -> list[dict[str, Any]]:
    """Load reviewed Bazi rules from the repository."""

    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(RULES_DIR.glob("BAZI-*.json"))
    ]


def _matched_rule_ids(findings: list[dict[str, Any]]) -> set[str]:
    return {finding["rule_id"] for finding in findings}


def _explanation(
    *,
    fact_ids: list[str],
    rule_id: str,
    statement: str,
    matched: set[str],
) -> dict[str, Any]:
    if rule_id not in matched:
        raise ValueError(f"Required rule did not match the validated chart: {rule_id}")
    return {"fact_ids": fact_ids, "rule_ids": [rule_id], "statement": statement}


def build_report(chart: dict[str, Any], strength_lineage: str | None = None) -> dict[str, Any]:
    """Return chart plus a fully linked narrative layer.

    Computed facts are deep-copied before rule evaluation, and no rule output is
    merged into that layer. Every explanatory statement has both fact and rule IDs.
    """

    if chart.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid calculator chart is required.")

    report = deepcopy(chart)
    original_facts = deepcopy(chart["computed_facts"])
    rules = load_bazi_rules()
    baseline_rules = [rule for rule in rules if rule["lineage"] != STRENGTH_LINEAGE]
    findings = evaluate_rules(baseline_rules, report)
    matched = _matched_rule_ids(findings)
    facts = report["computed_facts"]

    boundary_rule = (
        "BAZI-CAL-DAY-002"
        if report["normalized_input"]["day_boundary"] == "zi_initial"
        else "BAZI-CAL-DAY-001"
    )
    pillar_rules = {
        "year": "BAZI-CAL-YEAR-001",
        "month": "BAZI-CAL-MONTH-001",
        "day": boundary_rule,
        "hour": "BAZI-CAL-HOUR-001",
    }

    verified_facts = []
    for position in ("year", "month", "day", "hour"):
        pillar = facts["pillars"][position]
        verified_facts.append(
            _explanation(
                fact_ids=[pillar["fact_id"]],
                rule_id=pillar_rules[position],
                statement=f"{position} pillar is {pillar['ganzhi']} under the selected policy.",
                matched=matched,
            )
        )
    day_master = facts["day_master"]
    verified_facts.append(
        _explanation(
            fact_ids=[day_master["fact_id"]],
            rule_id="BAZI-FACT-DAYMASTER-001",
            statement=(
                f"Day master is {day_master['name']} "
                f"({day_master['polarity']} {day_master['element']})."
            ),
            matched=matched,
        )
    )

    symbolic = [
        _explanation(
            fact_ids=[facts["ten_gods"]["fact_id"]],
            rule_id="BAZI-FACT-TENGOD-001",
            statement=(
                "Ten Gods are relational labels calculated from the day stem; "
                "no event claim is added."
            ),
            matched=matched,
        )
    ]
    for relation in facts["branch_relations"]:
        symbolic.append(
            _explanation(
                fact_ids=[relation["fact_id"]],
                rule_id="BAZI-FACT-BRANCH-REL-001",
                statement=(
                    f"Recorded branch relation {relation['type']} connects "
                    f"{', '.join(relation['positions'])}."
                ),
                matched=matched,
            )
        )

    timing: list[dict[str, Any]] = []
    if facts["luck_cycles"] is not None:
        timing.append(
            _explanation(
                fact_ids=[facts["luck_cycles"]["fact_id"]],
                rule_id="BAZI-LUCK-SEQUENCE-001",
                statement=(
                    "Luck-cycle pillars and decimal start ages are method-specific sequence data, "
                    "not event predictions."
                ),
                matched=matched,
            )
        )

    strength_explanations: list[dict[str, Any]] = []
    if strength_lineage is not None:
        if strength_lineage != STRENGTH_LINEAGE:
            raise ValueError(f"Unsupported strength lineage: {strength_lineage}")
        features = seasonal_support_features(report)
        strength_context = deepcopy(report)
        strength_context["analysis_features"] = features
        strength_rules = [rule for rule in rules if rule["lineage"] == STRENGTH_LINEAGE]
        strength_findings = evaluate_rules(strength_rules, strength_context)
        if len(strength_findings) != 1:
            raise AssertionError("Exactly one seasonal-support classifier must match.")
        strength_finding = strength_findings[0]
        findings.extend(strength_findings)
        strength_explanations.append(
            {
                "fact_ids": [
                    facts["day_master"]["fact_id"],
                    facts["pillars"]["month"]["fact_id"],
                    *[pillar["fact_id"] for pillar in facts["pillars"].values()],
                ],
                "rule_ids": [strength_finding["rule_id"]],
                "statement": (
                    f"Explicit {STRENGTH_LINEAGE} score {features['total_score']} is labeled "
                    f"{strength_finding['value']}; this low-confidence label is not a life claim."
                ),
                "features": features,
            }
        )

    report["derived_findings"] = findings
    report["narrative"] = {
        "calculation_basis": [
            _explanation(
                fact_ids=[facts["pillars"]["hour"]["fact_id"]],
                rule_id="BAZI-TIME-CIVIL-001",
                statement=(
                    "Calculation uses the supplied IANA civil time; true solar time is not applied."
                ),
                matched=matched,
            )
        ],
        "verified_facts": verified_facts,
        "symbolic_relationships": symbolic,
        "seasonal_support_path": strength_explanations,
        "method_specific_timing": timing,
        "limitations": [
            (
                "No fixed life event, medical, legal, financial, or compatibility "
                "conclusion is produced."
            ),
            (
                "Strength, structure, climate adjustment, and useful-god selection "
                "require a separately reviewed lineage module."
            ),
        ],
    }
    if report["computed_facts"] != original_facts:
        raise AssertionError("Rule evaluation must not mutate computed facts.")
    return report
