"""Create a repository-relative SHA-256 evidence record for a human review artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def evidence_record(root: Path, path: Path) -> dict[str, Any]:
    root = root.resolve()
    path = path.resolve()
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise ValueError("evidence file must be retained inside the repository") from exc
    if not path.is_file():
        raise ValueError("evidence path must identify a file")
    return {
        "locator": relative.as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "retained_in_repository": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path", type=Path, help="review evidence file retained under the repository"
    )
    parser.add_argument("--root", type=Path, default=Path("."), help="repository root")
    args = parser.parse_args(argv)
    try:
        record = evidence_record(args.root, args.path)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
