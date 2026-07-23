from __future__ import annotations

import json
from pathlib import Path

from systems.numerology.calculator import calculate_profile

ROOT = Path(__file__).resolve().parent / "golden"
INPUTS = [
    {"name": "Arden Vale", "birth_date": "1905-12-10"},
    {"name": "Grace River", "birth_date": "1906-12-09"},
    {"name": "Alex Rowan", "birth_date": "1912-06-23"},
    {"name": "Katherine North", "birth_date": "1918-08-26"},
    {"name": "Lina Stone", "birth_date": "1969-12-28"},
    {"name": "Renée Élise", "birth_date": "1988-11-11"},
    {"name": "Test Person", "birth_date": "2000-01-01"},
    {"name": "Example Name", "birth_date": "2024-02-29"},
    {"name": "Master Builder", "birth_date": "1975-07-30"},
    {"name": "Reflective User", "birth_date": "2030-10-05"},
]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for number, payload in enumerate(INPUTS, start=1):
        profile = calculate_profile(payload)
        case = {
            "case_id": f"CASE-NUMEROLOGY-PROFILE-{number:03d}",
            "title": f"Pythagorean project profile {number:03d}",
            "system": "numerology",
            "lineage": "pythagorean-project-v0.1",
            "category": "standard",
            "data_classification": "synthetic",
            "raw_input": payload,
            "normalized_input": profile["normalized_input"],
            "expected_intermediate": {},
            "expected_output": {"computed_facts": profile["computed_facts"]},
            "must_match_rules": [
                "NUMEROLOGY-CAL-DATE-001",
                "NUMEROLOGY-CAL-NAME-001",
                "NUMEROLOGY-INTERPRET-THEME-001",
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "The number proves a personality trait.",
                "A future event is guaranteed.",
            ],
            "sources": [
                {"source_id": "SRC-NUMEROLOGY-PROJECT-SPEC-001", "locator": "v0.1 mapping contract"}
            ],
            "reviewers": [
                {
                    "reviewer_id": "deterministic-profile-review",
                    "role": "calculation",
                    "reviewed_at": "2026-07-23",
                    "decision": "accepted",
                    "notes": "Synthetic regression case; symbolic validity is not asserted.",
                }
            ],
        }
        (ROOT / f"{case['case_id']}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
