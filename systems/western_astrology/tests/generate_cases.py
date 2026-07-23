"""Generate ten deterministic Western natal Golden Cases."""

from __future__ import annotations

import json
from pathlib import Path

from systems.western_astrology.calculator import calculate_chart

ROOT = Path(__file__).resolve().parent / "golden"
INPUTS = [
    {
        "local_datetime": "2000-01-01T12:00:00",
        "timezone": "UTC",
        "longitude": 0.0,
        "latitude": 51.4779,
    },
    {
        "local_datetime": "1986-05-29T19:30:00",
        "timezone": "Asia/Shanghai",
        "longitude": 121.4737,
        "latitude": 31.2304,
        "house_system": "equal",
    },
    {
        "local_datetime": "2024-11-03T01:30:00",
        "timezone": "America/New_York",
        "fold": 0,
        "longitude": -74.006,
        "latitude": 40.7128,
    },
    {
        "local_datetime": "2024-11-03T01:30:00",
        "timezone": "America/New_York",
        "fold": 1,
        "longitude": -74.006,
        "latitude": 40.7128,
    },
    {
        "local_datetime": "1969-07-20T16:17:00",
        "timezone": "America/Los_Angeles",
        "longitude": -118.2437,
        "latitude": 34.0522,
    },
    {
        "local_datetime": "2012-02-29T23:30:00",
        "timezone": "Asia/Tokyo",
        "longitude": 139.6917,
        "latitude": 35.6895,
        "house_system": "equal",
    },
    {
        "local_datetime": "1947-08-15T00:00:00",
        "timezone": "Asia/Kolkata",
        "longitude": 77.209,
        "latitude": 28.6139,
    },
    {
        "local_datetime": "1999-12-31T23:59:59",
        "timezone": "Europe/London",
        "longitude": -0.1276,
        "latitude": 51.5072,
    },
    {
        "local_datetime": "2020-06-21T12:00:00",
        "timezone": "Australia/Sydney",
        "longitude": 151.2093,
        "latitude": -33.8688,
    },
    {
        "local_datetime": "2038-01-19T03:14:07",
        "timezone": "America/Sao_Paulo",
        "longitude": -46.6333,
        "latitude": -23.5505,
        "house_system": "equal",
    },
]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for number, payload in enumerate(INPUTS, start=1):
        chart = calculate_chart(payload)
        house_rule = (
            "WESTERN-HOUSE-WHOLE-001"
            if chart["normalized_input"]["house_system"] == "whole_sign"
            else "WESTERN-HOUSE-EQUAL-001"
        )
        case = {
            "case_id": f"CASE-WESTERN-NATAL-{number:03d}",
            "title": f"Tropical natal calculation {number:03d}",
            "system": "western-astrology",
            "lineage": "tropical-geocentric-v0.1",
            "category": "standard",
            "data_classification": "synthetic",
            "raw_input": payload,
            "normalized_input": chart["normalized_input"],
            "expected_intermediate": {},
            "expected_output": {"computed_facts": chart["computed_facts"]},
            "must_match_rules": [
                "WESTERN-CAL-POSITION-001",
                "WESTERN-CAL-ANGLES-001",
                house_rule,
                "WESTERN-ASPECT-MAJOR-001",
                "WESTERN-INTERPRET-STRUCTURE-001",
                "WESTERN-TRADITIONAL-CONDITION-001",
            ],
            "allowed_disagreements": [],
            "forbidden_conclusions": [
                "A life event is guaranteed.",
                "An unsupported house system was silently substituted.",
            ],
            "sources": [
                {
                    "source_id": "SRC-WESTERN-ASTRONOMY-ENGINE-001",
                    "locator": "Pinned 2.1.19 calculation",
                },
                {
                    "source_id": "SRC-WESTERN-PROJECT-SPEC-001",
                    "locator": "Tropical house and aspect contract",
                },
                {
                    "source_id": "SRC-WESTERN-PTOLEMY-001",
                    "locator": "Book I traditional houses and exaltations",
                },
            ],
            "reviewers": [
                {
                    "reviewer_id": "pinned-astronomy-engine-review",
                    "role": "calculation",
                    "reviewed_at": "2026-07-23",
                    "decision": "accepted",
                    "notes": (
                        "Synthetic regression fixture; independent practitioner "
                        "sign-off remains pending."
                    ),
                }
            ],
        }
        path = ROOT / f"{case['case_id']}.json"
        path.write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print("Generated 10 Western natal Golden Cases.")


if __name__ == "__main__":
    main()
