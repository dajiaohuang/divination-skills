"""Shared product views that select existing facts without adding calculations."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

HIGH_IMPACT_DOMAINS = {
    "medical",
    "legal",
    "financial",
    "employment_selection",
    "safety",
}


def _source_ids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        if isinstance(value.get("source_ids"), list):
            found.update(value["source_ids"])
        for child in value.values():
            found.update(_source_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_source_ids(child))
    return found


def _bazi_selection(chart: dict[str, Any], view: str) -> tuple[list[str], list[str]]:
    facts = chart["computed_facts"]
    pillars = facts["pillars"]
    if view == "career":
        ids = [pillars["month"]["fact_id"], pillars["day"]["fact_id"]]
        if facts.get("luck_cycles"):
            ids.append(facts["luck_cycles"]["fact_id"])
        return ids, ["BAZI-FACT-TENGOD-001", "BAZI-LUCK-SEQUENCE-001"]
    ids = [pillar["fact_id"] for pillar in pillars.values()]
    ids.extend(item["fact_id"] for item in facts["branch_relations"])
    return ids, ["BAZI-FACT-BRANCH-REL-001", "BAZI-FACT-TENGOD-001"]


def _western_selection(chart: dict[str, Any], view: str) -> tuple[list[str], list[str]]:
    facts = chart["computed_facts"]
    ids = [item["fact_id"] for item in facts["positions"]]
    ids.extend(item["fact_id"] for item in facts["aspects"])
    if view == "career":
        ids.append(facts["angles"]["midheaven"]["fact_id"])
        ids.extend(item["fact_id"] for item in facts["house_cusps"])
    return ids, ["WESTERN-CAL-POSITION-001", "WESTERN-ASPECT-MAJOR-001"]


def _ziwei_selection(chart: dict[str, Any], view: str) -> tuple[list[str], list[str]]:
    target_name = "官禄" if view == "career" else "夫妻"
    palaces = chart["computed_facts"]["palaces"]
    target = next(item for item in palaces if item["name"] == target_name)
    indices = (
        target["index"],
        (target["index"] + 4) % 12,
        (target["index"] + 6) % 12,
        (target["index"] + 8) % 12,
    )
    ids = [palaces[index]["fact_id"] for index in indices]
    ids.extend(
        star["fact_id"]
        for index in indices
        for group in ("majorStars", "minorStars", "auxiliaryStars")
        for star in palaces[index][group]
    )
    return ids, ["ZIWEI-CORE-STRUCTURE-001", "ZIWEI-PALACE-SURROUNDED-001"]


SELECTORS = {
    "bazi": _bazi_selection,
    "western-astrology": _western_selection,
    "ziwei": _ziwei_selection,
}


def build_product_view(
    *,
    system: str,
    chart: dict[str, Any],
    view: str,
    high_impact_domain: str | None = None,
) -> dict[str, Any]:
    """Build career/relationship selection using only pre-existing chart facts."""

    if view not in {"career", "relationship"}:
        raise ValueError("view must be career or relationship.")
    if system not in SELECTORS:
        raise ValueError(f"Unsupported product-view system: {system}")
    if chart.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid chart is required.")
    if high_impact_domain is not None and high_impact_domain not in HIGH_IMPACT_DOMAINS:
        raise ValueError(f"Unsupported high-impact domain: {high_impact_domain}")
    original = deepcopy(chart["computed_facts"])
    fact_ids, rule_ids = SELECTORS[system](chart, view)
    sources = sorted(_source_ids(chart["computed_facts"]))
    if chart["computed_facts"] != original:
        raise AssertionError("Product views must not mutate chart facts.")
    downgraded = high_impact_domain is not None
    return {
        "schema_version": "0.1.0",
        "system": system,
        "view": view,
        "mode": "reflective_information_only" if downgraded else "structural_summary",
        "conclusions": [
            {
                "conclusion_id": f"{system}.{view}.structure.001",
                "statement": (
                    f"Selected {len(fact_ids)} existing {system} facts for the {view} view. "
                    "The view introduces no new calculation or guaranteed outcome."
                ),
                "fact_ids": sorted(set(fact_ids)),
                "rule_ids": sorted(set(rule_ids)),
                "source_ids": sources,
                "support": [
                    "All selected facts already exist in the validated source chart."
                ],
                "counterevidence": [
                    "The selected system does not establish real-world causation or outcome."
                ],
                "limitations": [
                    "No hiring, firing, investment, diagnosis, legal, or safety decision is made.",
                    "Third-party intent, fidelity, and private state are not inferred.",
                ],
            }
        ],
        "high_impact": {
            "domain": high_impact_domain,
            "downgraded": downgraded,
            "policy": "reflective_information_only" if downgraded else "not_applicable",
        },
    }


def build_timing_view(
    *,
    system: str,
    timing: dict[str, Any],
    high_impact_domain: str | None = None,
) -> dict[str, Any]:
    """Wrap an existing timing result without adding events or calculations."""

    if system not in SELECTORS:
        raise ValueError(f"Unsupported timing-view system: {system}")
    if timing.get("system") != system:
        raise ValueError("Timing result system does not match the requested system.")
    if timing.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid timing result is required.")
    if high_impact_domain is not None and high_impact_domain not in HIGH_IMPACT_DOMAINS:
        raise ValueError(f"Unsupported high-impact domain: {high_impact_domain}")
    original = deepcopy(timing)
    entries = timing.get("timeline", {}).get("entries", [])
    if not entries:
        raise ValueError("The timing result contains no timeline entries.")
    fact_ids = sorted(
        {
            fact_id
            for entry in entries
            for fact_id in entry.get("fact_ids", [])
        }
    )
    rule_ids = sorted(
        {
            rule_id
            for entry in entries
            for rule_id in entry.get("rule_ids", [])
        }
    )
    if not fact_ids or not rule_ids:
        raise ValueError("Timeline entries must cite facts and rules.")
    if timing != original:
        raise AssertionError("Timing views must not mutate timing facts.")
    downgraded = high_impact_domain is not None
    return {
        "schema_version": "0.1.0",
        "system": system,
        "view": "timing",
        "mode": "reflective_information_only" if downgraded else "structural_timeline",
        "conclusions": [
            {
                "conclusion_id": f"{system}.timing.structure.001",
                "statement": (
                    f"Selected {len(entries)} existing timeline entries for the timing view. "
                    "No real-world event or guaranteed outcome is inferred."
                ),
                "fact_ids": fact_ids,
                "rule_ids": rule_ids,
                "source_ids": sorted(_source_ids(timing)),
                "support": [
                    "Each displayed interval already exists in the validated timing result."
                ],
                "counterevidence": [
                    "A calculated symbolic interval does not establish that an event will occur."
                ],
                "limitations": [
                    "Boundary policies and the selected lineage limit every interval.",
                    "No medical, legal, financial, employment, or safety action is recommended.",
                ],
            }
        ],
        "timeline": deepcopy(timing["timeline"]),
        "high_impact": {
            "domain": high_impact_domain,
            "downgraded": downgraded,
            "policy": "reflective_information_only" if downgraded else "not_applicable",
        },
    }


def answer_fact_question(
    *,
    system: str,
    chart: dict[str, Any],
    requested_fact_ids: list[str],
    high_impact_domain: str | None = None,
) -> dict[str, Any]:
    """Answer QA by fact ID only; no free-form rule invention is possible."""

    if system not in SELECTORS:
        raise ValueError(f"Unsupported QA system: {system}")
    if not requested_fact_ids:
        raise ValueError("At least one requested_fact_id is required.")
    if high_impact_domain is not None and high_impact_domain not in HIGH_IMPACT_DOMAINS:
        raise ValueError(f"Unsupported high-impact domain: {high_impact_domain}")

    index: dict[str, dict[str, Any]] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            fact_id = value.get("fact_id")
            if isinstance(fact_id, str):
                index[fact_id] = deepcopy(value)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(chart.get("computed_facts", {}))
    matched = [fact_id for fact_id in requested_fact_ids if fact_id in index]
    missing = [fact_id for fact_id in requested_fact_ids if fact_id not in index]
    return {
        "schema_version": "0.1.0",
        "system": system,
        "view": "qa",
        "status": "answered" if matched else "unsupported",
        "requested_fact_ids": requested_fact_ids,
        "matched_fact_ids": matched,
        "missing_fact_ids": missing,
        "facts": [index[fact_id] for fact_id in matched],
        "mode": (
            "reflective_information_only"
            if high_impact_domain is not None
            else "fact_lookup"
        ),
        "limitations": [
            "No fact or rule absent from the supplied chart is invented.",
            "A fact lookup cannot establish causation, guaranteed outcomes, or high-impact advice.",
        ],
    }
