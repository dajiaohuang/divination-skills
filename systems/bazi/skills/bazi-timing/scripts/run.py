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

from systems.bazi.timing import calculate_timing  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate Bazi structural timing.")
    parser.add_argument("--chart", type=Path, required=True)
    parser.add_argument("--target-local-datetime", required=True)
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--fold", type=int, choices=(0, 1))
    args = parser.parse_args()
    chart = json.loads(args.chart.read_text(encoding="utf-8"))
    result = calculate_timing(
        chart,
        target_local_datetime=args.target_local_datetime,
        timezone=args.timezone,
        fold=args.fold,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
