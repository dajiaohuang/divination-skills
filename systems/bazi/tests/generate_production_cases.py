"""Generate M3 calculation fixtures after deterministic comparator checks.

These fixtures can establish calculation regression coverage. They do not replace
external domain-expert sign-off for interpretive reports.
"""

from __future__ import annotations

from datetime import timedelta
from zoneinfo import ZoneInfo

from systems.bazi.calculator.comparator import (
    lunar_python_reference,
    sxtwl_modern_reference,
)
from systems.bazi.calculator.engine import _jie_terms_for_year, calculate_chart
from systems.bazi.tests.generate_development_cases import (
    SOURCE_HKO,
    SOURCE_LUNAR,
    SOURCE_TIME,
    base_case,
    write_case,
)

SOURCE_SXTWL = {
    "source_id": "SRC-BAZI-SXTWL-MODERN-001",
    "locator": "Independent sxtwl-modern 1.1.2 day-level API",
}


def simple_pillars(payload: dict) -> dict[str, str]:
    chart = calculate_chart(payload)
    return {
        position: pillar["ganzhi"]
        for position, pillar in chart["computed_facts"]["pillars"].items()
    }


def expected_pillars(payload: dict) -> dict:
    return {"computed_facts": {"pillars": simple_pillars(payload)}}


