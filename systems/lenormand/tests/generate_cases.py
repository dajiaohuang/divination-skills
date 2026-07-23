"""Generate deterministic Lenormand Golden Cases."""

from __future__ import annotations

import json
from pathlib import Path

from systems.lenormand.engine import draw

ROOT = Path(__file__).resolve().parent / "golden"
SPREADS = ["single", "three-card", "nine-card"]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for number in range(1, 6):
        payload = {
            "spread": SPREADS[(number - 1) % len(SPREADS)],
            "question": f"Synthetic Lenormand reflection prompt {number}",
            "seed_hex": f"{number:064x}",
            "allow_reversals": False,
        }
        result = draw(payload)
        case = {
            "case_id": f"CASE-LENORMAND-DRAW-{number:03d}",
            "title": f"Auditable Lenormand draw {number:03d}",
            "system": "lenormand",
            "lineage": "lenormand-36-project-v0.3",
            "category": "standard",
            "data_classification": "synthetic",
            "raw_input": payload,
            "normalized_input": result["normalized_input"],
            "expected_intermediate": {"deck_sha256": result["audit"]["deck_sha256"]},
            "expected_output": {
                "audit": {"draw_id": result["audit"]["draw_id"]},
                "computed_facts": result["computed_facts"],
            },
            "must_match_rules": [
                "LENORMAND-CARD-UPRIGHT-001",
                "LENORMAND-POSITION-001",
                "LENORMAND-SEQUENCE-001",
                "LENORMAND-CARD-IDENTITY-001",
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "A fixed future event is guaranteed.",
                "The symbols establish a hidden fact about a third party.",
            ],
            "sources": [
                {
                    "source_id": "SRC-LENORMAND-PROJECT-SPEC-001",
                    "locator": "text-only 36-symbol project deck and draw contract",
                },
                {
                    "source_id": "SRC-LENORMAND-BM-HOPE-001",
                    "locator": "British Museum complete Game of Hope pack",
                },
            ],
            "reviewers": [
                {
                    "reviewer_id": "deterministic-draw-review",
                    "role": "calculation",
                    "reviewed_at": "2026-07-23",
                    "decision": "accepted",
                    "notes": "Synthetic replay review; not evidence of predictive validity.",
                }
            ],
        }
        (ROOT / f"{case['case_id']}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print("Generated 5 Lenormand Golden Cases.")


if __name__ == "__main__":
    main()
