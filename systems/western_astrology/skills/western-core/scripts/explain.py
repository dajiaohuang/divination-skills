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

from systems.western_astrology.core import build_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Explain validated Western natal facts.")
    parser.add_argument("chart", type=Path)
    args = parser.parse_args()
    report = build_report(json.loads(args.chart.read_text(encoding="utf-8")))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
