"""Generate deterministic Elder Futhark Golden Cases."""

from __future__ import annotations

import json
from pathlib import Path

from systems.runes.engine import draw

ROOT = Path(__file__).resolve().parent / "golden"
SPREADS = ["single", "three-rune"]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for number in range(1, 6):
        payload = {
            "spread": SPREADS[(number - 1) % len(SPREADS)],
            "question": f"Synthetic rune reflection prompt {number}",
            "seed_hex": f"{number + 100:064x}",
            "allow_reversals": False,
        }
        result = draw(payload)
        case = {
            "case_id": f"CASE-RUNES-DRAW-{number:03d}",
            "title": f"Auditable Elder Futhark draw {number:03d}",
            "system": "runes",
            "lineage": "elder-futhark-project-v0.3",
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
                "RUNES-DRAW-UNIQUE-001",
                "RUNES-SYMBOL-UPRIGHT-001",
                "RUNES-POSITION-001",
                "RUNES-SEQUENCE-001",
                "RUNES-GRAPHEME-IDENTITY-001",
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "A fixed future event is guaranteed.",
                "The symbols establish a hidden fact about a third party.",
            ],
            "sources": [
                {
                    "source_id": "SRC-RUNES-PROJECT-SPEC-001",
                    "locator": "text-only 24-symbol project deck and draw contract",
                },
                {
                    "source_id": "SRC-RUNES-UNICODE-001",
                    "locator": "Unicode Runic block names list",
                },
                {
                    "source_id": "SRC-RUNES-SHM-KYLVER-001",
                    "locator": "Kylver stone 24-character sequence",
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
    print("Generated 5 Rune Golden Cases.")


if __name__ == "__main__":
    main()
