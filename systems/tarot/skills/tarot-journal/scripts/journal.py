from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = (
    SCRIPT_ROOT
    if (SCRIPT_ROOT / "systems").is_dir()
    else Path(__file__).resolve().parents[5]
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from systems.tarot.journal import (  # noqa: E402
    JournalError,
    append_entry,
    descriptive_statistics,
    load_entries,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage a consent-gated local Tarot journal.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    append = subparsers.add_parser("append")
    append.add_argument("--journal", type=Path, required=True)
    append.add_argument("--draw", type=Path, required=True)
    append.add_argument("--reflection-file", type=Path, required=True)
    append.add_argument("--tag", action="append", default=[])
    append.add_argument("--consent-to-store", action="store_true")
    append.add_argument("--occurred-at")
    stats = subparsers.add_parser("stats")
    stats.add_argument("--journal", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "append":
            result = append_entry(
                args.journal,
                json.loads(args.draw.read_text(encoding="utf-8")),
                reflection=args.reflection_file.read_text(encoding="utf-8"),
                tags=args.tag,
                consent_to_store=args.consent_to_store,
                occurred_at=args.occurred_at,
            )
        else:
            result = descriptive_statistics(load_entries(args.journal))
    except (JournalError, json.JSONDecodeError, OSError) as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "code": getattr(exc, "code", "journal_io_error"),
                    "message": str(exc),
                }
            )
        )
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
