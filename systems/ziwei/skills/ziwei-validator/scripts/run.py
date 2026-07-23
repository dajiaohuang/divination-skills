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

from systems.ziwei.validator import compare_chart  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare structured Ziwei charts.")
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--imported", type=Path, required=True)
    args = parser.parse_args()
    native = json.loads(args.native.read_text(encoding="utf-8"))
    imported = json.loads(args.imported.read_text(encoding="utf-8"))
    print(json.dumps(compare_chart(native, imported), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
