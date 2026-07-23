"""Generate the 20 synthetic M3 invalid-input regression fixtures."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "invalid_inputs"

SPECS = [
    ("MISSING-DATETIME", {}, "missing_local_datetime", "local_datetime"),
    (
        "MISSING-TIMEZONE",
        {"local_datetime": "2024-01-01T00:00:00"},
        "missing_timezone",
        "timezone",
    ),
    (
        "INVALID-DATETIME",
        {"local_datetime": "2024-02-30T00:00:00", "timezone": "UTC"},
        "invalid_local_datetime",
        "ISO 8601",
    ),
    (
        "OFFSET-NOT-ALLOWED",
        {"local_datetime": "2024-01-01T00:00:00+08:00", "timezone": "Asia/Shanghai"},
        "offset_not_allowed",
        "UTC offset",
    ),
    (
        "YEAR-BELOW-RANGE",
        {"local_datetime": "1899-12-31T23:59:59", "timezone": "UTC"},
        "date_out_of_range",
        "1900 through 2100",
    ),
    (
        "YEAR-ABOVE-RANGE",
        {"local_datetime": "2101-01-01T00:00:00", "timezone": "UTC"},
        "date_out_of_range",
        "1900 through 2100",
    ),
    (
        "NONEXISTENT-DST",
        {"local_datetime": "2024-03-10T02:30:00", "timezone": "America/New_York"},
        "nonexistent_local_time",
        "does not exist",
    ),
    (
        "AMBIGUOUS-DST",
        {"local_datetime": "2024-11-03T01:30:00", "timezone": "America/New_York"},
        "ambiguous_local_time",
        "occurs twice",
    ),
    (
        "FOLD-WRONG-TYPE",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "fold": "0"},
        "invalid_fold",
        "0 or 1",
    ),
    (
        "FOLD-OUT-OF-RANGE",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "fold": 2},
        "invalid_fold",
        "0 or 1",
    ),
    (
        "DAY-BOUNDARY",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "day_boundary": "noon"},
        "invalid_day_boundary",
        "midnight",
    ),
    (
        "TRUE-SOLAR-TIME",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "true_solar_time": True},
        "true_solar_time_unsupported",
        "not implemented",
    ),
    (
        "UNKNOWN-FIELD",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "gender": "x"},
        "unknown_fields",
        "gender",
    ),
    (
        "UNKNOWN-TIMEZONE",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "Mars/Olympus"},
        "unknown_timezone",
        "Unknown IANA",
    ),
    (
        "LUCK-DIRECTION",
        {
            "local_datetime": "2024-01-01T00:00:00",
            "timezone": "UTC",
            "luck_cycle_direction": "auto",
        },
        "invalid_luck_cycle_direction",
        "forward",
    ),
    (
        "LONGITUDE-HIGH",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "longitude": 181},
        "invalid_longitude",
        "-180 and 180",
    ),
    (
        "LONGITUDE-LOW",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "longitude": -181},
        "invalid_longitude",
        "-180 and 180",
    ),
    (
        "LATITUDE-HIGH",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "latitude": 91},
        "invalid_latitude",
        "-90 and 90",
    ),
    (
        "LATITUDE-LOW",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC", "latitude": -91},
        "invalid_latitude",
        "-90 and 90",
    ),
    (
        "EMPTY-TIMEZONE",
        {"local_datetime": "2024-01-01T00:00:00", "timezone": ""},
        "missing_timezone",
        "timezone",
    ),
]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for number, (slug, payload, code, message) in enumerate(SPECS, start=1):
        case = {
            "case_id": f"CASE-BAZI-INVALID-{slug}-{number:03d}",
            "title": slug.replace("-", " ").title(),
            "input": payload,
            "expected_error_code": code,
            "expected_message_contains": message,
            "data_classification": "synthetic",
        }
        (ROOT / f"{case['case_id']}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(f"Generated {len(SPECS)} invalid-input cases.")


if __name__ == "__main__":
    main()
