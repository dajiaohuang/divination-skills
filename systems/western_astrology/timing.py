"""Western transit and solar-return structural calculations."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import astronomy
from divination_skills.contracts import stable_identifier

from systems.western_astrology.calculator.engine import (
    ASPECTS,
    _astro_time,
    _longitude,
    calculate_chart,
)


def _signed_delta(target: float, current: float) -> float:
    return (target - current + 180) % 360 - 180


def _separation(left: float, right: float) -> float:
    distance = abs(left - right) % 360
    return min(distance, 360 - distance)


def _cross_aspects(
    transit: dict[str, Any],
    natal: dict[str, Any],
) -> list[dict[str, Any]]:
    facts = []
    for moving in transit["computed_facts"]["positions"]:
        for radix in natal["computed_facts"]["positions"]:
            separation = _separation(
                moving["longitude_degrees"],
                radix["longitude_degrees"],
            )
            for name, exact, allowed_orb in ASPECTS:
                orb = abs(separation - exact)
                if orb <= allowed_orb:
                    facts.append(
                        {
                            "fact_id": f"western.transit.aspect.{len(facts) + 1:03d}",
                            "direction": "transit_to_natal",
                            "transit_body": moving["body"],
                            "transit_fact_id": moving["fact_id"],
                            "natal_body": radix["body"],
                            "natal_fact_id": radix["fact_id"],
                            "aspect": name,
                            "separation_degrees": round(separation, 8),
                            "orb_degrees": round(orb, 8),
                            "allowed_orb_degrees": allowed_orb,
                            "rule_ids": ["WESTERN-TIMING-TRANSIT-001"],
                            "source_ids": [
                                "SRC-WESTERN-ASTRONOMY-ENGINE-001",
                                "SRC-WESTERN-PROJECT-SPEC-001",
                            ],
                        }
                    )
                    break
    return facts


def _solar_return_utc(natal_sun: float, year: int, seed: datetime) -> datetime:
    current = seed.astimezone(UTC)
    for _ in range(12):
        time = _astro_time(current)
        longitude = _longitude(astronomy.Body.Sun, time)[0]
        before = _longitude(astronomy.Body.Sun, time.AddDays(-0.25))[0]
        after = _longitude(astronomy.Body.Sun, time.AddDays(0.25))[0]
        speed = _signed_delta(after, before) / 0.5
        error = _signed_delta(natal_sun, longitude)
        if abs(error) < 1e-8:
            break
        current += timedelta(days=error / speed)
    if current.year not in {year - 1, year, year + 1}:
        raise ValueError("Solar return search did not converge near the requested year.")
    return current


def _return_chart(natal: dict[str, Any], year: int) -> tuple[datetime, dict[str, Any]]:
    timezone = natal["normalized_input"]["timezone"]
    zone = ZoneInfo(timezone)
    birth_local = datetime.fromisoformat(natal["normalized_input"]["local_datetime"])
    try:
        seed_local = birth_local.replace(year=year)
    except ValueError:
        seed_local = birth_local.replace(year=year, day=28)
    natal_sun = next(
        item["longitude_degrees"]
        for item in natal["computed_facts"]["positions"]
        if item["body"] == "sun"
    )
    instant = _solar_return_utc(natal_sun, year, seed_local)
    local = instant.astimezone(zone)
    payload = {
        "local_datetime": local.replace(tzinfo=None).isoformat(),
        "timezone": timezone,
        "longitude": natal["normalized_input"]["longitude"],
        "latitude": natal["normalized_input"]["latitude"],
        "house_system": natal["normalized_input"]["house_system"],
    }
    return instant, calculate_chart(payload)


def calculate_timing(
    natal: dict[str, Any],
    *,
    target_local_datetime: str,
    timezone: str,
    fold: int | None = None,
) -> dict[str, Any]:
    if natal.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Western natal chart is required.")
    transit_payload = {
        "local_datetime": target_local_datetime,
        "timezone": timezone,
        "longitude": natal["normalized_input"]["longitude"],
        "latitude": natal["normalized_input"]["latitude"],
        "house_system": natal["normalized_input"]["house_system"],
    }
    if fold is not None:
        transit_payload["fold"] = fold
    transit = calculate_chart(transit_payload)
    target = datetime.fromisoformat(transit["normalized_input"]["local_datetime"])
    return_instant, return_chart = _return_chart(natal, target.year)
    next_return, _ = _return_chart(natal, target.year + 1)
    chart_id = stable_identifier(
        "CHART-WESTERN",
        {"engine": natal["engine"], "normalized_input": natal["normalized_input"]},
    )
    entries = [
        {
            "entry_id": f"TIME-WESTERN-TRANSIT-{target:%Y%m%d%H%M%S}",
            "scope": "transit",
            "start": target.isoformat(),
            "end": (target + timedelta(seconds=1)).isoformat(),
            "start_inclusive": True,
            "end_inclusive": False,
            "fact_ids": [
                item["fact_id"] for item in transit["computed_facts"]["positions"]
            ],
            "rule_ids": ["WESTERN-TIMING-TRANSIT-001"],
            "confidence": "deterministic",
        },
        {
            "entry_id": f"TIME-WESTERN-RETURN-{target.year}",
            "scope": "return",
            "start": return_instant.isoformat(),
            "end": next_return.isoformat(),
            "start_inclusive": True,
            "end_inclusive": False,
            "fact_ids": [
                next(
                    item["fact_id"]
                    for item in return_chart["computed_facts"]["positions"]
                    if item["body"] == "sun"
                )
            ],
            "rule_ids": ["WESTERN-TIMING-SOLAR-RETURN-001"],
            "confidence": "deterministic",
        },
    ]
    return {
        "schema_version": "0.2.0",
        "system": "western-astrology",
        "lineage": "tropical-geocentric-major-aspects-v0.2",
        "target": transit["normalized_input"],
        "transit_chart": transit,
        "transit_to_natal_aspects": _cross_aspects(transit, natal),
        "solar_return": {
            "return_utc_datetime": return_instant.isoformat().replace("+00:00", "Z"),
            "chart": return_chart,
        },
        "timeline": {
            "schema_version": "0.1.0",
            "timeline_id": stable_identifier(
                "TIMELINE",
                {
                    "chart_id": chart_id,
                    "target": transit["normalized_input"]["utc_datetime"],
                    "entries": entries,
                },
            ),
            "system": "western-astrology",
            "lineage": "tropical-geocentric-major-aspects-v0.2",
            "chart_id": chart_id,
            "entries": entries,
        },
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "structural_timing_only",
                    "message": "Transits and returns are structures, not event predictions.",
                },
                {
                    "code": "progressions_not_included",
                    "message": "Secondary progressions are outside this timing lineage.",
                },
            ],
        },
    }
