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

from systems.ziwei.reader import read_structured  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Read structured Ziwei JSON.")
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    value = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(read_structured(value), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
