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

from systems.ziwei.engine import calculate  # noqa: E402
from systems.ziwei.timing import calculate_timing  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate project-native Ziwei timing.")
    parser.add_argument("--natal-local-datetime", required=True)
    parser.add_argument("--natal-timezone", required=True)
    parser.add_argument("--calculation-gender", choices=("male", "female"), required=True)
    parser.add_argument("--target-local-datetime", required=True)
    parser.add_argument("--target-timezone", required=True)
    parser.add_argument("--natal-fold", type=int, choices=(0, 1))
    parser.add_argument("--target-fold", type=int, choices=(0, 1))
    args = parser.parse_args()
    natal_payload = {
        "local_datetime": args.natal_local_datetime,
        "timezone": args.natal_timezone,
        "calculation_gender": args.calculation_gender,
    }
    if args.natal_fold is not None:
        natal_payload["fold"] = args.natal_fold
    chart = calculate(natal_payload)
    result = calculate_timing(
        chart,
        target_local_datetime=args.target_local_datetime,
        timezone=args.target_timezone,
        fold=args.target_fold,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
