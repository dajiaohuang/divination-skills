"""Generate deterministic I Ching Golden Cases."""

from __future__ import annotations

import json
from pathlib import Path

from systems.iching.engine import cast

ROOT = Path(__file__).resolve().parent / "golden"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for number in range(1, 6):
        payload = {
            "question": f"Synthetic I Ching reflection prompt {number}",
            "seed_hex": f"{number + 200:064x}",
        }
        result = cast(payload)
        case = {
            "case_id": f"CASE-ICHING-CAST-{number:03d}",
            "title": f"Auditable three-coin cast {number:03d}",
            "system": "iching",
            "lineage": "three-coin-king-wen-structural-v0.1",
            "category": "standard",
            "data_classification": "synthetic",
            "raw_input": payload,
            "normalized_input": result["normalized_input"],
            "expected_intermediate": {
                "line_values": [line["value"] for line in result["computed_facts"]["lines"]]
            },
            "expected_output": {
                "audit": {"cast_id": result["audit"]["cast_id"]},
                "computed_facts": result["computed_facts"],
            },
            "must_match_rules": [
                "ICHING-HEXAGRAM-MAP-001",
                "ICHING-MOVING-LINES-001",
                "ICHING-STRUCTURAL-REFLECTION-001",
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "A fixed future event is guaranteed.",
                "The cast replaces medical, legal, or financial evidence.",
            ],
            "sources": [
                {
                    "source_id": "SRC-ICHING-PROJECT-SPEC-001",
                    "locator": "three-coin cast and King Wen mapping",
                }
            ],
            "reviewers": [
                {
                    "reviewer_id": "deterministic-cast-review",
                    "role": "calculation",
                    "reviewed_at": "2026-07-23",
                    "decision": "accepted",
                    "notes": "Synthetic replay review only; domain acceptance remains pending.",
                }
            ],
        }
        (ROOT / f"{case['case_id']}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print("Generated 5 I Ching Golden Cases.")


if __name__ == "__main__":
    main()
