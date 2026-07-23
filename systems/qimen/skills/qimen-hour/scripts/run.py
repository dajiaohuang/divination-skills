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

from systems.qimen.engine import calculate, explain  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate a bounded Chaibu Qimen foundation.")
    parser.add_argument("--local-datetime", required=True)
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--day-boundary", choices=("midnight", "zi_initial"), default="midnight")
    args = parser.parse_args()
    result = calculate(
        {
            "local_datetime": args.local_datetime,
            "timezone": args.timezone,
            "day_boundary": args.day_boundary,
        }
    )
    print(json.dumps(explain(result), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
