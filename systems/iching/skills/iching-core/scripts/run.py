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

from systems.iching.engine import cast, explain  # noqa: E402
from systems.iching.text_layer import POLICIES, build_classical_layer  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an auditable three-coin I Ching report.")
    parser.add_argument("--question", default="")
    parser.add_argument("--seed-hex")
    parser.add_argument(
        "--policy-id",
        choices=tuple(sorted(POLICIES)),
        default="all-moving-lines-v0.2",
    )
    args = parser.parse_args()
    payload = {"question": args.question}
    if args.seed_hex:
        payload["seed_hex"] = args.seed_hex
    cast_result = cast(payload)
    print(
        json.dumps(
            {
                "report": explain(cast_result),
                "classical_layer": build_classical_layer(
                    cast_result,
                    policy_id=args.policy_id,
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
