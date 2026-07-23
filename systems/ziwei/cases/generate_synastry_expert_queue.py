"""Generate a pending Ziwei synastry expert-review queue."""

from __future__ import annotations

import json
from pathlib import Path

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = SYSTEM_ROOT / "tests" / "extension_cases" / "synastry"
OUTPUT = Path(__file__).resolve().parent / "synastry_expert_candidates.json"


def main() -> None:
    cases = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(CASE_ROOT.glob("*.json"))
    ]
    candidates = [
        {
            "candidate_id": f"ZIWEI-SYNASTRY-EXPERT-{index:03d}",
            "source_case_id": case["case_id"],
            "expected_output_sha256": case["expected_sha256"],
            "status": "pending_expert_review",
            "accepted": False,
            "review_focus": [
                "directional transformation provenance",
                "same-role shared-major-star symmetry",
                "absence of compatibility, intent, fidelity, and outcome claims",
            ],
            "review": {
                "reviewer_id": None,
                "reviewed_at": None,
                "decision": "pending",
                "notes": "",
            },
        }
        for index, case in enumerate(cases, start=1)
    ]
    OUTPUT.write_text(
        json.dumps(
            {
                "system": "ziwei",
                "module": "synastry",
                "status": "pending_expert_review",
                "candidate_count": len(candidates),
                "candidates": candidates,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Generated {len(candidates)} Ziwei synastry expert candidates.")


if __name__ == "__main__":
    main()
