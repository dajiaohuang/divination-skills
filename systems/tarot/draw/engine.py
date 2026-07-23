"""Draw Tarot cards without replacement using an auditable hash stream."""

from __future__ import annotations

import hashlib
import json
import secrets
from functools import lru_cache
from pathlib import Path
from typing import Any

POSITIONS = {
    "single": ("focus",),
    "situation-challenge-guidance": ("situation", "challenge", "guidance"),
    "option-a-option-b-focus": ("option_a", "option_b", "decision_focus"),
    "elemental-five": ("center", "fire", "water", "air", "earth"),
    "relationship-six": (
        "self_position",
        "other_position",
        "connection",
        "communication",
        "boundary",
        "shared_focus",
    ),
    "horseshoe-seven": (
        "past_context",
        "present_context",
        "hidden_factor",
        "obstacle",
        "external_context",
        "suggested_focus",
        "possible_direction",
    ),
    "celtic-cross": (
        "present",
        "crossing",
        "foundation",
        "recent_past",
        "possible_direction",
        "near_context",
        "self_view",
        "environment",
        "hopes_concerns",
        "outcome_reflection",
    ),
}
ALGORITHM = "sha256-counter-rejection-v1"
DECK_PATH = Path(__file__).resolve().parents[1] / "data" / "rws-78.json"


class DrawError(ValueError):
    """Typed draw input error."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@lru_cache(maxsize=1)
def load_deck() -> dict[str, Any]:
    return json.loads(DECK_PATH.read_text(encoding="utf-8"))


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _digest(seed: bytes, domain: bytes, counter: int) -> bytes:
    return hashlib.sha256(
        b"tarot-draw-v1\x00" + domain + b"\x00" + seed + counter.to_bytes(8, "big")
    ).digest()


def _uniform_index(seed: bytes, domain: bytes, counter: int, size: int) -> tuple[int, int]:
    limit = 1 << 64
    accepted_limit = limit - (limit % size)
    while True:
        value = int.from_bytes(_digest(seed, domain, counter)[:8], "big")
        counter += 1
        if value < accepted_limit:
            return value % size, counter


def _normalize(payload: dict[str, Any]) -> tuple[str, str, bytes, bool, list[dict[str, str]]]:
    allowed = {"spread", "question", "seed_hex", "allow_reversals"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise DrawError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    spread = payload.get("spread")
    if spread not in POSITIONS:
        raise DrawError("invalid_spread", f"spread must be one of: {', '.join(POSITIONS)}")
    question = payload.get("question", "")
    if not isinstance(question, str) or len(question) > 2000:
        raise DrawError("invalid_question", "question must be a string of at most 2000 characters.")
    seed_hex = payload.get("seed_hex")
    warnings = []
    if seed_hex is None:
        seed = secrets.token_bytes(32)
        warnings.append(
            {
                "code": "seed_generated",
                "message": "A cryptographic seed was generated and disclosed for reproducibility.",
            }
        )
    elif not isinstance(seed_hex, str) or len(seed_hex) != 64:
        raise DrawError("invalid_seed", "seed_hex must contain exactly 64 hexadecimal characters.")
    else:
        try:
            seed = bytes.fromhex(seed_hex)
        except ValueError as exc:
            raise DrawError("invalid_seed", "seed_hex must be hexadecimal.") from exc
    allow_reversals = payload.get("allow_reversals", True)
    if not isinstance(allow_reversals, bool):
        raise DrawError("invalid_reversal_policy", "allow_reversals must be boolean.")
    return spread, question, seed, allow_reversals, warnings


def draw_cards(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a reproducible draw; interpretation is intentionally separate."""

    spread, question, seed, allow_reversals, warnings = _normalize(payload)
    deck = load_deck()
    deck_hash = hashlib.sha256(canonical_json(deck)).hexdigest()
    question_hash = hashlib.sha256(question.encode("utf-8")).hexdigest()
    remaining = list(range(len(deck["cards"])))
    selected = []
    card_counter = 0
    orientation_counter = 0
    for number, position in enumerate(POSITIONS[spread], start=1):
        selection_index, card_counter = _uniform_index(seed, b"card", card_counter, len(remaining))
        card_index = remaining.pop(selection_index)
        card = deck["cards"][card_index]
        if allow_reversals:
            orientation_index, orientation_counter = _uniform_index(
                seed, b"orientation", orientation_counter, 2
            )
            orientation = "reversed" if orientation_index else "upright"
        else:
            orientation = "upright"
        selected.append(
            {
                "fact_id": f"tarot.draw.card.{number:03d}",
                "position": position,
                "card_id": card["card_id"],
                "card_index": card_index,
                "name": card["name"],
                "orientation": orientation,
                "source_ids": ["SRC-TAROT-DECK-SPEC-001"],
            }
        )

    normalized = {
        "spread": spread,
        "question_sha256": question_hash,
        "allow_reversals": allow_reversals,
    }
    seed_hex = seed.hex()
    audit_basis = {"normalized_input": normalized, "seed_hex": seed_hex, "deck_sha256": deck_hash}
    return {
        "schema_version": "0.1.0",
        "engine": {
            "name": "divination-skills-tarot-draw",
            "version": "0.1.0",
            "source_ids": ["SRC-TAROT-DECK-SPEC-001"],
        },
        "normalized_input": normalized,
        "audit": {
            "algorithm": ALGORITHM,
            "seed_hex": seed_hex,
            "seed_commitment": hashlib.sha256(b"tarot-seed-v1\x00" + seed).hexdigest(),
            "deck_sha256": deck_hash,
            "draw_id": hashlib.sha256(canonical_json(audit_basis)).hexdigest(),
        },
        "computed_facts": {"spread": spread, "cards": selected},
        "derived_findings": [],
        "narrative": None,
        "validation": {"status": "valid", "warnings": warnings},
    }
