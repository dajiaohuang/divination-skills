from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = (
    SCRIPT_ROOT
    if (SCRIPT_ROOT / "systems").is_dir()
    else Path(__file__).resolve().parents[5]
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from systems.liuyao.judgment import QUESTION_PACKS, analyze  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply bounded Liuyao judgment rule packs.")
    parser.add_argument("--chart", type=Path, required=True)
    parser.add_argument("--question-category", choices=tuple(QUESTION_PACKS), required=True)
    parser.add_argument("--include-timing", action="store_true")
    args = parser.parse_args()
    chart = json.loads(args.chart.read_text(encoding="utf-8"))
    result = analyze(
        chart,
        question_category=args.question_category,
        include_timing=args.include_timing,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
