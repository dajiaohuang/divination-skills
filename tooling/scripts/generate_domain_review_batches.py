"""Create or extend pending domain-review batches without overwriting human decisions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def _case_ids(system: Path) -> list[str]:
    identifiers: list[str] = []
    for relative in ("tests/golden", "tests/edge_cases", "tests/disputes"):
        for path in sorted((system / relative).glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            identifiers.append(document["case_id"])
    return sorted(identifiers)


def update_batch(system: Path) -> tuple[Path, int]:
    """Add newly discovered cases while preserving every existing human field."""

    path = system / "reviews" / "domain-review.json"
    version = (system / "VERSION").read_text(encoding="utf-8").strip()
    if path.is_file():
        batch: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    else:
        batch = {
            "system": system.name,
            "release": version,
            "status": "pending",
            "reviewer_id": None,
            "reviewed_at": None,
            "evidence": None,
            "case_reviews": [],
            "notes": "Independent domain review has not yet been performed.",
        }

    batch.setdefault("evidence", None)
    existing = {item["case_id"] for item in batch["case_reviews"]}
    additions = [case_id for case_id in _case_ids(system) if case_id not in existing]
    batch["case_reviews"].extend(
        {"case_id": case_id, "decision": "pending", "notes": ""} for case_id in additions
    )
    batch["case_reviews"].sort(key=lambda item: item["case_id"])
    if additions:
        batch.update(status="pending", reviewer_id=None, reviewed_at=None, evidence=None)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path, len(additions)


def main() -> int:
    total = 0
    for system in sorted((ROOT / "systems").iterdir()):
        if not system.is_dir() or system.name == "bazi" or not (system / "skills").is_dir():
            continue
        path, additions = update_batch(system)
        total += additions
        print(f"{path.relative_to(ROOT)}: added {additions}")
    print(f"Added {total} pending domain-review cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
