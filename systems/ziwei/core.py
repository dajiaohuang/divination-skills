"""Experimental, evidence-linked Ziwei structural explanation layer."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from systems.ziwei.analyzer import (
    is_empty_palace,
    palace_stem_transformation_paths,
    surrounded_palaces,
    transformation_paths,
)
from systems.ziwei.engine import CLASSICAL_SOURCE_ID, LINEAGE
from systems.ziwei.terms import PALACE_TERM_IDS, display_label


def analyze_core(chart: dict[str, Any], *, locale: str = "zh-Hans") -> dict[str, Any]:
    if chart.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Ziwei chart is required.")
    if chart.get("normalized_input", {}).get("lineage") != LINEAGE:
        raise ValueError(f"Expected lineage {LINEAGE}.")
    original = deepcopy(chart["computed_facts"])
    sections = []
    findings = []
    for item in chart["computed_facts"]["palaces"]:
        term_id = PALACE_TERM_IDS[item["name"]]
        surrounded = surrounded_palaces(chart, item["index"])
        empty = is_empty_palace(chart, item["index"])
        star_fact_ids = [
            star["fact_id"]
            for group in ("majorStars", "minorStars", "auxiliaryStars")
            for star in item[group]
        ]
        fact_ids = [item["fact_id"], *star_fact_ids, *surrounded["fact_ids"]]
        rule_ids = ["ZIWEI-CORE-STRUCTURE-001", "ZIWEI-PALACE-SURROUNDED-001"]
        finding_id = f"ziwei.finding.core.palace-{item['index']:03d}"
        findings.append(
            {
                "finding_id": finding_id,
                "finding_type": "ziwei.structural_palace_summary",
                "term_id": term_id,
                "fact_ids": sorted(set(fact_ids)),
                "rule_ids": rule_ids,
                "source_ids": [
                    "SRC-ZIWEI-PROJECT-SPEC-001",
                    CLASSICAL_SOURCE_ID,
                ],
                "confidence": "medium",
                "status": "experimental",
            }
        )
        major_names = [star["name"] for star in item["majorStars"]]
        sections.append(
            {
                "section_id": f"ziwei.core.palace-{item['index']:03d}",
                "term_id": term_id,
                "label": display_label(term_id, locale),
                "statement": (
                    f"{display_label(term_id, locale)}位于{item['earthlyBranch']}宫；"
                    f"主星为{'、'.join(major_names) if major_names else '空宫'}。"
                    "三方四正与星曜位置仅作为结构证据，不代表固定事件或吉凶。"
                ),
                "is_empty_major_palace": empty["is_empty_major_palace"],
                "fact_ids": sorted(set(fact_ids)),
                "rule_ids": rule_ids,
                "source_ids": [
                    "SRC-ZIWEI-PROJECT-SPEC-001",
                    CLASSICAL_SOURCE_ID,
                ],
                "limitations": [
                    "No fixed event is inferred from this structure.",
                    (
                        "Brightness is not interpreted because the selected lineage "
                        "does not provide it."
                    ),
                ],
            }
        )
    paths = transformation_paths(chart)
    palace_paths = palace_stem_transformation_paths(chart)
    if chart["computed_facts"] != original:
        raise AssertionError("Core analysis must not mutate natal facts.")
    return {
        "schema_version": "0.4.0",
        "status": "experimental",
        "system": "ziwei",
        "lineage": LINEAGE,
        "locale": locale,
        "findings": findings,
        "sections": sections,
        "transformation_paths": paths,
        "palace_stem_transformation_paths": palace_paths,
        "validation": {
            "status": "valid",
            "citation_completeness": 1.0,
            "fact_reference_validity": 1.0,
            "warnings": [
                {
                    "code": "expert_acceptance_pending",
                    "message": (
                        "The explanation layer remains experimental until independent "
                        "practitioner acceptance and domain sign-off are recorded."
                    ),
                }
            ],
        },
    }
