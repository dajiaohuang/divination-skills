"""Generate reviewed development fixtures from pinned calculator comparators.

The generated cases are development Golden Set candidates, not evidence of predictive validity.
Run this script only when the pinned comparator or case specification changes, then review the diff.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from systems.bazi.calculator.comparator import lunar_python_reference
from systems.bazi.calculator.engine import calculate_chart

ROOT = Path(__file__).resolve().parent
SOURCE_LUNAR = {"source_id": "SRC-BAZI-LUNARPY-001", "locator": "EightChar API v1.4.8"}
SOURCE_HKO = {
    "source_id": "SRC-ASTRONOMY-HKO-SOLAR-TERMS-001",
    "locator": "24 solar terms longitude table and 2024 calendar",
}
SOURCE_NOAA = {
    "source_id": "SRC-ASTRONOMY-NOAA-SOLAR-001",
    "locator": "General Solar Position Calculations, true solar time equations",
}
SOURCE_TIME = {
    "source_id": "SRC-TIME-PYTHON-ZONEINFO-001",
    "locator": "ZoneInfo fold and transition behavior",
}

STANDARD_INPUTS = [
    "1900-02-04T13:30:00",
    "1912-01-01T00:00:00",
    "1927-12-31T22:15:00",
    "1949-10-01T15:00:00",
    "1966-06-06T06:06:00",
    "1970-01-01T00:00:00",
    "1978-12-18T11:30:00",
    "1986-05-29T19:30:00",
    "1990-01-01T12:00:00",
    "1997-07-01T00:00:00",
    "2000-01-07T12:00:00",
    "2008-08-08T20:08:00",
    "2012-02-29T23:30:00",
    "2020-11-01T08:30:00",
    "2021-12-31T16:45:00",
    "2023-06-21T09:00:00",
    "2024-09-17T18:30:00",
    "2025-02-03T12:00:00",
    "2038-01-19T03:14:07",
    "2099-12-31T22:30:00",
]


def reviewer(role: str = "calculation") -> list[dict[str, str]]:
    return [
        {
            "reviewer_id": "pinned-comparator-review",
            "role": role,
            "reviewed_at": "2026-07-23",
            "decision": "accepted",
            "notes": (
                "Synthetic development case checked against pinned APIs; "
                "not expert interpretation review."
            ),
        }
    ]


def base_case(
    case_id: str,
    title: str,
    category: str,
    raw_input: dict[str, Any],
    expected_output: dict[str, Any],
    rules: list[str],
    *,
    sources: list[dict[str, str]] | None = None,
    expected_intermediate: dict[str, Any] | None = None,
    allowed_disagreements: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "title": title,
        "system": "bazi",
        "lineage": "ziping-calculation-baseline",
        "category": category,
        "data_classification": "synthetic",
        "raw_input": raw_input,
        "normalized_input": {
            "timezone": raw_input.get("timezone"),
            "day_boundary": raw_input.get("day_boundary", "midnight"),
        },
        "expected_intermediate": expected_intermediate or {},
        "expected_output": expected_output,
        "must_match_rules": rules,
        "allowed_disagreements": allowed_disagreements or [],
        "forbidden_conclusions": [
            "A fixed life event is guaranteed.",
            "An unsupported true-solar-time correction was silently applied.",
        ],
        "sources": sources or [SOURCE_LUNAR],
        "reviewers": reviewer(),
    }


def pillar_output(payload: dict[str, Any]) -> dict[str, Any]:
    reference = lunar_python_reference(payload)
    return {"computed_facts": {"pillars": reference}}


def write_case(directory: str, case: dict[str, Any]) -> None:
    target_dir = ROOT / directory
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / f"{case['case_id']}.json"
    path.write_text(
        json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def generate_standard_cases() -> None:
    for index, local_datetime in enumerate(STANDARD_INPUTS, start=1):
        payload = {
            "local_datetime": local_datetime,
            "timezone": "Asia/Shanghai",
            "day_boundary": "midnight",
        }
        case = base_case(
            f"CASE-BAZI-STANDARD-{index:03d}",
            f"Pinned four-pillar comparison {index:03d}",
            "standard",
            payload,
            pillar_output(payload),
            [
                "BAZI-CAL-YEAR-001",
                "BAZI-CAL-MONTH-001",
                "BAZI-CAL-DAY-001",
                "BAZI-CAL-HOUR-001",
                "BAZI-TIME-CIVIL-001",
            ],
        )
        write_case("golden", case)


def generate_edge_cases() -> None:
    edge_specs = [
        (
            "CASE-BAZI-EDGE-LICHUN-BEFORE-001",
            "One second before 2024 Spring Commences",
            {"local_datetime": "2024-02-04T16:27:06", "timezone": "Asia/Shanghai"},
            ["BAZI-CAL-YEAR-001", "BAZI-CAL-MONTH-001"],
        ),
        (
            "CASE-BAZI-EDGE-LICHUN-AT-001",
            "At the exact 2024 Spring Commences instant",
            {"local_datetime": "2024-02-04T16:27:07", "timezone": "Asia/Shanghai"},
            ["BAZI-CAL-YEAR-001", "BAZI-CAL-MONTH-001"],
        ),
        (
            "CASE-BAZI-EDGE-JINGZHE-BEFORE-001",
            "One second before the 2024 Insects Waken month boundary",
            {"local_datetime": "2024-03-05T10:22:44", "timezone": "Asia/Shanghai"},
            ["BAZI-CAL-MONTH-001"],
        ),
        (
            "CASE-BAZI-EDGE-JINGZHE-AT-001",
            "At the exact 2024 Insects Waken month boundary",
            {"local_datetime": "2024-03-05T10:22:45", "timezone": "Asia/Shanghai"},
            ["BAZI-CAL-MONTH-001"],
        ),
        (
            "CASE-BAZI-EDGE-LATEZI-MIDNIGHT-001",
            "Late Zi hour with midnight day boundary",
            {
                "local_datetime": "2024-01-01T23:30:00",
                "timezone": "Asia/Shanghai",
                "day_boundary": "midnight",
            },
            ["BAZI-CAL-DAY-001", "BAZI-CAL-HOUR-001"],
        ),
        (
            "CASE-BAZI-EDGE-LATEZI-ZIINITIAL-001",
            "Late Zi hour with 23:00 day boundary",
            {
                "local_datetime": "2024-01-01T23:30:00",
                "timezone": "Asia/Shanghai",
                "day_boundary": "zi_initial",
            },
            ["BAZI-CAL-DAY-002", "BAZI-CAL-HOUR-001"],
        ),
    ]
    for case_id, title, payload, rules in edge_specs:
        write_case(
            "edge_cases",
            base_case(
                case_id,
                title,
                "edge_case",
                payload,
                pillar_output(payload),
                rules,
                sources=[SOURCE_LUNAR, SOURCE_HKO]
                if "LICHUN" in case_id or "JINGZHE" in case_id
                else [SOURCE_LUNAR],
            ),
        )

    for fold, expected_utc in ((0, "2024-11-03T05:30:00Z"), (1, "2024-11-03T06:30:00Z")):
        payload = {
            "local_datetime": "2024-11-03T01:30:00",
            "timezone": "America/New_York",
            "fold": fold,
        }
        write_case(
            "edge_cases",
            base_case(
                f"CASE-BAZI-EDGE-DST-FOLD{fold}-001",
                f"Ambiguous New York time with fold {fold}",
                "edge_case",
                payload,
                {"normalized_input": {"utc_datetime": expected_utc, "fold": fold}},
                ["BAZI-VAL-DST-001"],
                sources=[SOURCE_TIME],
            ),
        )

    for case_id, payload in (
        (
            "CASE-BAZI-EDGE-MINYEAR-001",
            {"local_datetime": "1900-02-04T13:30:00", "timezone": "Asia/Shanghai"},
        ),
        (
            "CASE-BAZI-EDGE-MAXYEAR-001",
            {"local_datetime": "2100-12-31T22:30:00", "timezone": "Asia/Shanghai"},
        ),
    ):
        chart = calculate_chart(payload)
        write_case(
            "edge_cases",
            base_case(
                case_id,
                "Supported date-window boundary",
                "edge_case",
                payload,
                {
                    "computed_facts": {
                        "pillars": {
                            name: pillar["ganzhi"]
                            for name, pillar in chart["computed_facts"]["pillars"].items()
                        }
                    }
                },
                ["BAZI-CAL-YEAR-001", "BAZI-CAL-DAY-001"],
            ),
        )


def generate_dispute_cases() -> None:
    cases = [
        base_case(
            "CASE-BAZI-DISPUTE-DAY-BOUNDARY-001",
            "Late-Zi day-boundary alternatives",
            "dispute",
            {"local_datetime": "2024-01-01T23:30:00", "timezone": "Asia/Shanghai"},
            {"computed_facts": {"day_pillar": "甲子"}},
            ["BAZI-CAL-DAY-001", "BAZI-CAL-DAY-002"],
            allowed_disagreements=[
                {
                    "dispute_id": "DSP-BAZI-DAY-BOUNDARY-001",
                    "field_path": "computed_facts.day_pillar",
                    "allowed_values": ["甲子", "乙丑"],
                }
            ],
        ),
        base_case(
            "CASE-BAZI-DISPUTE-SOLAR-TIME-001",
            "Civil versus apparent solar time",
            "dispute",
            {
                "local_datetime": "2024-01-01T12:00:00",
                "timezone": "Asia/Shanghai",
                "longitude": 87.62,
                "time_basis": "apparent_solar",
            },
            {"normalized_input": {"true_solar_time_applied": True}},
            ["BAZI-TIME-CIVIL-001", "BAZI-TIME-SOLAR-001"],
            sources=[SOURCE_LUNAR, SOURCE_NOAA],
            allowed_disagreements=[
                {
                    "dispute_id": "DSP-BAZI-SOLAR-TIME-001",
                    "field_path": "normalized_input.true_solar_time_applied",
                    "allowed_values": [False, True],
                }
            ],
        ),
        base_case(
            "CASE-BAZI-DISPUTE-LUCK-DIRECTION-001",
            "Explicit versus inferred luck-cycle direction",
            "dispute",
            {
                "local_datetime": "1990-01-01T12:00:00",
                "timezone": "Asia/Shanghai",
                "luck_cycle_direction": "forward",
            },
            {"computed_facts": {"luck_cycles": {"direction": "forward"}}},
            ["BAZI-LUCK-DIR-001", "BAZI-LUCK-DIR-002"],
            allowed_disagreements=[
                {
                    "dispute_id": "DSP-BAZI-LUCK-DIRECTION-001",
                    "field_path": "computed_facts.luck_cycles.direction",
                    "allowed_values": ["forward", "reverse"],
                }
            ],
        ),
        base_case(
            "CASE-BAZI-DISPUTE-LUCK-START-001",
            "Luck-cycle start-age conversion methods",
            "dispute",
            {
                "local_datetime": "1990-01-01T12:00:00",
                "timezone": "Asia/Shanghai",
                "luck_cycle_direction": "forward",
            },
            {"computed_facts": {"luck_cycles": {"start_method": "three_days_per_year"}}},
            ["BAZI-LUCK-START-001", "BAZI-LUCK-START-002"],
            allowed_disagreements=[
                {
                    "dispute_id": "DSP-BAZI-LUCK-START-001",
                    "field_path": "computed_facts.luck_cycles.start_method",
                    "allowed_values": ["three_days_per_year", "calendar_component_conversion"],
                }
            ],
        ),
        base_case(
            "CASE-BAZI-DISPUTE-MONTH-BOUNDARY-001",
            "Exact instant versus whole-day month boundary",
            "dispute",
            {"local_datetime": "2024-03-05T08:00:00", "timezone": "Asia/Shanghai"},
            {"computed_facts": {"month_pillar": "丙寅"}},
            ["BAZI-CAL-MONTH-001", "BAZI-CAL-MONTH-002"],
            sources=[SOURCE_LUNAR, SOURCE_HKO],
            allowed_disagreements=[
                {
                    "dispute_id": "DSP-BAZI-MONTH-BOUNDARY-001",
                    "field_path": "computed_facts.month_pillar",
                    "allowed_values": ["丙寅", "丁卯"],
                }
            ],
        ),
    ]
    for case in cases:
        write_case("disputes", case)


def main() -> None:
    generate_standard_cases()
    generate_edge_cases()
    generate_dispute_cases()
    print("Generated 20 standard, 10 edge, and 5 dispute cases.")


if __name__ == "__main__":
    main()
