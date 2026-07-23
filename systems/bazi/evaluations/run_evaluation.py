"""Generate the deterministic layered Bazi v0.1 evaluation report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from divination_skills.evaluation import (
    collect_fact_ids,
    collect_narrative_claims,
    corpus_sha256,
    ratio_metric,
)

from systems.bazi.calculator.comparator import sxtwl_modern_reference
from systems.bazi.calculator.engine import calculate_chart
from systems.bazi.core.report import build_report, load_bazi_rules

SYSTEM = Path(__file__).resolve().parents[1]
REPORT_PATH = Path(__file__).resolve().parent / "EVALUATION_REPORT.json"


def _load_cases() -> tuple[list[Path], list[dict[str, Any]]]:
    paths = sorted((SYSTEM / "tests" / "golden").glob("*.json"))
    return paths, [json.loads(path.read_text(encoding="utf-8")) for path in paths]


def _simple_pillars(chart: dict[str, Any]) -> dict[str, str]:
    return {
        position: pillar["ganzhi"]
        for position, pillar in chart["computed_facts"]["pillars"].items()
    }


def evaluate() -> dict[str, Any]:
    paths, cases = _load_cases()
    known_rules = {rule["rule_id"]: rule for rule in load_bazi_rules()}
    exact_cases = 0
    independent_matches = 0
    independent_compared = 0
    exclusions = []
    required_hits = 0
    required_total = 0
    cited_rule_total = 0
    unknown_rule_total = 0
    cross_system_total = 0
    claim_total = 0
    cited_claim_total = 0
    fact_reference_total = 0
    valid_fact_reference_total = 0

    for case in cases:
        chart = calculate_chart(case["raw_input"])
        pillars = _simple_pillars(chart)
        if pillars == case["expected_output"]["computed_facts"]["pillars"]:
            exact_cases += 1

        local_date = case["raw_input"]["local_datetime"][:10]
        boundary_dates = {
            chart["computed_facts"]["previous_month_boundary"]["beijing_datetime"][:10],
            chart["computed_facts"]["next_month_boundary"]["beijing_datetime"][:10],
        }
        if local_date in boundary_dates:
            exclusions.append(
                {
                    "case_id": case["case_id"],
                    "reason": (
                        "sxtwl-modern comparator exposes day-level year/month boundaries; "
                        "the case falls on a Jie calendar date."
                    ),
                }
            )
        else:
            independent_compared += 1
            if sxtwl_modern_reference(case["raw_input"]) == pillars:
                independent_matches += 1

        report = build_report(chart)
        claims = collect_narrative_claims(report["narrative"])
        fact_ids = collect_fact_ids(report["computed_facts"])
        cited_rule_ids = {rule_id for claim in claims for rule_id in claim.get("rule_ids", [])}
        cited_rule_ids.update(
            finding["rule_id"]
            for finding in report["derived_findings"]
            if isinstance(finding.get("rule_id"), str)
        )
        required = set(case["must_match_rules"])
        required_hits += len(required.intersection(cited_rule_ids))
        required_total += len(required)

        for claim in claims:
            claim_total += 1
            fact_refs = claim.get("fact_ids", [])
            rule_refs = claim.get("rule_ids", [])
            if fact_refs and rule_refs:
                cited_claim_total += 1
            fact_reference_total += len(fact_refs)
            valid_fact_reference_total += sum(ref in fact_ids for ref in fact_refs)
            cited_rule_total += len(rule_refs)
            unknown_rule_total += sum(ref not in known_rules for ref in rule_refs)
            cross_system_total += sum(not ref.startswith("BAZI-") for ref in rule_refs)

    candidates = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((SYSTEM / "evaluations" / "expert_candidates").glob("*.json"))
    ]
    accepted = sum(
        candidate["review"]["status"] == "reviewed"
        and candidate["review"]["decision"] == "accepted"
        for candidate in candidates
    )
    signoffs = json.loads((SYSTEM / "reviews" / "release-signoff.json").read_text(encoding="utf-8"))
    signoff_failures = [
        f"signoff:{item['role']}" for item in signoffs["signoffs"] if item["status"] != "accepted"
    ]

    layers = {
        "calculation": {
            "golden_case_exact_consistency": ratio_metric(
                exact_cases,
                len(cases),
                threshold=1.0,
                comparison="minimum",
                evidence=["systems/bazi/tests/golden", "systems/bazi/tests/test_golden_replay.py"],
            ),
            "independent_comparator_consistency": ratio_metric(
                independent_matches,
                independent_compared,
                threshold=1.0,
                comparison="minimum",
                evidence=[
                    "systems/bazi/calculator/comparator.py:sxtwl_modern_reference",
                    "systems/bazi/tests/test_golden_replay.py",
                ],
            ),
        },
        "rules": {
            "required_rule_recall": ratio_metric(
                required_hits,
                required_total,
                threshold=1.0,
                comparison="minimum",
                evidence=["systems/bazi/tests/golden", "systems/bazi/core/report.py"],
            ),
            "unknown_rule_misuse_rate": ratio_metric(
                unknown_rule_total,
                cited_rule_total,
                threshold=0.0,
                comparison="maximum",
                evidence=["systems/bazi/rules", "systems/bazi/core/report.py"],
            ),
        },
        "narrative": {
            "citation_completeness": ratio_metric(
                cited_claim_total,
                claim_total,
                threshold=1.0,
                comparison="minimum",
                evidence=["systems/bazi/core/report.py", "systems/bazi/core/tests/test_report.py"],
            ),
            "fact_reference_validity": ratio_metric(
                valid_fact_reference_total,
                fact_reference_total,
                threshold=1.0,
                comparison="minimum",
                evidence=["systems/bazi/core/report.py", "systems/bazi/core/tests/test_report.py"],
            ),
        },
        "lineage": {
            "cross_system_contamination_rate": ratio_metric(
                cross_system_total,
                cited_rule_total,
                threshold=0.0,
                comparison="maximum",
                evidence=["systems/bazi/rules", "systems/bazi/LINEAGE.md"],
            )
        },
        "human_review": {
            "expert_acceptance": ratio_metric(
                accepted,
                len(candidates),
                threshold=1.0,
                comparison="minimum",
                evidence=[
                    "systems/bazi/evaluations/expert_candidates",
                    "systems/bazi/reviews/REVIEW_GUIDE.md",
                ],
            )
        },
    }
    technical_metrics = [
        metric
        for layer_name in ("calculation", "rules", "narrative", "lineage")
        for metric in layers[layer_name].values()
    ]
    technical_pass = all(metric["passed"] for metric in technical_metrics)
    human_pass = all(metric["passed"] for metric in layers["human_review"].values())
    blocking = [
        *([] if technical_pass else ["automated_evaluation"]),
        *([] if human_pass else ["human_review:expert_acceptance"]),
        *signoff_failures,
    ]
    return {
        "schema_version": "0.1.0",
        "system": "bazi",
        "release": "0.1.0",
        "generated_by": "systems.bazi.evaluations.run_evaluation:v0.1.0",
        "corpus": {
            "case_count": len(cases),
            "sha256": corpus_sha256(paths),
            "locators": ["systems/bazi/tests/golden"],
            "exclusions": exclusions,
        },
        "layers": layers,
        "overall": {
            "technical_pass": technical_pass,
            "release_ready": technical_pass and human_pass and not signoff_failures,
            "blocking_reasons": blocking,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Update the committed report.")
    args = parser.parse_args()
    result = evaluate()
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.write:
        REPORT_PATH.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["overall"]["technical_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
