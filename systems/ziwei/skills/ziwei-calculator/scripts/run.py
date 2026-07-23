from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = (
    SCRIPT_ROOT if (SCRIPT_ROOT / "systems").is_dir() else Path(__file__).resolve().parents[5]
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from systems.ziwei.engine import calculate, structural_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate a normalized Ziwei natal chart.")
    parser.add_argument("--calendar-type", choices=("solar", "lunar"), default="solar")
    parser.add_argument("--local-datetime")
    parser.add_argument("--lunar-date")
    parser.add_argument("--is-leap-month", action="store_true")
    parser.add_argument("--time-index", type=int, choices=range(13))
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--calculation-gender", choices=("male", "female"), required=True)
    parser.add_argument("--fold", type=int, choices=(0, 1))
    parser.add_argument(
        "--year-boundary",
        choices=("lunar_new_year", "spring_commences"),
        default="lunar_new_year",
    )
    parser.add_argument(
        "--late-zi-policy",
        choices=("current_day", "next_day"),
        default="current_day",
    )
    parser.add_argument(
        "--leap-month-policy",
        choices=("preserve", "split_after_15"),
        default="preserve",
    )
    args = parser.parse_args()
    payload = {
        "calendar_type": args.calendar_type,
        "timezone": args.timezone,
        "calculation_gender": args.calculation_gender,
        "year_boundary": args.year_boundary,
        "late_zi_policy": args.late_zi_policy,
        "leap_month_policy": args.leap_month_policy,
    }
    if args.calendar_type == "solar":
        if not args.local_datetime:
            parser.error("--local-datetime is required for solar input")
        payload["local_datetime"] = args.local_datetime
    else:
        if not args.lunar_date or args.time_index is None:
            parser.error("--lunar-date and --time-index are required for lunar input")
        payload["lunar_date"] = args.lunar_date
        payload["is_leap_month"] = args.is_leap_month
        payload["time_index"] = args.time_index
    if args.fold is not None:
        payload["fold"] = args.fold
    print(json.dumps(structural_report(calculate(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
