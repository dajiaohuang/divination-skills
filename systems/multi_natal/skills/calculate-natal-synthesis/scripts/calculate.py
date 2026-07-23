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

from systems.multi_natal.engine import (  # noqa: E402
    NatalSynthesisError,
    calculate_natal_synthesis,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate all supported birth-based systems and a bounded synthesis."
    )
    parser.add_argument("input", type=Path, help="UTF-8 JSON birth-profile input")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = calculate_natal_synthesis(payload)
    except (OSError, json.JSONDecodeError, NatalSynthesisError) as exc:
        error = {
            "error": getattr(exc, "code", "invalid_input"),
            "message": str(exc),
        }
        print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
