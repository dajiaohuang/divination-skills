"""Create an evidence-linked report from a validated Bazi chart JSON file."""

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

from systems.bazi.core import build_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chart", type=Path, help="Validated calculator chart JSON")
    parser.add_argument(
        "--strength-lineage",
        choices=["project-seasonal-support-v0.1"],
        help="Explicitly opt into the experimental, isolated support path.",
    )
    args = parser.parse_args()
    chart = json.loads(args.chart.read_text(encoding="utf-8"))
    json.dump(
        build_report(chart, strength_lineage=args.strength_lineage),
        sys.stdout,
        ensure_ascii=False,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
