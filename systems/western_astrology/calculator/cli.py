from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import AstrologyError, calculate_chart


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate a bounded Western natal chart.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = calculate_chart(json.loads(args.input.read_text(encoding="utf-8")))
    except (AstrologyError, json.JSONDecodeError) as exc:
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
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
