"""Generate the initial calculation-policy rules and dispute records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SYSTEM_ROOT = Path(__file__).resolve().parents[1]
RULE_DIR = SYSTEM_ROOT / "rules"
DISPUTE_DIR = SYSTEM_ROOT / "disputes"

LUNAR_DIRECT = {
    "source_id": "SRC-BAZI-LUNARPY-001",
    "locator": "Pinned v1.4.8 public API and implementation",
    "support_type": "direct",
}
HKO_CORROBORATING = {
    "source_id": "SRC-ASTRONOMY-HKO-SOLAR-TERMS-001",
    "locator": "24 solar terms longitude table and 2024 calendar",
    "support_type": "corroborating",
}
ZONEINFO_DIRECT = {
    "source_id": "SRC-TIME-PYTHON-ZONEINFO-001",
    "locator": "ZoneInfo fold and transition behavior",
    "support_type": "direct",
}


def rule(
    rule_id: str,
    title: str,
    kind: str,
    condition_path: str,
    operator: str,
    condition_value: Any,
    output_path: str,
    output_value: Any,
    tests: list[str],
    *,
    lineage: str = "ziping-calculation-baseline",
    status: str = "tested",
    priority: int = 800,
    sources: list[dict[str, str]] | None = None,
    disputes: list[str] | None = None,
) -> dict[str, Any]:
    condition = {"fact_path": condition_path, "operator": operator}
    if operator not in {"exists", "absent"}:
        condition["value"] = condition_value
    return {
        "rule_id": rule_id,
        "title": title,
        "system": "bazi",
        "lineage": lineage,
        "version": "0.1.0",
        "status": status,
        "kind": kind,
        "conditions": [condition],
        "conclusions": [
            {
                "finding_type": f"bazi.{kind}",
                "output_path": output_path,
                "value": output_value,
                "confidence": "deterministic" if kind != "interpretation" else "low",
            }
        ],
        "priority": priority,
        "sources": sources or [LUNAR_DIRECT],
        "disputes": disputes or [],
        "tests": tests,
    }


RULES = [
    rule(
        "BAZI-CAL-YEAR-001",
        "Change the year pillar at the exact Spring Commences instant",
        "calculation",
        "normalized_input.utc_datetime",
        "exists",
        None,
        "computed_facts.pillars.year",
        "exact_li_chun_boundary",
        ["CASE-BAZI-EDGE-LICHUN-BEFORE-001", "CASE-BAZI-EDGE-LICHUN-AT-001"],
        sources=[LUNAR_DIRECT, HKO_CORROBORATING],
    ),
    rule(
        "BAZI-CAL-MONTH-001",
        "Change the month pillar at the exact minor solar-term instant",
        "calculation",
        "normalized_input.utc_datetime",
        "exists",
        None,
        "computed_facts.pillars.month",
        "exact_jie_boundary",
        ["CASE-BAZI-EDGE-JINGZHE-BEFORE-001", "CASE-BAZI-EDGE-JINGZHE-AT-001"],
        sources=[LUNAR_DIRECT, HKO_CORROBORATING],
        disputes=["DSP-BAZI-MONTH-BOUNDARY-001"],
    ),
    rule(
        "BAZI-CAL-MONTH-002",
        "Change the month pillar at the beginning of the term's civil date",
        "calculation",
        "normalized_input.month_boundary_policy",
        "eq",
        "whole_day",
        "computed_facts.pillars.month",
        "whole_day_boundary",
        ["CASE-BAZI-DISPUTE-MONTH-BOUNDARY-001"],
        lineage="whole-day-boundary",
        status="proposed",
        priority=100,
        sources=[HKO_CORROBORATING],
        disputes=["DSP-BAZI-MONTH-BOUNDARY-001"],
    ),
    rule(
        "BAZI-CAL-DAY-001",
        "Use midnight as the default day-pillar boundary",
        "calculation",
        "normalized_input.day_boundary",
        "eq",
        "midnight",
        "computed_facts.pillars.day",
        "midnight_boundary",
        ["CASE-BAZI-STANDARD-001", "CASE-BAZI-EDGE-LATEZI-MIDNIGHT-001"],
        disputes=["DSP-BAZI-DAY-BOUNDARY-001"],
    ),
    rule(
        "BAZI-CAL-DAY-002",
        "Advance the day pillar at 23:00 when zi_initial is selected",
        "calculation",
        "normalized_input.day_boundary",
        "eq",
        "zi_initial",
        "computed_facts.pillars.day",
        "zi_initial_boundary",
        ["CASE-BAZI-EDGE-LATEZI-ZIINITIAL-001"],
        lineage="late-zi-alternative",
        disputes=["DSP-BAZI-DAY-BOUNDARY-001"],
    ),
    rule(
        "BAZI-CAL-HOUR-001",
        "Derive the double-hour branch and stem from local civil time",
        "calculation",
        "normalized_input.local_datetime",
        "exists",
        None,
        "computed_facts.pillars.hour",
        "civil_double_hour",
        ["CASE-BAZI-STANDARD-001", "CASE-BAZI-EDGE-LATEZI-MIDNIGHT-001"],
    ),
    rule(
        "BAZI-TIME-CIVIL-001",
        "Use IANA local civil time without solar-time correction",
        "calculation",
        "normalized_input.true_solar_time_applied",
        "eq",
        False,
        "normalized_input.local_datetime",
        "civil_time",
        ["CASE-BAZI-STANDARD-001", "CASE-BAZI-DISPUTE-SOLAR-TIME-001"],
        sources=[ZONEINFO_DIRECT, LUNAR_DIRECT],
        disputes=["DSP-BAZI-SOLAR-TIME-001"],
    ),
    rule(
        "BAZI-TIME-SOLAR-001",
        "Apply apparent solar time before selecting day and hour pillars",
        "calculation",
        "normalized_input.true_solar_time_applied",
        "eq",
        True,
        "normalized_input.local_datetime",
        "apparent_solar_time",
        ["CASE-BAZI-DISPUTE-SOLAR-TIME-001"],
        lineage="apparent-solar-time",
        status="rejected",
        priority=0,
        sources=[HKO_CORROBORATING],
        disputes=["DSP-BAZI-SOLAR-TIME-001"],
    ),
    rule(
        "BAZI-LUCK-DIR-001",
        "Require explicit luck-cycle direction",
        "validation",
        "normalized_input.luck_cycle_direction",
        "in",
        ["forward", "reverse"],
        "computed_facts.luck_cycles.direction",
        "explicit_input",
        ["CASE-BAZI-DISPUTE-LUCK-DIRECTION-001"],
        disputes=["DSP-BAZI-LUCK-DIRECTION-001"],
    ),
    rule(
        "BAZI-LUCK-DIR-002",
        "Infer luck-cycle direction from sex and year-stem polarity",
        "calculation",
        "normalized_input.sex_for_traditional_direction",
        "exists",
        None,
        "computed_facts.luck_cycles.direction",
        "traditional_inference",
        ["CASE-BAZI-DISPUTE-LUCK-DIRECTION-001"],
        lineage="traditional-gender-polarity",
        status="proposed",
        priority=100,
        disputes=["DSP-BAZI-LUCK-DIRECTION-001"],
    ),
    rule(
        "BAZI-LUCK-START-001",
        "Convert adjacent-term interval at three days per year",
        "calculation",
        "normalized_input.luck_cycle_direction",
        "in",
        ["forward", "reverse"],
        "computed_facts.luck_cycles.start_age_years",
        "three_days_per_year",
        ["CASE-BAZI-DISPUTE-LUCK-START-001"],
        disputes=["DSP-BAZI-LUCK-START-001"],
    ),
    rule(
        "BAZI-LUCK-START-002",
        "Convert adjacent-term interval into calendar components",
        "calculation",
        "normalized_input.luck_start_method",
        "eq",
        "calendar_component_conversion",
        "computed_facts.luck_cycles.start_age_years",
        "calendar_component_conversion",
        ["CASE-BAZI-DISPUTE-LUCK-START-001"],
        lineage="calendar-component-conversion",
        status="proposed",
        priority=100,
        disputes=["DSP-BAZI-LUCK-START-001"],
    ),
    rule(
        "BAZI-VAL-DST-001",
        "Require fold for an ambiguous local time",
        "validation",
        "normalized_input.fold",
        "in",
        [0, 1],
        "validation.status",
        "valid",
        ["CASE-BAZI-EDGE-DST-FOLD0-001", "CASE-BAZI-EDGE-DST-FOLD1-001"],
        priority=1000,
        sources=[ZONEINFO_DIRECT],
    ),
]


def source_ref(source: dict[str, str]) -> dict[str, str]:
    return {"source_id": source["source_id"], "locator": source["locator"]}


def dispute(
    dispute_id: str,
    title: str,
    topic: str,
    positions: list[tuple[str, str, list[str], list[dict[str, str]]]],
    selected_lineage: str,
    rationale: str,
    disclosure: str,
) -> dict[str, Any]:
    return {
        "dispute_id": dispute_id,
        "title": title,
        "system": "bazi",
        "topic": topic,
        "status": "resolved_for_product",
        "positions": [
            {
                "lineage": lineage,
                "summary": summary,
                "rule_ids": rule_ids,
                "sources": [source_ref(source) for source in sources],
            }
            for lineage, summary, rule_ids, sources in positions
        ],
        "default_policy": {
            "selected_lineage": selected_lineage,
            "rationale": rationale,
            "user_disclosure_required": True,
        },
        "user_disclosure": disclosure,
        "sources": [
            source_ref(source)
            for _, _, _, position_sources in positions
            for source in position_sources
        ],
    }


DISPUTES = [
    dispute(
        "DSP-BAZI-DAY-BOUNDARY-001",
        "Day pillar changes at midnight or at 23:00",
        "day boundary",
        [
            (
                "ziping-calculation-baseline",
                "Keep the civil date's day pillar through 23:59.",
                ["BAZI-CAL-DAY-001"],
                [LUNAR_DIRECT],
            ),
            (
                "late-zi-alternative",
                "Advance the day pillar at the beginning of the Zi double-hour.",
                ["BAZI-CAL-DAY-002"],
                [LUNAR_DIRECT],
            ),
        ],
        "ziping-calculation-baseline",
        "Midnight is the v0.1 default; the alternative remains an explicit input.",
        "The default day pillar changes at midnight; select zi_initial to change it at 23:00.",
    ),
    dispute(
        "DSP-BAZI-SOLAR-TIME-001",
        "Civil time or apparent solar time",
        "time basis",
        [
            (
                "ziping-calculation-baseline",
                "Use historical local civil time from an IANA time zone.",
                ["BAZI-TIME-CIVIL-001"],
                [ZONEINFO_DIRECT, LUNAR_DIRECT],
            ),
            (
                "apparent-solar-time",
                "Correct civil time using longitude and equation of time.",
                ["BAZI-TIME-SOLAR-001"],
                [HKO_CORROBORATING],
            ),
        ],
        "ziping-calculation-baseline",
        "No validated apparent-solar-time implementation exists in v0.1.",
        "Coordinates are recorded but do not change the v0.1 civil-time chart.",
    ),
    dispute(
        "DSP-BAZI-LUCK-DIRECTION-001",
        "Explicit or inferred luck-cycle direction",
        "luck-cycle direction",
        [
            (
                "ziping-calculation-baseline",
                "Require callers to select forward or reverse explicitly.",
                ["BAZI-LUCK-DIR-001"],
                [LUNAR_DIRECT],
            ),
            (
                "traditional-gender-polarity",
                "Infer direction from recorded sex and year-stem polarity.",
                ["BAZI-LUCK-DIR-002"],
                [LUNAR_DIRECT],
            ),
        ],
        "ziping-calculation-baseline",
        (
            "Explicit input avoids silently assigning a sensitive attribute "
            "and exposes the lineage choice."
        ),
        "Luck-cycle direction must be selected explicitly in v0.1.",
    ),
    dispute(
        "DSP-BAZI-LUCK-START-001",
        "Luck-cycle start-age conversion",
        "luck-cycle start",
        [
            (
                "ziping-calculation-baseline",
                "Represent the adjacent-term interval as a decimal age at three days per year.",
                ["BAZI-LUCK-START-001"],
                [LUNAR_DIRECT],
            ),
            (
                "calendar-component-conversion",
                (
                    "Convert remaining days and double-hours into year, month, "
                    "day, and hour components."
                ),
                ["BAZI-LUCK-START-002"],
                [LUNAR_DIRECT],
            ),
        ],
        "ziping-calculation-baseline",
        "A decimal age preserves the measured interval and avoids calendar-rounding ambiguity.",
        "The displayed start age uses the three-days-per-year decimal method.",
    ),
    dispute(
        "DSP-BAZI-MONTH-BOUNDARY-001",
        "Exact solar-term instant or whole civil date",
        "month boundary",
        [
            (
                "ziping-calculation-baseline",
                "Change the month pillar at the exact minor solar-term instant.",
                ["BAZI-CAL-MONTH-001"],
                [LUNAR_DIRECT, HKO_CORROBORATING],
            ),
            (
                "whole-day-boundary",
                "Change the month pillar at the start of the term's civil date.",
                ["BAZI-CAL-MONTH-002"],
                [HKO_CORROBORATING],
            ),
        ],
        "ziping-calculation-baseline",
        "The exact astronomical instant is reproducible and avoids a full day of boundary drift.",
        "Month pillars change at the exact solar-term instant in v0.1.",
    ),
]


def write_json(directory: Path, identifier: str, value: dict[str, Any]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{identifier}.json").write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for value in RULES:
        write_json(RULE_DIR, value["rule_id"], value)
    for value in DISPUTES:
        write_json(DISPUTE_DIR, value["dispute_id"], value)
    print(f"Generated {len(RULES)} rules and {len(DISPUTES)} disputes.")


if __name__ == "__main__":
    main()
