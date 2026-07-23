"""Project-native Ziwei dynamic layers and normalized timeline output."""

from __future__ import annotations

from calendar import monthrange
from datetime import UTC, datetime, timedelta
from typing import Any

from divination_skills.contracts import stable_identifier
from divination_skills.time import TimeNormalizationError, localize_strict
from lunar_python import Solar

from systems.ziwei.analyzer import find_star
from systems.ziwei.engine import (
    LINEAGE,
    TRANSFORMATION_LABELS,
    TRANSFORMATIONS,
    ZiweiError,
    _time_index,
)
from systems.ziwei.star_catalog import (
    LU_CUN_BY_STEM,
    TIAN_MA_BY_GROUP,
    branch_index,
    group_value,
)


def _iso(value: datetime) -> str:
    return value.isoformat()


def _layer(
    chart: dict[str, Any],
    *,
    scope: str,
    index: int,
    stem: str,
    branch: str,
    fact_id: str,
) -> dict[str, Any]:
    target_palace = chart["computed_facts"]["palaces"][index]
    transformations = []
    for star_name, label in zip(
        TRANSFORMATIONS[stem],
        TRANSFORMATION_LABELS,
        strict=True,
    ):
        for match in find_star(chart, star_name):
            transformations.append(
                {
                    "scope": scope,
                    "origin_palace_fact_id": target_palace["fact_id"],
                    "origin_stem": stem,
                    "target_star": star_name,
                    "target_star_fact_id": match["star"]["fact_id"],
                    "target_palace_fact_id": match["palace_fact_id"],
                    "transformation": label,
                    "self_transformation": match["palace_fact_id"]
                    == target_palace["fact_id"],
                    "fact_id": (
                        f"{fact_id}.transformation."
                        f"{len(transformations) + 1:03d}"
                    ),
                    "rule_ids": ["ZIWEI-TRANSFORMATION-DYNAMIC-001"],
                    "source_ids": ["SRC-ZIWEI-PROJECT-SPEC-001"],
                }
            )
    lu_cun_index = branch_index(LU_CUN_BY_STEM[stem])
    flow_placements = (
        ("流禄", lu_cun_index),
        ("流羊", (lu_cun_index + 1) % 12),
        ("流陀", (lu_cun_index - 1) % 12),
        ("流马", branch_index(group_value(branch, TIAN_MA_BY_GROUP))),
    )
    flow_stars = [
        {
            "name": name,
            "palace_index": star_index,
            "palace_fact_id": chart["computed_facts"]["palaces"][star_index]["fact_id"],
            "fact_id": f"{fact_id}.flow-star.{position:03d}",
            "rule_ids": ["ZIWEI-STAR-FLOW-001"],
            "source_ids": [
                "SRC-ZIWEI-PROJECT-SPEC-001",
                "SRC-ZIWEI-QUANSHU-001",
            ],
        }
        for position, (name, star_index) in enumerate(flow_placements, start=1)
    ]
    return {
        "scope": scope,
        "palace_index": index,
        "palace_name": target_palace["name"],
        "palace_fact_id": target_palace["fact_id"],
        "heavenly_stem": stem,
        "earthly_branch": branch,
        "transformations": transformations,
        "flow_stars": flow_stars,
        "fact_id": fact_id,
        "rule_ids": ["ZIWEI-TIMING-ROTATION-001"],
        "source_ids": ["SRC-ZIWEI-PROJECT-SPEC-001"],
    }


def _entry(
    *,
    entry_id: str,
    scope: str,
    start: datetime,
    end: datetime,
    fact_ids: list[str],
    rule_ids: list[str],
) -> dict[str, Any]:
    return {
        "entry_id": entry_id,
        "scope": scope,
        "start": _iso(start),
        "end": _iso(end),
        "start_inclusive": True,
        "end_inclusive": False,
        "fact_ids": fact_ids,
        "rule_ids": rule_ids,
        "confidence": "deterministic",
    }


