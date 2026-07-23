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

from systems.tarot.combinations import analyze_combinations  # noqa: E402
from systems.tarot.core import build_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Explain a validated Tarot draw.")
    parser.add_argument("draw", type=Path)
    parser.add_argument("--with-combinations", action="store_true")
    args = parser.parse_args()
    draw = json.loads(args.draw.read_text(encoding="utf-8"))
    report = build_report(draw)
    output = {
        "report": report,
        "combinations": analyze_combinations(draw) if args.with_combinations else None,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
