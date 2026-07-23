from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import DrawError, draw_cards


def main() -> int:
    parser = argparse.ArgumentParser(description="Produce an auditable Tarot draw.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        result = draw_cards(json.loads(args.input.read_text(encoding="utf-8")))
    except (DrawError, json.JSONDecodeError) as exc:
        code = getattr(exc, "code", "invalid_json")
        print(json.dumps({"status": "error", "code": code, "message": str(exc)}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
