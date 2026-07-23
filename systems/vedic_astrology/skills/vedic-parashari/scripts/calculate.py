from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = (
    SCRIPT_ROOT if (SCRIPT_ROOT / "systems").is_dir() else Path(__file__).resolve().parents[5]
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from systems.vedic_astrology.lineage_cli import run_lineage_cli  # noqa: E402


def main() -> int:
    return run_lineage_cli(
        "parashari", "Calculate the bounded Parashari structural layer."
    )


if __name__ == "__main__":
    raise SystemExit(main())
