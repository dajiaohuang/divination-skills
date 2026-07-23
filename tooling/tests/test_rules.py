from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from divination_skills.rules import evaluate_rule, evaluate_rules, predicate_matches

ROOT = Path(__file__).resolve().parents[2]


def load_rule(name: str) -> dict:
    path = ROOT / "common" / "examples" / "rules" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_predicate_operators() -> None:
    context = {"facts": {"number": 3, "items": ["a", "b"]}}
    assert predicate_matches({"fact_path": "facts.number", "operator": "gte", "value": 3}, context)
    assert predicate_matches(
        {"fact_path": "facts.items", "operator": "contains", "value": "a"}, context
    )
    assert predicate_matches(
        {"fact_path": "facts.items", "operator": "intersects", "value": ["b", "c"]},
        context,
    )
    assert predicate_matches({"fact_path": "facts.missing", "operator": "absent"}, context)


def test_evaluation_emits_evidence_without_mutating_context() -> None:
    rule = load_rule("EXAMPLE-CAL-001")
    context = {"normalized_input": {"boundary_policy": "later_interval", "boundary_known": True}}
    original = deepcopy(context)
    findings = evaluate_rule(rule, context)
    assert context == original
    assert findings[0]["rule_id"] == "EXAMPLE-CAL-001"
    assert findings[0]["evidence"] == [
        {"path": "normalized_input.boundary_policy", "value": "later_interval"}
    ]


def test_exception_can_require_review_or_skip() -> None:
    rule = load_rule("EXAMPLE-CAL-001")
    context = {"normalized_input": {"boundary_policy": "later_interval", "boundary_known": False}}
    findings = evaluate_rule(rule, context)
    assert findings[0]["exception_effects"] == ["require_review"]
    skip_rule = deepcopy(rule)
    skip_rule["exceptions"][0]["effect"] = "skip"
    assert evaluate_rule(skip_rule, context) == []


def test_proposed_and_rejected_rules_are_not_evaluated_by_default() -> None:
    tested = load_rule("EXAMPLE-CAL-001")
    proposed = deepcopy(tested)
    proposed["rule_id"] = "EXAMPLE-CAL-999"
    proposed["status"] = "proposed"
    context = {"normalized_input": {"boundary_policy": "later_interval", "boundary_known": True}}
    findings = evaluate_rules([proposed, tested], context)
    assert [finding["rule_id"] for finding in findings] == ["EXAMPLE-CAL-001"]
