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
    parser.add_argument("--local-datetime", required=True)
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--calculation-gender", choices=("male", "female"), required=True)
    parser.add_argument("--fold", type=int, choices=(0, 1))
    args = parser.parse_args()
    payload = {
        "local_datetime": args.local_datetime,
        "timezone": args.timezone,
        "calculation_gender": args.calculation_gender,
    }
    if args.fold is not None:
        payload["fold"] = args.fold
    print(json.dumps(structural_report(calculate(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
