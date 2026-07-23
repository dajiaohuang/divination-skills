"""Generate an auditable, unaccepted Ziwei expert-review candidate queue."""

from __future__ import annotations

import json
from pathlib import Path

from systems.ziwei.core import analyze_core
from systems.ziwei.engine import LINEAGE, calculate

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_ROOT = SYSTEM_ROOT / "tests" / "golden"
OUTPUT_ROOT = Path(__file__).resolve().parent / "expert_candidates"


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT_ROOT.glob("ZIWEI-EXPERT-CANDIDATE-*.json"):
        path.unlink()
    golden = sorted(GOLDEN_ROOT.glob("CASE-ZIWEI-NATAL-*.json"))[:50]
    for index, path in enumerate(golden, start=1):
        case = json.loads(path.read_text(encoding="utf-8"))
        report = analyze_core(calculate(case["raw_input"]))
        candidate = {
            "candidate_id": f"ZIWEI-EXPERT-CANDIDATE-{index:03d}",
            "system": "ziwei",
            "lineage": LINEAGE,
            "source_case_id": case["case_id"],
            "status": "pending_expert_review",
            "accepted": False,
            "review_requirements": [
                "Verify each cited fact exists in the source chart.",
                "Reject deterministic event, identity, diagnosis, or fortune claims.",
                "Record rule-level acceptance, changes requested, or rejection.",
            ],
            "candidate_report": report,
            "review": {
                "reviewer_id": None,
                "reviewed_at": None,
                "decision": "pending",
                "notes": "",
            },
        }
        output = OUTPUT_ROOT / f"{candidate['candidate_id']}.json"
        output.write_text(
            json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(f"Generated {len(golden)} pending Ziwei expert candidates.")


if __name__ == "__main__":
    main()
