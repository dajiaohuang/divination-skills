"""Run the repository's canonical Bazi calculator from the source Skill."""

from __future__ import annotations

import sys
from importlib import import_module
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = (
    SCRIPT_ROOT if (SCRIPT_ROOT / "systems").is_dir() else Path(__file__).resolve().parents[5]
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

main = import_module("systems.bazi.calculator.cli").main


if __name__ == "__main__":
    raise SystemExit(main())
