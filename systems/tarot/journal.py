"""Consent-gated local Tarot journal and descriptive statistics."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class JournalError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def append_entry(
    path: Path,
    draw: dict[str, Any],
    *,
    reflection: str,
    tags: list[str] | None = None,
    consent_to_store: bool,
    occurred_at: str | None = None,
) -> dict[str, Any]:
    if consent_to_store is not True:
        raise JournalError(
            "storage_consent_required",
            "Explicit consent_to_store=true is required.",
        )
    if draw.get("validation", {}).get("status") != "valid":
        raise JournalError("invalid_draw", "A valid Tarot draw is required.")
    if not isinstance(reflection, str) or not reflection.strip() or len(reflection) > 10_000:
        raise JournalError(
            "invalid_reflection",
            "reflection must contain 1 to 10000 characters.",
        )
    raw_tags = tags or []
    if any(not isinstance(tag, str) or not tag or len(tag) > 64 for tag in raw_tags):
        raise JournalError(
            "invalid_tags",
            "tags must be non-empty strings of at most 64 characters.",
        )
    clean_tags = sorted(set(raw_tags))
    instant = occurred_at or datetime.now(UTC).isoformat()
    try:
        parsed = datetime.fromisoformat(instant.replace("Z", "+00:00"))
    except ValueError as exc:
        raise JournalError("invalid_occurred_at", "occurred_at must be ISO 8601.") from exc
    if parsed.tzinfo is None:
        raise JournalError("invalid_occurred_at", "occurred_at must include a UTC offset.")
    cards = [
        {
            "card_id": card["card_id"],
            "position": card["position"],
            "orientation": card["orientation"],
        }
        for card in draw["computed_facts"]["cards"]
    ]
    basis = {
        "draw_id": draw["audit"]["draw_id"],
        "occurred_at": parsed.isoformat(),
        "reflection": reflection,
        "tags": clean_tags,
    }
    entry = {
        "schema_version": "0.2.0",
        "entry_id": "TAROT-JOURNAL-" + hashlib.sha256(_canonical(basis)).hexdigest()[:24],
        "occurred_at": parsed.isoformat(),
        "draw_id": draw["audit"]["draw_id"],
        "question_sha256": draw["normalized_input"]["question_sha256"],
        "spread": draw["computed_facts"]["spread"],
        "cards": cards,
        "reflection": reflection,
        "tags": clean_tags,
        "privacy": {
            "raw_question_stored": False,
            "consent_to_store": True,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
    return entry


def load_entries(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            raise JournalError("invalid_journal", f"Invalid JSON at line {number}.") from exc
        if entry.get("privacy", {}).get("raw_question_stored") is not False:
            raise JournalError("invalid_journal", f"Unsafe privacy metadata at line {number}.")
        entries.append(entry)
    return entries


def descriptive_statistics(entries: list[dict[str, Any]]) -> dict[str, Any]:
    spread_counts = Counter(entry["spread"] for entry in entries)
    card_counts = Counter(
        card["card_id"] for entry in entries for card in entry.get("cards", [])
    )
    orientation_counts = Counter(
        card["orientation"] for entry in entries for card in entry.get("cards", [])
    )
    tag_counts = Counter(tag for entry in entries for tag in entry.get("tags", []))
    return {
        "schema_version": "0.2.0",
        "entry_count": len(entries),
        "spread_counts": dict(sorted(spread_counts.items())),
        "card_counts": dict(sorted(card_counts.items())),
        "orientation_counts": dict(sorted(orientation_counts.items())),
        "tag_counts": dict(sorted(tag_counts.items())),
        "limitations": [
            "Counts describe journal contents; they do not measure predictive accuracy.",
            "No correlation, diagnosis, causal inference, or outcome scoring is performed.",
        ],
    }
