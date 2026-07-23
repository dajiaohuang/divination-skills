"""Build 50 traceable synthetic reports for independent expert review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from systems.bazi.calculator.engine import calculate_chart
from systems.bazi.core.report import build_report

SYSTEM = Path(__file__).resolve().parents[1]
CASES = SYSTEM / "tests" / "golden"
OUTPUT = Path(__file__).resolve().parent / "expert_candidates"
SECTIONS = (
    "calculation_basis",
    "verified_facts",
    "symbolic_relationships",
    "seasonal_support_path",
    "method_specific_timing",
)


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    case_paths = sorted(CASES.glob("*.json"))[:50]
    if len(case_paths) != 50:
        raise AssertionError("Exactly 50 standard cases are required for review candidates.")

    for number, case_path in enumerate(case_paths, start=1):
        case = json.loads(case_path.read_text(encoding="utf-8"))
        chart = calculate_chart(case["raw_input"])
        report = build_report(chart)
        chain = []
        for section in SECTIONS:
            for explanation in report["narrative"][section]:
                claim = {
                    "claim_id": f"CLAIM-{len(chain) + 1:03d}",
                    "section": section,
                    "statement": explanation["statement"],
                    "fact_ids": sorted(set(explanation["fact_ids"])),
                    "rule_ids": sorted(set(explanation["rule_ids"])),
                }
                if "features" in explanation:
                    claim["features"] = explanation["features"]
                chain.append(claim)
        candidate = {
            "analysis_id": f"ANALYSIS-BAZI-{number:03d}",
            "case_id": case["case_id"],
            "data_classification": "synthetic",
            "computed_facts_sha256": canonical_hash(chart["computed_facts"]),
            "strength_lineage": None,
            "reasoning_chain": chain,
            "review": {
                "status": "pending_expert",
                "reviewer_id": None,
                "reviewed_at": None,
                "decision": None,
                "notes": (
                    "Machine-generated traceability candidate only. An independent named domain "
                    "expert must verify or revise every claim before release."
                ),
            },
        }
        path = OUTPUT / f"{candidate['analysis_id']}.json"
        path.write_text(
            json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print("Generated 50 expert-review candidates without fabricating expert approval.")


if __name__ == "__main__":
    main()
