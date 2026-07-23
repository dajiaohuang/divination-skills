"""Explicit, bounded Liuyao judgment rule packs."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from systems.liuyao.engine import (
    BRANCH_ELEMENT,
    BRANCHES,
    ELEMENT_CONTROLS,
    ELEMENT_GENERATES,
    NAJIA,
    SOURCE_ID,
    six_relative,
)

LINEAGE = "wen-wang-najia-project-judgment-v0.2"
QUESTION_PACKS = {
    "self": {"selector": "role", "value": "shi"},
    "counterpart": {"selector": "role", "value": "ying"},
    "career": {"selector": "six_relative", "value": "官鬼"},
    "finances": {"selector": "six_relative", "value": "妻财"},
    "documents": {"selector": "six_relative", "value": "父母"},
    "children_relief": {"selector": "six_relative", "value": "子孙"},
    "peers_competition": {"selector": "six_relative", "value": "兄弟"},
}
CLASH_BRANCH = dict(zip(BRANCHES, BRANCHES[6:] + BRANCHES[:6], strict=True))


def _element_relation(origin: str, target: str) -> str:
    if origin == target:
        return "same"
    if ELEMENT_GENERATES[origin] == target:
        return "origin_generates_target"
    if ELEMENT_GENERATES[target] == origin:
        return "target_generates_origin"
    if ELEMENT_CONTROLS[origin] == target:
        return "origin_controls_target"
    if ELEMENT_CONTROLS[target] == origin:
        return "target_controls_origin"
    raise AssertionError("Unreachable five-element relation.")


def _context_score(line_element: str, context_element: str) -> tuple[int, str]:
    relation = _element_relation(context_element, line_element)
    return {
        "same": (2, "same_element"),
        "origin_generates_target": (1, "context_generates_line"),
        "target_generates_origin": (-1, "line_generates_context"),
        "origin_controls_target": (-2, "context_controls_line"),
        "target_controls_origin": (0, "line_controls_context"),
    }[relation]


def _changed_assignments(chart: dict[str, Any]) -> list[str]:
    changed = chart["computed_facts"]["changed_hexagram"]
    lower = changed["lower_trigram"]["id"]
    upper = changed["upper_trigram"]["id"]
    return [*NAJIA[lower]["inner"], *NAJIA[upper]["outer"]]


def analyze(
    chart: dict[str, Any],
    *,
    question_category: str,
    include_timing: bool = False,
) -> dict[str, Any]:
    """Apply only the requested project judgment packs to a valid structural chart."""

    if chart.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Liuyao chart is required.")
    if question_category not in QUESTION_PACKS:
        raise ValueError(
            "question_category must be one of: " + ", ".join(QUESTION_PACKS)
        )
    if not isinstance(include_timing, bool):
        raise ValueError("include_timing must be boolean.")

    original = deepcopy(chart["computed_facts"])
    facts = chart["computed_facts"]
    pack = QUESTION_PACKS[question_category]
    candidates = [
        line
        for line in facts["lines"]
        if line.get(pack["selector"]) == pack["value"]
    ]
    status = "structural_candidates" if candidates else "underdetermined"
    selected_ids = [line["fact_id"] for line in candidates]

    month_branch = facts["calendar_context"]["month_commander"]["name"]
    day_branch = facts["calendar_context"]["day_pillar"]["branch"]["name"]
    strength = []
    for line in facts["lines"]:
        month_score, month_relation = _context_score(
            line["najia"]["element"],
            BRANCH_ELEMENT[month_branch],
        )
        day_score, day_relation = _context_score(
            line["najia"]["element"],
            BRANCH_ELEMENT[day_branch],
        )
        adjustments = []
        total = month_score + day_score
        if line["is_void"]:
            adjustments.append({"reason": "void", "delta": -2})
            total -= 2
        if line["moving"]:
            adjustments.append({"reason": "moving", "delta": 1})
            total += 1
        strength.append(
            {
                "fact_id": f"liuyao.judgment.strength.line-{line['position_from_bottom']:03d}",
                "line_fact_id": line["fact_id"],
                "month_relation": month_relation,
                "day_relation": day_relation,
                "adjustments": adjustments,
                "structural_score": total,
                "band": "supported" if total >= 2 else "mixed" if total >= 0 else "strained",
                "rule_ids": ["LIUYAO-STRENGTH-PROJECT-001"],
                "source_ids": [SOURCE_ID],
            }
        )

    changed_assignments = _changed_assignments(chart)
    changes = []
    palace_element = facts["palace"]["element"]
    for line, changed_ganzhi in zip(facts["lines"], changed_assignments, strict=True):
        if not line["moving"]:
            continue
        changed_branch = changed_ganzhi[1]
        changed_element = BRANCH_ELEMENT[changed_branch]
        changes.append(
            {
                "fact_id": f"liuyao.judgment.change.line-{line['position_from_bottom']:03d}",
                "line_fact_id": line["fact_id"],
                "position_from_bottom": line["position_from_bottom"],
                "original_branch": line["najia"]["branch"],
                "original_element": line["najia"]["element"],
                "changed_najia": changed_ganzhi,
                "changed_branch": changed_branch,
                "changed_element": changed_element,
                "changed_six_relative": six_relative(palace_element, changed_element),
                "element_relation": _element_relation(
                    line["najia"]["element"],
                    changed_element,
                ),
                "rule_ids": ["LIUYAO-MOVING-CHANGE-001"],
                "source_ids": [SOURCE_ID],
            }
        )

    timing_candidates = []
    if include_timing:
        changed_by_line = {item["line_fact_id"]: item for item in changes}
        for line in candidates:
            branches = [
                {"branch": line["najia"]["branch"], "trigger": "same_as_use_line"},
                {
                    "branch": CLASH_BRANCH[line["najia"]["branch"]],
                    "trigger": "clashes_use_line",
                },
            ]
            if line["fact_id"] in changed_by_line:
                branches.append(
                    {
                        "branch": changed_by_line[line["fact_id"]]["changed_branch"],
                        "trigger": "same_as_changed_line",
                    }
                )
            for item in branches:
                timing_candidates.append(
                    {
                        "fact_id": (
                            f"liuyao.judgment.timing.{len(timing_candidates) + 1:03d}"
                        ),
                        "use_line_fact_id": line["fact_id"],
                        **item,
                        "precision": "branch_only",
                        "rule_ids": ["LIUYAO-TIMING-CANDIDATE-001"],
                        "source_ids": [SOURCE_ID],
                    }
                )

    if chart["computed_facts"] != original:
        raise AssertionError("Judgment must not mutate structural chart facts.")
    return {
        "schema_version": "0.2.0",
        "system": "liuyao",
        "lineage": LINEAGE,
        "question_category": question_category,
        "status": status,
        "use_deity": {
            "selector": pack,
            "candidate_line_fact_ids": selected_ids,
            "rule_ids": ["LIUYAO-USE-DEITY-PROJECT-001"],
            "source_ids": [SOURCE_ID],
        },
        "line_strength": strength,
        "moving_changes": changes,
        "timing_pack": {
            "enabled": include_timing,
            "candidates": timing_candidates,
            "precision": "branch_only" if include_timing else None,
        },
        "conclusions": [
            {
                "conclusion_id": "liuyao.judgment.structure.001",
                "statement": (
                    "The result lists project-lineage structural candidates only; "
                    "it does not assert an outcome or event date."
                ),
                "fact_ids": selected_ids,
                "rule_ids": [
                    "LIUYAO-USE-DEITY-PROJECT-001",
                    "LIUYAO-STRENGTH-PROJECT-001",
                    "LIUYAO-MOVING-CHANGE-001",
                ],
                "source_ids": [SOURCE_ID],
                "support": ["Candidates follow the explicitly selected question-category pack."],
                "counterevidence": [
                    "Other Liuyao lineages may select or prioritize 用神 differently."
                ],
                "limitations": [
                    "Scores are transparent project heuristics pending practitioner review.",
                    "Timing candidates are branches, not promised dates or outcomes.",
                ],
            }
        ],
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "judgment_pending_domain_review",
                    "message": (
                        "This project rule pack is not an accepted universal Liuyao standard."
                    ),
                }
            ],
        },
    }
