"""Generate deterministic Liuyao Golden Cases."""

from __future__ import annotations

import json
from pathlib import Path

from systems.liuyao.engine import calculate

ROOT = Path(__file__).resolve().parent / "golden"


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    dates = [
        "2026-01-05T08:15:00",
        "2026-03-20T23:10:00",
        "2026-05-16T14:30:00",
        "2026-08-07T06:45:00",
        "2026-11-22T19:20:00",
    ]
    for number, local_datetime in enumerate(dates, start=1):
        payload = {
            "question": f"Synthetic Liuyao structural case {number}",
            "seed_hex": f"{number + 300:064x}",
            "local_datetime": local_datetime,
            "timezone": "Asia/Shanghai",
            "day_boundary": "zi_initial" if number == 2 else "midnight",
        }
        result = calculate(payload)
        case = {
            "case_id": f"CASE-LIUYAO-CAST-{number:03d}",
            "title": f"Auditable Wen Wang structural cast {number:03d}",
            "system": "liuyao",
            "lineage": "wen-wang-najia-structural-v0.1",
            "category": "standard",
            "data_classification": "synthetic",
            "raw_input": payload,
            "normalized_input": result["normalized_input"],
            "expected_intermediate": {
                "palace": result["computed_facts"]["palace"],
                "day_pillar": result["computed_facts"]["calendar_context"]["day_pillar"]["ganzhi"],
            },
            "expected_output": {
                "audit": {"cast_id": result["audit"]["cast_id"]},
                "computed_facts": result["computed_facts"],
            },
            "must_match_rules": [
                "LIUYAO-NAJIA-001",
                "LIUYAO-PALACE-SHIYING-001",
                "LIUYAO-CALENDAR-CONTEXT-001",
                "LIUYAO-STRUCTURAL-BOUNDARY-001",
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "An event outcome is certain.",
                "A response date was inferred without a reviewed timing method.",
            ],
            "sources": [
                {
                    "source_id": "SRC-LIUYAO-PROJECT-SPEC-001",
                    "locator": "Wen Wang Najia structural tables",
                }
            ],
            "reviewers": [
                {
                    "reviewer_id": "deterministic-structure-review",
                    "role": "calculation",
                    "reviewed_at": "2026-07-23",
                    "decision": "accepted",
                    "notes": "Synthetic replay review; practitioner acceptance remains pending.",
                }
            ],
        }
        (ROOT / f"{case['case_id']}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print("Generated 5 Liuyao Golden Cases.")


if __name__ == "__main__":
    main()
