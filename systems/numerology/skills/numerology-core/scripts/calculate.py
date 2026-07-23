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

from systems.numerology.calculator import NumerologyError, calculate_profile  # noqa: E402
from systems.numerology.core import build_report  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate a traceable numerology profile.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        profile = build_report(
            calculate_profile(json.loads(args.input.read_text(encoding="utf-8")))
        )
    except (NumerologyError, json.JSONDecodeError) as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "code": getattr(exc, "code", "invalid_json"),
                    "message": str(exc),
                }
            )
        )
        return 2
    print(json.dumps(profile, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