def extra_standard_inputs() -> list[str]:
    values = []
    for index in range(80):
        year = 1901 + (index * 23) % 199
        month = 1 + (index * 7) % 12
        day = 12 + (index * 7) % 10
        hour = (index * 5) % 23
        minute = (index * 13) % 60
        values.append(f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00")
    return values


def generate_standard_cases() -> None:
    for number, local_datetime in enumerate(extra_standard_inputs(), start=21):
        payload = {"local_datetime": local_datetime, "timezone": "Asia/Shanghai"}
        lunar = lunar_python_reference(payload)
        sxtwl = sxtwl_modern_reference(payload)
        engine = simple_pillars(payload)
        if lunar != sxtwl or engine != lunar:
            raise AssertionError(f"Comparator mismatch for production candidate {payload}")
        case = base_case(
            f"CASE-BAZI-STANDARD-{number:03d}",
            f"Two-source four-pillar comparison {number:03d}",
            "standard",
            payload,
            {"computed_facts": {"pillars": engine}},
            [
                "BAZI-CAL-YEAR-001",
                "BAZI-CAL-MONTH-001",
                "BAZI-CAL-DAY-001",
                "BAZI-CAL-HOUR-001",
                "BAZI-TIME-CIVIL-001",
            ],
            sources=[SOURCE_LUNAR, SOURCE_SXTWL],
        )
        case["reviewers"][0]["reviewer_id"] = "two-source-calculation-review"
        case["reviewers"][0]["notes"] = (
            "Engine output matched pinned lunar-python and independent sxtwl-modern APIs; "
            "this is calculation review, not interpretive expert sign-off."
        )
        write_case("golden", case)


def term_edge_specs() -> list[tuple[str, str, dict]]:
    selected = [
        (1901, "立春", "LICHUN"),
        (1950, "惊蛰", "JINGZHE"),
        (1986, "立夏", "LIXIA"),
        (2000, "白露", "BAILU"),
        (2025, "立春", "LICHUN"),
    ]
    specs = []
    zone = ZoneInfo("Asia/Shanghai")
    for year, term_name, term_code in selected:
        term = next(item for item in _jie_terms_for_year(year) if item.name == term_name)
        local_at = term.utc.astimezone(zone).replace(tzinfo=None)
        for suffix, instant in (("BEFORE", local_at - timedelta(seconds=1)), ("AT", local_at)):
            specs.append(
                (
                    f"TERM-{year}-{term_code}-{suffix}",
                    f"{suffix.lower()} {year} {term_name} exact boundary",
                    {
                        "local_datetime": instant.isoformat(),
                        "timezone": "Asia/Shanghai",
                    },
                )
            )
    return specs


def generate_edge_cases() -> None:
    number = 11
    for slug, title, payload in term_edge_specs():
        write_case(
            "edge_cases",
            base_case(
                f"CASE-BAZI-EDGE-{slug}-{number:03d}",
                title,
                "edge_case",
                payload,
                expected_pillars(payload),
                ["BAZI-CAL-YEAR-001", "BAZI-CAL-MONTH-001"],
                sources=[SOURCE_LUNAR, SOURCE_HKO],
            ),
        )
        number += 1

    folds = [
        ("LONDON", "2024-10-27T01:30:00", "Europe/London", 0),
        ("LONDON", "2024-10-27T01:30:00", "Europe/London", 1),
        ("SYDNEY", "2024-04-07T02:30:00", "Australia/Sydney", 0),
        ("SYDNEY", "2024-04-07T02:30:00", "Australia/Sydney", 1),
    ]
    for slug, local_datetime, timezone, fold in folds:
        payload = {"local_datetime": local_datetime, "timezone": timezone, "fold": fold}
        chart = calculate_chart(payload)
        write_case(
            "edge_cases",
            base_case(
                f"CASE-BAZI-EDGE-DST-{slug}-FOLD{fold}-{number:03d}",
                f"Ambiguous {timezone} time with fold {fold}",
                "edge_case",
                payload,
                {
                    "normalized_input": {
                        "utc_datetime": chart["normalized_input"]["utc_datetime"],
                        "fold": fold,
                    }
                },
                ["BAZI-VAL-DST-001"],
                sources=[SOURCE_TIME],
            ),
        )
        number += 1

    global_specs = [
        ("APIA-BEFORE-SKIP", "2011-12-29T12:00:00", "Pacific/Apia"),
        ("KATHMANDU-1986", "1986-01-01T01:00:00", "Asia/Kathmandu"),
        ("PARIS-1940", "1940-06-15T12:00:00", "Europe/Paris"),
        ("KOLKATA-1942", "1942-09-01T12:00:00", "Asia/Kolkata"),
        ("LEAP-2000", "2000-02-29T12:00:00", "UTC"),
        ("STJOHNS-1988", "1988-07-01T12:00:00", "America/St_Johns"),
    ]
    for slug, local_datetime, timezone in global_specs:
        payload = {"local_datetime": local_datetime, "timezone": timezone}
        write_case(
            "edge_cases",
            base_case(
                f"CASE-BAZI-EDGE-{slug}-{number:03d}",
                f"Historical or calendar boundary case in {timezone}",
                "edge_case",
                payload,
                expected_pillars(payload),
                ["BAZI-TIME-CIVIL-001", "BAZI-CAL-DAY-001"],
                sources=[SOURCE_TIME, SOURCE_LUNAR],
            ),
        )
        number += 1
    if number != 31:
        raise AssertionError(f"Expected edge cases through 030, got next index {number}")


def day_boundary_case(number: int, local_datetime: str) -> dict:
    midnight = {
        "local_datetime": local_datetime,
        "timezone": "Asia/Shanghai",
        "day_boundary": "midnight",
    }
    zi_initial = {**midnight, "day_boundary": "zi_initial"}
    values = [simple_pillars(midnight)["day"], simple_pillars(zi_initial)["day"]]
    return base_case(
        f"CASE-BAZI-DISPUTE-DAY-BOUNDARY-{number:03d}",
        "Late-Zi day-boundary alternatives",
        "dispute",
        midnight,
        {"computed_facts": {"day_pillar": values[0]}},
        ["BAZI-CAL-DAY-001", "BAZI-CAL-DAY-002"],
        allowed_disagreements=[
            {
                "dispute_id": "DSP-BAZI-DAY-BOUNDARY-001",
                "field_path": "computed_facts.day_pillar",
                "allowed_values": values,
            }
        ],
    )


def generate_dispute_cases() -> None:
    cases = []
    for offset, date in enumerate(
        [
            "1901-01-15T23:30:00",
            "1966-06-15T23:30:00",
            "2000-02-29T23:30:00",
            "2099-12-15T23:30:00",
        ],
        start=2,
    ):
        cases.append(day_boundary_case(offset, date))

    for number, longitude in enumerate((87.62, 103.82, 121.47), start=2):
        payload = {
            "local_datetime": f"{1980 + number * 7}-07-15T12:00:00",
            "timezone": "Asia/Shanghai",
            "longitude": longitude,
        }
        cases.append(
            base_case(
                f"CASE-BAZI-DISPUTE-SOLAR-TIME-{number:03d}",
                "Civil versus apparent solar time",
                "dispute",
                payload,
                {"normalized_input": {"true_solar_time_applied": False}},
                ["BAZI-TIME-CIVIL-001", "BAZI-TIME-SOLAR-001"],
                allowed_disagreements=[
                    {
                        "dispute_id": "DSP-BAZI-SOLAR-TIME-001",
                        "field_path": "normalized_input.true_solar_time_applied",
                        "allowed_values": [False, True],
                    }
                ],
            )
        )

    for number, date in enumerate(
        ["1960-01-15T12:00:00", "2000-07-15T12:00:00", "2040-10-15T12:00:00"],
        start=2,
    ):
        payload = {
            "local_datetime": date,
            "timezone": "Asia/Shanghai",
            "luck_cycle_direction": "forward",
        }
        cases.append(
            base_case(
                f"CASE-BAZI-DISPUTE-LUCK-DIRECTION-{number:03d}",
                "Explicit luck-cycle direction alternatives",
                "dispute",
                payload,
                {"computed_facts": {"luck_cycles": {"direction": "forward"}}},
                ["BAZI-LUCK-DIR-001", "BAZI-LUCK-DIR-002"],
                allowed_disagreements=[
                    {
                        "dispute_id": "DSP-BAZI-LUCK-DIRECTION-001",
                        "field_path": "computed_facts.luck_cycles.direction",
                        "allowed_values": ["forward", "reverse"],
                    }
                ],
            )
        )

    for number, date in enumerate(
        ["1955-04-15T12:00:00", "1995-08-15T12:00:00", "2035-11-15T12:00:00"],
        start=2,
    ):
        payload = {
            "local_datetime": date,
            "timezone": "Asia/Shanghai",
            "luck_cycle_direction": "forward",
        }
        cases.append(
            base_case(
                f"CASE-BAZI-DISPUTE-LUCK-START-{number:03d}",
                "Luck-cycle start-age conversion alternatives",
                "dispute",
                payload,
                {"computed_facts": {"luck_cycles": {"start_method": "three_days_per_year"}}},
                ["BAZI-LUCK-START-001", "BAZI-LUCK-START-002"],
                allowed_disagreements=[
                    {
                        "dispute_id": "DSP-BAZI-LUCK-START-001",
                        "field_path": "computed_facts.luck_cycles.start_method",
                        "allowed_values": ["three_days_per_year", "calendar_component_conversion"],
                    }
                ],
            )
        )

    for number, date in enumerate(("2000-09-07T08:00:00", "2025-02-03T08:00:00"), start=2):
        payload = {"local_datetime": date, "timezone": "Asia/Shanghai"}
        baseline = simple_pillars(payload)["month"]
        cases.append(
            base_case(
                f"CASE-BAZI-DISPUTE-MONTH-BOUNDARY-{number:03d}",
                "Exact-instant versus whole-day month boundary",
                "dispute",
                payload,
                {"computed_facts": {"month_pillar": baseline}},
                ["BAZI-CAL-MONTH-001", "BAZI-CAL-MONTH-002"],
                allowed_disagreements=[
                    {
                        "dispute_id": "DSP-BAZI-MONTH-BOUNDARY-001",
                        "field_path": "computed_facts.month_pillar",
                        "allowed_values": [
                            baseline,
                            simple_pillars({**payload, "local_datetime": date[:11] + "23:00:00"})[
                                "month"
                            ],
                        ],
                    }
                ],
            )
        )

    if len(cases) != 15:
        raise AssertionError(f"Expected 15 additional disputes, got {len(cases)}")
    for case in cases:
        write_case("disputes", case)


def main() -> None:
    generate_standard_cases()
    generate_edge_cases()
    generate_dispute_cases()
    print("Generated M3 totals: 100 standard, 30 edge, 20 dispute cases.")


if __name__ == "__main__":
    main()
