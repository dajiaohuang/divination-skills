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

from systems.runes.engine import draw, explain  # noqa: E402
from systems.runes.layers import build_layers  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an auditable rune report.")
    parser.add_argument("--spread", choices=("single", "three-rune"), required=True)
    parser.add_argument("--question", default="")
    parser.add_argument("--seed-hex")
    args = parser.parse_args()
    payload = {"spread": args.spread, "question": args.question}
    if args.seed_hex:
        payload["seed_hex"] = args.seed_hex
    draw_result = draw(payload)
    print(
        json.dumps(
            {"report": explain(draw_result), "layers": build_layers(draw_result)},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
