"""Bazi luck-cycle and calendar activation facts."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from divination_skills.contracts import stable_identifier
from divination_skills.time import TimeNormalizationError, localize_strict

from systems.bazi.calculator.engine import (
    PAIR_RELATIONS,
    calculate_chart,
    solar_year_boundaries,
)

SECONDS_PER_YEAR = 365.2425 * 86_400


def _cross_relations(
    natal_pillars: dict[str, Any],
    period_pillars: dict[str, Any],
) -> list[dict[str, Any]]:
    facts = []
    for natal_name, natal in natal_pillars.items():
        natal_branch = natal["branch"]["name"]
        for period_name, period in period_pillars.items():
            period_branch = period["branch"]["name"]
            for relation, pairs in PAIR_RELATIONS.items():
                if tuple(sorted((natal_branch, period_branch))) in {
                    tuple(sorted(pair)) for pair in pairs
                }:
                    facts.append(
                        {
                            "fact_id": (
                                f"bazi.timing.relation.{len(facts) + 1:03d}"
                            ),
                            "relation": relation,
                            "natal_position": natal_name,
                            "natal_branch": natal_branch,
                            "period_position": period_name,
                            "period_branch": period_branch,
                            "rule_ids": ["BAZI-TIMING-ACTIVATION-001"],
                            "source_ids": ["SRC-BAZI-PROJECT-SPEC-001"],
                        }
                    )
    return facts


def calculate_timing(
    chart: dict[str, Any],
    *,
    target_local_datetime: str,
    timezone: str,
    fold: int | None = None,
) -> dict[str, Any]:
    if chart.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid native Bazi chart is required.")
    luck = chart.get("computed_facts", {}).get("luck_cycles")
    if luck is None:
        raise ValueError("Bazi timing requires an explicitly calculated luck-cycle direction.")
    try:
        target, resolved_fold = localize_strict(target_local_datetime, timezone, fold)
    except TimeNormalizationError as exc:
        raise ValueError(exc.message) from exc
    birth = datetime.fromisoformat(chart["normalized_input"]["utc_datetime"].replace("Z", "+00:00"))
    target_utc = target.astimezone(UTC)
    if target_utc < birth:
        raise ValueError("target_local_datetime precedes birth.")
    age_years = (target_utc - birth).total_seconds() / SECONDS_PER_YEAR
    active_cycle = next(
        (
            cycle
            for cycle in luck["cycles"]
            if cycle["start_age_years"] <= age_years < cycle["end_age_years"]
        ),
        None,
    )
    target_payload = {
        "local_datetime": target_local_datetime,
        "timezone": timezone,
        "day_boundary": chart["normalized_input"]["day_boundary"],
    }
    if fold is not None:
        target_payload["fold"] = fold
    period_chart = calculate_chart(target_payload)
    period_pillars = {
        "year": period_chart["computed_facts"]["pillars"]["year"],
        "month": period_chart["computed_facts"]["pillars"]["month"],
    }
    activations = _cross_relations(
        chart["computed_facts"]["pillars"],
        period_pillars,
    )
    entries = []
    if active_cycle:
        cycle_start = birth + timedelta(
            seconds=active_cycle["start_age_years"] * SECONDS_PER_YEAR
        )
        cycle_end = birth + timedelta(
            seconds=active_cycle["end_age_years"] * SECONDS_PER_YEAR
        )
        entries.append(
            {
                "entry_id": f"TIME-BAZI-MAJOR-{active_cycle['number']:03d}",
                "scope": "major_period",
                "start": cycle_start.isoformat(),
                "end": cycle_end.isoformat(),
                "start_inclusive": True,
                "end_inclusive": False,
                "fact_ids": ["bazi.luck_cycles"],
                "rule_ids": ["BAZI-TIMING-LUCK-CYCLE-001"],
                "confidence": "deterministic",
            }
        )
    solar_year = period_chart["computed_facts"]["solar_year"]
    solar_year_start, solar_year_end = solar_year_boundaries(solar_year)
    solar_month_start = datetime.fromisoformat(
        period_chart["computed_facts"]["previous_month_boundary"][
            "utc_datetime"
        ].replace("Z", "+00:00")
    )
    solar_month_end = datetime.fromisoformat(
        period_chart["computed_facts"]["next_month_boundary"]["utc_datetime"].replace(
            "Z", "+00:00"
        )
    )
    entries.extend(
        [
            {
                "entry_id": f"TIME-BAZI-SOLAR-YEAR-{solar_year}",
                "scope": "year",
                "start": solar_year_start.utc.isoformat(),
                "end": solar_year_end.utc.isoformat(),
                "start_inclusive": True,
                "end_inclusive": False,
                "fact_ids": [period_pillars["year"]["fact_id"]],
                "rule_ids": ["BAZI-TIMING-ACTIVATION-001"],
                "confidence": "deterministic",
            },
            {
                "entry_id": (
                    "TIME-BAZI-SOLAR-MONTH-"
                    f"{solar_month_start:%Y%m%d%H%M%S}"
                ),
                "scope": "month",
                "start": solar_month_start.isoformat(),
                "end": solar_month_end.isoformat(),
                "start_inclusive": True,
                "end_inclusive": False,
                "fact_ids": [period_pillars["month"]["fact_id"]],
                "rule_ids": ["BAZI-TIMING-ACTIVATION-001"],
                "confidence": "deterministic",
            },
        ]
    )
    chart_id = stable_identifier(
        "CHART-BAZI",
        {"engine": chart["engine"], "normalized_input": chart["normalized_input"]},
    )
    return {
        "schema_version": "0.2.0",
        "system": "bazi",
        "lineage": "ziping-calculation-baseline",
        "target": {
            "local_datetime": target.isoformat(),
            "utc_datetime": target_utc.isoformat().replace("+00:00", "Z"),
            "timezone": timezone,
            "fold": resolved_fold,
            "age_years": round(age_years, 8),
        },
        "active_luck_cycle": active_cycle,
        "period_pillars": period_pillars,
        "activations": activations,
        "timeline": {
            "schema_version": "0.1.0",
            "timeline_id": stable_identifier(
                "TIMELINE",
                {"chart_id": chart_id, "target": target_utc.isoformat(), "entries": entries},
            ),
            "system": "bazi",
            "lineage": "ziping-calculation-baseline",
            "chart_id": chart_id,
            "entries": entries,
        },
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "structural_timing_only",
                    "message": "Activations are structural relations, not event predictions.",
                }
            ],
        },
    }
