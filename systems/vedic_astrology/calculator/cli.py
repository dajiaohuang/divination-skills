"""JSON command-line interface for the Vedic astrology calculator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import VedicAstrologyError, calculate_chart


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="JSON input path; stdin when omitted")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        if args.input:
            payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        else:
            payload = json.load(sys.stdin)
        result = calculate_chart(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
        return 0
    except (OSError, json.JSONDecodeError, VedicAstrologyError) as exc:
        code = getattr(exc, "code", "invalid_input")
        print(json.dumps({"error": {"code": code, "message": str(exc)}}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
