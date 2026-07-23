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

from systems.western_astrology.validator import compare_chart  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare Western chart facts.")
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--imported", type=Path, required=True)
    parser.add_argument("--tolerance-degrees", type=float, default=0.01)
    args = parser.parse_args()
    native = json.loads(args.native.read_text(encoding="utf-8"))
    imported = json.loads(args.imported.read_text(encoding="utf-8"))
    result = compare_chart(
        native,
        imported,
        longitude_tolerance_degrees=args.tolerance_degrees,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
