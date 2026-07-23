"""Audit Bazi v0.1 release evidence without inventing missing approvals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from systems.bazi.evaluations.run_evaluation import REPORT_PATH, evaluate

SYSTEM = Path(__file__).resolve().parents[1]


def _json_count(path: Path) -> int:
    return len(list(path.glob("*.json")))


def audit_release() -> dict[str, Any]:
    signoff_path = Path(__file__).resolve().parent / "release-signoff.json"
    schema_path = SYSTEM.parents[1] / "common" / "evaluation" / "release-signoff.schema.json"
    signoff = json.loads(signoff_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(
        signoff
    )

    candidates = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((SYSTEM / "evaluations" / "expert_candidates").glob("*.json"))
    ]
    accepted_expert = sum(
        candidate["review"]["status"] == "reviewed"
        and candidate["review"]["decision"] == "accepted"
        for candidate in candidates
    )
    counts = {
        "standard": _json_count(SYSTEM / "tests" / "golden"),
        "edge": _json_count(SYSTEM / "tests" / "edge_cases"),
        "dispute": _json_count(SYSTEM / "tests" / "disputes"),
        "invalid_input": _json_count(SYSTEM / "tests" / "invalid_inputs"),
        "expert_candidates": len(candidates),
        "expert_accepted": accepted_expert,
    }
    minimums = {
        "standard": 100,
        "edge": 30,
        "dispute": 20,
        "invalid_input": 20,
        "expert_candidates": 50,
        "expert_accepted": 50,
    }
    count_checks = {key: counts[key] >= minimum for key, minimum in minimums.items()}
    signoff_checks = {item["role"]: item["status"] == "accepted" for item in signoff["signoffs"]}
    current_evaluation = evaluate()
    committed_evaluation = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    evaluation_checks = {
        "report_current": committed_evaluation == current_evaluation,
        "technical_pass": current_evaluation["overall"]["technical_pass"],
    }
    ready = (
        all(count_checks.values())
        and all(signoff_checks.values())
        and all(evaluation_checks.values())
    )
    return {
        "release": signoff["release"],
        "ready": ready,
        "counts": counts,
        "minimums": minimums,
        "count_checks": count_checks,
        "signoff_checks": signoff_checks,
        "evaluation_checks": evaluation_checks,
        "blocking_reasons": [
            *[f"count:{key}" for key, passed in count_checks.items() if not passed],
            *[f"signoff:{key}" for key, passed in signoff_checks.items() if not passed],
            *[f"evaluation:{key}" for key, passed in evaluation_checks.items() if not passed],
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report-only", action="store_true", help="Always exit zero after reporting."
    )
    args = parser.parse_args()
    result = audit_release()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ready"] or args.report_only else 1


if __name__ == "__main__":
    raise SystemExit(main())
