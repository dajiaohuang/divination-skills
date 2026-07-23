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

from systems.western_astrology.rectifier import scan_candidates  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan Western birth-time intervals.")
    parser.add_argument("--birth-date", required=True)
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--longitude", type=float, required=True)
    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--interval-minutes", type=int, choices=(15, 30, 60), default=30)
    args = parser.parse_args()
    events = json.loads(args.events.read_text(encoding="utf-8"))
    result = scan_candidates(
        birth_date=args.birth_date,
        timezone=args.timezone,
        longitude=args.longitude,
        latitude=args.latitude,
        events=events,
        interval_minutes=args.interval_minutes,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
