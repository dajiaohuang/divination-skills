from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import NumerologyError, calculate_profile


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate a project numerology profile.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        profile = calculate_profile(json.loads(args.input.read_text(encoding="utf-8")))
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
