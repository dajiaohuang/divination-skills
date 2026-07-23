"""Evaluate structured rules without allowing them to mutate computed facts."""

from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from typing import Any

MISSING = object()


def get_path(context: dict[str, Any], path: str, default: Any = MISSING) -> Any:
    """Resolve a dot-separated object path."""

    value: Any = context
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return default
        value = value[part]
    return value


def predicate_matches(predicate: dict[str, Any], context: dict[str, Any]) -> bool:
    """Evaluate one schema-approved predicate."""

    actual = get_path(context, predicate["fact_path"])
    operator = predicate["operator"]
    expected = predicate.get("value")
    if operator == "exists":
        return actual is not MISSING
    if operator == "absent":
        return actual is MISSING
    if actual is MISSING:
        return False
    if operator == "eq":
        return actual == expected
    if operator == "neq":
        return actual != expected
    if operator == "gt":
        return actual > expected
    if operator == "gte":
        return actual >= expected
    if operator == "lt":
        return actual < expected
    if operator == "lte":
        return actual <= expected
    if operator == "in":
        return actual in expected
    if operator == "not_in":
        return actual not in expected
    if operator == "contains":
        return expected in actual
    if operator == "intersects":
        return bool(set(actual).intersection(expected))
    raise ValueError(f"Unsupported predicate operator: {operator}")


def _conditions_match(conditions: Iterable[dict[str, Any]], context: dict[str, Any]) -> bool:
    return all(predicate_matches(condition, context) for condition in conditions)


def evaluate_rule(rule: dict[str, Any], context: dict[str, Any]) -> list[dict[str, Any]]:
    """Return evidence-bearing findings for one matching rule."""

    if not _conditions_match(rule["conditions"], context):
        return []
    exception_effects = [
        exception["effect"]
        for exception in rule.get("exceptions", [])
        if _conditions_match(exception["when"], context)
    ]
    if "skip" in exception_effects:
        return []

    evidence = [
        {
            "path": condition["fact_path"],
            "value": None
            if get_path(context, condition["fact_path"]) is MISSING
            else deepcopy(get_path(context, condition["fact_path"])),
        }
        for condition in rule["conditions"]
    ]
    findings: list[dict[str, Any]] = []
    for index, conclusion in enumerate(rule["conclusions"], start=1):
        finding = {
            "finding_id": f"{rule['rule_id']}:{index}",
            "rule_id": rule["rule_id"],
            "rule_version": rule["version"],
            "lineage": rule["lineage"],
            "finding_type": conclusion["finding_type"],
            "output_path": conclusion["output_path"],
            "value": deepcopy(conclusion["value"]),
            "confidence": conclusion["confidence"],
            "evidence": evidence,
            "sources": deepcopy(rule["sources"]),
            "exception_effects": exception_effects,
        }
        if "downgrade" in exception_effects:
            finding["confidence"] = "low"
        findings.append(finding)
    return findings


def evaluate_rules(
    rules: Iterable[dict[str, Any]],
    context: dict[str, Any],
    allowed_statuses: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Evaluate reviewed rules in priority order and return a separate finding layer."""

    statuses = allowed_statuses or {"tested", "production"}
    selected = [rule for rule in rules if rule.get("status") in statuses]
    findings: list[dict[str, Any]] = []
    for rule in sorted(selected, key=lambda item: (-item["priority"], item["rule_id"])):
        findings.extend(evaluate_rule(rule, context))
    return findings
