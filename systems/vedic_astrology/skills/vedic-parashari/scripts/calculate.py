from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = (
    SCRIPT_ROOT if (SCRIPT_ROOT / "systems").is_dir() else Path(__file__).resolve().parents[5]
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from systems.vedic_astrology.calculator.engine import (  # noqa: E402
    VedicAstrologyError,
    calculate_chart,
)


def main() -> int:
    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        payload["lineages"] = ["parashari"]
        print(json.dumps(calculate_chart(payload), ensure_ascii=False, indent=2))
        return 0
    except (IndexError, OSError, json.JSONDecodeError, VedicAstrologyError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