def calculate_timing(
    chart: dict[str, Any],
    *,
    target_local_datetime: str,
    timezone: str,
    fold: int | None = None,
) -> dict[str, Any]:
    """Calculate bounded decadal, minor, annual, monthly, daily, and hourly facts."""

    if chart.get("validation", {}).get("status") != "valid":
        raise ZiweiError("invalid_chart", "A valid natal chart is required.")
    if chart.get("normalized_input", {}).get("lineage") != LINEAGE:
        raise ZiweiError("lineage_mismatch", f"Expected lineage {LINEAGE}.")
    try:
        target, resolved_fold = localize_strict(target_local_datetime, timezone, fold)
    except TimeNormalizationError as exc:
        raise ZiweiError(exc.code, exc.message) from exc

    solar = Solar.fromYmdHms(
        target.year,
        target.month,
        target.day,
        target.hour,
        target.minute,
        target.second,
    )
    lunar = solar.getLunar()
    palaces = chart["computed_facts"]["palaces"]
    birth = datetime.fromisoformat(chart["normalized_input"]["local_datetime"])
    nominal_age = target.year - birth.year + 1
    if nominal_age < 1:
        raise ZiweiError("target_before_birth", "target_local_datetime precedes the natal year.")

    soul_index = next(item["index"] for item in palaces if item["isOriginalPalace"])
    birth_branch = chart["computed_facts"]["raw_dates"]["year_branch"]
    annual_index = (
        soul_index
        + "子丑寅卯辰巳午未申酉戌亥".index(lunar.getYearZhi())
        - "子丑寅卯辰巳午未申酉戌亥".index(birth_branch)
    ) % 12
    month_index = (annual_index + abs(lunar.getMonth()) - 1) % 12
    day_index = (month_index + lunar.getDay() - 1) % 12
    hour_index = (day_index + _time_index(target.hour) % 12) % 12

    decadal_palace = next(
        (
            item
            for item in palaces
            if item["decadal"]["start_age"] <= nominal_age <= item["decadal"]["end_age"]
        ),
        None,
    )
    minor_palace = next(
        (item for item in palaces if nominal_age in item["minor_limit_ages"]),
        None,
    )
    layers: dict[str, Any] = {}
    if decadal_palace:
        layers["decadal"] = _layer(
            chart,
            scope="major_period",
            index=decadal_palace["index"],
            stem=decadal_palace["heavenlyStem"],
            branch=decadal_palace["earthlyBranch"],
            fact_id=f"ziwei.timing.decadal.age-{nominal_age:03d}",
        )
    if minor_palace:
        layers["minor_limit"] = _layer(
            chart,
            scope="subperiod",
            index=minor_palace["index"],
            stem=minor_palace["heavenlyStem"],
            branch=minor_palace["earthlyBranch"],
            fact_id=f"ziwei.timing.minor.age-{nominal_age:03d}",
        )
    for key, scope, index, stem, branch in (
        ("annual", "year", annual_index, lunar.getYearGan(), lunar.getYearZhi()),
        ("monthly", "month", month_index, lunar.getMonthGan(), lunar.getMonthZhi()),
        ("daily", "day", day_index, lunar.getDayGan(), lunar.getDayZhi()),
        ("hourly", "hour", hour_index, lunar.getTimeGan(), lunar.getTimeZhi()),
    ):
        layers[key] = _layer(
            chart,
            scope=scope,
            index=index,
            stem=stem,
            branch=branch,
            fact_id=f"ziwei.timing.{key}.{target:%Y%m%d%H%M%S}",
        )

    year_start = target.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    year_end = year_start.replace(year=year_start.year + 1)
    month_start = target.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_days = monthrange(target.year, target.month)[1]
    month_end = month_start + timedelta(days=month_days)
    day_start = target.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    target_time_index = _time_index(target.hour)
    if target_time_index == 0:
        hour_start = target.replace(hour=0, minute=0, second=0, microsecond=0)
        hour_end = hour_start + timedelta(hours=1)
    elif target_time_index == 12:
        hour_start = target.replace(hour=23, minute=0, second=0, microsecond=0)
        hour_end = hour_start + timedelta(hours=1)
    else:
        hour_start = target.replace(
            hour=target_time_index * 2 - 1,
            minute=0,
            second=0,
            microsecond=0,
        )
        hour_end = hour_start + timedelta(hours=2)

    entries = [
        _entry(
            entry_id=f"TIME-ZIWEI-YEAR-{target:%Y}",
            scope="year",
            start=year_start,
            end=year_end,
            fact_ids=[layers["annual"]["fact_id"]],
            rule_ids=["ZIWEI-TIMING-ROTATION-001"],
        ),
        _entry(
            entry_id=f"TIME-ZIWEI-MONTH-{target:%Y%m}",
            scope="month",
            start=month_start,
            end=month_end,
            fact_ids=[layers["monthly"]["fact_id"]],
            rule_ids=["ZIWEI-TIMING-ROTATION-001"],
        ),
        _entry(
            entry_id=f"TIME-ZIWEI-DAY-{target:%Y%m%d}",
            scope="day",
            start=day_start,
            end=day_end,
            fact_ids=[layers["daily"]["fact_id"]],
            rule_ids=["ZIWEI-TIMING-ROTATION-001"],
        ),
        _entry(
            entry_id=f"TIME-ZIWEI-HOUR-{target:%Y%m%d%H}",
            scope="hour",
            start=hour_start,
            end=hour_end,
            fact_ids=[layers["hourly"]["fact_id"]],
            rule_ids=["ZIWEI-TIMING-ROTATION-001"],
        ),
    ]
    if "decadal" in layers:
        start_year = birth.year + decadal_palace["decadal"]["start_age"] - 1
        end_year = birth.year + decadal_palace["decadal"]["end_age"]
        entries.insert(
            0,
            _entry(
                entry_id=(
                    f"TIME-ZIWEI-MAJOR-"
                    f"{decadal_palace['decadal']['start_age']:03d}"
                ),
                scope="major_period",
                start=target.replace(
                    year=start_year,
                    month=1,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
                end=target.replace(
                    year=end_year,
                    month=1,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                ),
                fact_ids=[layers["decadal"]["fact_id"]],
                rule_ids=["ZIWEI-CYCLE-DECADAL-001"],
            ),
        )

    chart_id = stable_identifier(
        "CHART-ZIWEI",
        {
            "normalized_input": chart["normalized_input"],
            "engine": chart["engine"],
        },
    )
    timeline_identity = {
        "chart_id": chart_id,
        "target": target.astimezone(UTC).isoformat(),
        "entries": entries,
    }
    return {
        "schema_version": "0.4.0",
        "system": "ziwei",
        "lineage": LINEAGE,
        "target": {
            "local_datetime": target.isoformat(),
            "utc_datetime": target.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "timezone": timezone,
            "fold": resolved_fold,
            "nominal_age": nominal_age,
        },
        "layers": layers,
        "timeline": {
            "schema_version": "0.1.0",
            "timeline_id": stable_identifier("TIMELINE", timeline_identity),
            "system": "ziwei",
            "lineage": LINEAGE,
            "chart_id": chart_id,
            "entries": entries,
        },
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "structural_timing_only",
                    "message": "Dynamic layers describe structure, not guaranteed events.",
                },
                {
                    "code": "nominal_age_policy",
                    "message": (
                        "Major and minor limits use target Gregorian year minus "
                        "birth year plus one."
                    ),
                },
            ],
        },
    }
