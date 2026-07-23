"""Generate Qimen foundation Golden Cases."""

from __future__ import annotations

import json
from pathlib import Path

from systems.qimen.engine import calculate

ROOT = Path(__file__).resolve().parent / "golden"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    dates = [
        "2026-01-06T08:00:00",
        "2026-03-21T10:00:00",
        "2026-06-22T12:00:00",
        "2026-09-24T16:00:00",
        "2026-12-22T20:00:00",
    ]
    for number, local_datetime in enumerate(dates, start=1):
        payload = {
            "local_datetime": local_datetime,
            "timezone": "Asia/Shanghai",
            "day_boundary": "midnight",
        }
        result = calculate(payload)
        case = {
            "case_id": f"CASE-QIMEN-FOUNDATION-{number:03d}",
            "title": f"Chaibu Qimen foundation {number:03d}",
            "system": "qimen",
            "lineage": "shijia-zhuanpan-chaibu-v0.3",
            "category": "standard",
            "data_classification": "synthetic",
            "raw_input": payload,
            "normalized_input": result["normalized_input"],
            "expected_intermediate": {
                "solar_term": result["computed_facts"]["solar_term"],
                "yuan": result["computed_facts"]["yuan"],
            },
            "expected_output": {"computed_facts": result["computed_facts"]},
            "must_match_rules": [
                "QIMEN-CHAIBU-JU-001",
                "QIMEN-EARTH-PLATE-001",
                "QIMEN-DUTY-ORIGIN-001",
                "QIMEN-FOUNDATION-BOUNDARY-001",
                "QIMEN-CLASSICAL-PLATE-PROVENANCE-001",
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "This foundation is a complete Qimen chart.",
                "An auspicious direction or event outcome was inferred.",
            ],
            "sources": [
                {"source_id": "SRC-QIMEN-PROJECT-SPEC-001", "locator": "Chaibu foundation tables"},
                {
                    "source_id": "SRC-QIMEN-BAOJIAN-001",
                    "locator": "classical shared structural vocabulary",
                },
            ],
            "reviewers": [
                {
                    "reviewer_id": "deterministic-foundation-review",
                    "role": "calculation",
                    "reviewed_at": "2026-07-23",
                    "decision": "accepted",
                    "notes": "Synthetic replay review; practitioner acceptance remains pending.",
                }
            ],
        }
        (ROOT / f"{case['case_id']}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print("Generated 5 Qimen foundation Golden Cases.")


if __name__ == "__main__":
    main()
