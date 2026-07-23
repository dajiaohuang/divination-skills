"""Generate project-native Ziwei foundation Golden Cases."""

from __future__ import annotations

import json
from pathlib import Path

from systems.ziwei.engine import calculate

ROOT = Path(__file__).resolve().parent / "golden"
INPUTS = [
    ("1900-02-04T00:30:00", "male"),
    ("1984-02-29T01:15:00", "female"),
    ("2000-08-16T03:20:00", "female"),
    ("2026-07-23T12:00:00", "male"),
    ("2099-12-31T23:30:00", "female"),
]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for number, (local_datetime, gender) in enumerate(INPUTS, start=1):
        payload = {
            "local_datetime": local_datetime,
            "timezone": "Asia/Shanghai",
            "calculation_gender": gender,
        }
        result = calculate(payload)
        case = {
            "case_id": f"CASE-ZIWEI-NATAL-{number:03d}",
            "title": f"Project-native Ziwei foundation chart {number:03d}",
            "system": "ziwei",
            "lineage": "project-native-ziwei-foundation-v0.1",
            "category": "standard",
            "data_classification": "synthetic",
            "raw_input": payload,
            "normalized_input": result["normalized_input"],
            "expected_intermediate": {
                "time_index": result["normalized_input"]["time_index"],
                "five_elements_class": result["computed_facts"]["five_elements_class"],
            },
            "expected_output": {"computed_facts": result["computed_facts"]},
            "must_match_rules": [
                "ZIWEI-NATIVE-NATAL-001",
                "ZIWEI-TIME-INDEX-001",
                "ZIWEI-STRUCTURAL-BOUNDARY-001",
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "A fixed life event is guaranteed.",
                "The calculation-gender parameter was inferred as identity.",
            ],
            "sources": [
                {
                    "source_id": "SRC-ZIWEI-PROJECT-SPEC-001",
                    "locator": "project-native structural calculation",
                }
            ],
            "reviewers": [
                {
                    "reviewer_id": "project-native-regression-review",
                    "role": "calculation",
                    "reviewed_at": "2026-07-23",
                    "decision": "accepted",
                    "notes": (
                        "Synthetic deterministic regression review; independent Ziwei expert "
                        "comparison remains pending."
                    ),
                }
            ],
        }
        (ROOT / f"{case['case_id']}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print("Generated 5 Ziwei Golden Cases.")


if __name__ == "__main__":
    main()
