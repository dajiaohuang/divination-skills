"""Generate ten deterministic Tarot Golden Cases."""

from __future__ import annotations

import json
from pathlib import Path

from systems.tarot.draw.engine import draw_cards

ROOT = Path(__file__).resolve().parent / "golden"
SPREADS = [
    "single",
    "situation-challenge-guidance",
    "option-a-option-b-focus",
]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for number in range(1, 11):
        payload = {
            "spread": SPREADS[(number - 1) % len(SPREADS)],
            "question": f"Synthetic reflection prompt {number}",
            "seed_hex": f"{number:064x}",
            "allow_reversals": number % 4 != 0,
        }
        draw = draw_cards(payload)
        orientation_rules = sorted(
            {
                "TAROT-ORIENTATION-REVERSED-001"
                if card["orientation"] == "reversed"
                else "TAROT-ORIENTATION-UPRIGHT-001"
                for card in draw["computed_facts"]["cards"]
            }
        )
        case = {
            "case_id": f"CASE-TAROT-DRAW-{number:03d}",
            "title": f"Auditable Tarot draw {number:03d}",
            "system": "tarot",
            "lineage": "rws-text-baseline-v0.1",
            "category": "standard",
            "data_classification": "synthetic",
            "raw_input": payload,
            "normalized_input": draw["normalized_input"],
            "expected_intermediate": {"deck_sha256": draw["audit"]["deck_sha256"]},
            "expected_output": {
                "audit": {"draw_id": draw["audit"]["draw_id"]},
                "computed_facts": draw["computed_facts"],
            },
            "must_match_rules": [
                "TAROT-DRAW-UNIQUE-001",
                "TAROT-POSITION-001",
                "TAROT-NARRATIVE-001",
                *orientation_rules,
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "A fixed future event is guaranteed.",
                "The cards establish a hidden fact about a third party.",
            ],
            "sources": [
                {
                    "source_id": "SRC-TAROT-DECK-SPEC-001",
                    "locator": "rws-78.json and auditable draw contract",
                }
            ],
            "reviewers": [
                {
                    "reviewer_id": "deterministic-draw-review",
                    "role": "calculation",
                    "reviewed_at": "2026-07-23",
                    "decision": "accepted",
                    "notes": (
                        "Synthetic deterministic regression case; not proof of predictive validity."
                    ),
                }
            ],
        }
        path = ROOT / f"{case['case_id']}.json"
        path.write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print("Generated 10 Tarot Golden Cases.")


if __name__ == "__main__":
    main()
