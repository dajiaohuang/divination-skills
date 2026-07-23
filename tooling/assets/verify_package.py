"""Verify every declared file in an extracted divination Skill package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def verify(root: Path) -> list[str]:
    root = root.resolve()
    manifest_path = root / "CONTENT_MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"could not load CONTENT_MANIFEST.json: {exc}"]
    errors = []
    for item in manifest.get("files", []):
        relative = item.get("path")
        if not isinstance(relative, str):
            errors.append("content manifest contains a non-string path")
            continue
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            errors.append(f"path escapes package: {relative}")
            continue
        if not path.is_file():
            errors.append(f"missing file: {relative}")
            continue
        payload = path.read_bytes()
        if len(payload) != item.get("size"):
            errors.append(f"size mismatch: {relative}")
        if hashlib.sha256(payload).hexdigest() != item.get("sha256"):
            errors.append(f"hash mismatch: {relative}")
    return sorted(set(errors))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = verify(root)
    print(
        json.dumps(
            {"status": "verified" if not errors else "invalid", "errors": errors},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
