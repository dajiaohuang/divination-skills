"""Reusable unbiased draw protocol for text-only symbolic decks."""

from __future__ import annotations

import hashlib
import json
import secrets
from copy import deepcopy
from typing import Any


class AuditableDrawError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _uniform_index(seed: bytes, domain: bytes, counter: int, size: int) -> tuple[int, int]:
    limit = 1 << 64
    accepted = limit - limit % size
    while True:
        digest = hashlib.sha256(
            b"divination-symbol-draw-v1\x00" + domain + b"\x00" + seed + counter.to_bytes(8, "big")
        ).digest()
        counter += 1
        value = int.from_bytes(digest[:8], "big")
        if value < accepted:
            return value % size, counter


def draw_symbols(
    payload: dict[str, Any],
    *,
    system: str,
    lineage: str,
    items: list[dict[str, Any]],
    spreads: dict[str, tuple[str, ...]],
    source_id: str,
    allow_reversals: bool = False,
) -> dict[str, Any]:
    """Draw unique symbols and disclose everything required for replay."""

    allowed = {"spread", "question", "seed_hex", "allow_reversals"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise AuditableDrawError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    spread = payload.get("spread")
    if spread not in spreads:
        raise AuditableDrawError("invalid_spread", f"spread must be one of: {', '.join(spreads)}")
    question = payload.get("question", "")
    if not isinstance(question, str) or len(question) > 2000:
        raise AuditableDrawError("invalid_question", "question must be at most 2000 characters.")
    requested_reversals = payload.get("allow_reversals", allow_reversals)
    if not isinstance(requested_reversals, bool):
        raise AuditableDrawError("invalid_reversal_policy", "allow_reversals must be boolean.")
    if requested_reversals and not allow_reversals:
        raise AuditableDrawError(
            "reversals_unsupported", f"{system} v0.1 does not use reversed orientation."
        )
    raw_seed = payload.get("seed_hex")
    warnings = []
    if raw_seed is None:
        seed = secrets.token_bytes(32)
        warnings.append({"code": "seed_generated", "message": "A replay seed was generated."})
    elif not isinstance(raw_seed, str) or len(raw_seed) != 64:
        raise AuditableDrawError("invalid_seed", "seed_hex must be 64 hexadecimal characters.")
    else:
        try:
            seed = bytes.fromhex(raw_seed)
        except ValueError as exc:
            raise AuditableDrawError("invalid_seed", "seed_hex must be hexadecimal.") from exc

    deck_hash = hashlib.sha256(canonical_json(items)).hexdigest()
    remaining = list(range(len(items)))
    selected = []
    counter = 0
    orientation_counter = 0
    for number, position in enumerate(spreads[spread], start=1):
        selected_index, counter = _uniform_index(seed, b"item", counter, len(remaining))
        item_index = remaining.pop(selected_index)
        item = items[item_index]
        orientation = "upright"
        if requested_reversals:
            reversed_index, orientation_counter = _uniform_index(
                seed, b"orientation", orientation_counter, 2
            )
            orientation = "reversed" if reversed_index else "upright"
        selected.append(
            {
                "fact_id": f"{system}.draw.symbol.{number:03d}",
                "position": position,
                "symbol_id": item["symbol_id"],
                "symbol_index": item_index,
                "name": item["name"],
                "orientation": orientation,
                "source_ids": [source_id],
            }
        )
    normalized = {
        "spread": spread,
        "question_sha256": hashlib.sha256(question.encode("utf-8")).hexdigest(),
        "allow_reversals": requested_reversals,
        "lineage": lineage,
    }
    seed_hex = seed.hex()
    audit_basis = {"normalized": normalized, "seed_hex": seed_hex, "deck_sha256": deck_hash}
    return {
        "schema_version": "0.1.0",
        "engine": {
            "name": f"divination-skills-{system}-draw",
            "version": "0.1.0",
            "source_ids": [source_id],
        },
        "normalized_input": normalized,
        "audit": {
            "algorithm": "sha256-counter-rejection-v1",
            "seed_hex": seed_hex,
            "seed_commitment": hashlib.sha256(b"symbol-seed-v1\x00" + seed).hexdigest(),
            "deck_sha256": deck_hash,
            "draw_id": hashlib.sha256(canonical_json(audit_basis)).hexdigest(),
        },
        "computed_facts": {"spread": spread, "symbols": selected},
        "derived_findings": [],
        "narrative": None,
        "validation": {"status": "valid", "warnings": warnings},
    }


def build_symbol_report(
    draw: dict[str, Any],
    *,
    items: list[dict[str, Any]],
    system: str,
    source_id: str,
    orientation_rule: str,
    position_rule: str,
    sequence_rule: str,
) -> dict[str, Any]:
    """Build a generic reflective report while preserving draw facts."""

    if draw.get("validation", {}).get("status") != "valid":
        raise ValueError(f"A valid {system} draw is required.")
    report = deepcopy(draw)
    original = deepcopy(draw["computed_facts"])
    item_by_id = {item["symbol_id"]: item for item in items}
    explanations = []
    findings = []
    for number, fact in enumerate(draw["computed_facts"]["symbols"], start=1):
        item = item_by_id[fact["symbol_id"]]
        keywords = item[fact["orientation"]]
        explanation = {
            "fact_ids": [fact["fact_id"]],
            "rule_ids": [orientation_rule, position_rule],
            "statement": (
                f"{fact['position']}: {fact['name']} highlights {', '.join(keywords)}. "
                "Use this as a reflective prompt, not a factual or predictive claim."
            ),
        }
        explanations.append(explanation)
        findings.append(
            {
                "finding_id": f"{system}.finding.{number:03d}",
                "fact_ids": explanation["fact_ids"],
                "rule_ids": explanation["rule_ids"],
                "confidence": "low",
                "keywords": keywords,
                "source_ids": [source_id],
            }
        )
    sequence = {
        "fact_ids": [fact["fact_id"] for fact in draw["computed_facts"]["symbols"]],
        "rule_ids": [sequence_rule],
        "statement": (
            "Read the symbols in position order as a bounded comparison; "
            "the sequence does not establish hidden facts or a fixed future."
        ),
    }
    report["derived_findings"] = findings
    report["narrative"] = {
        "symbols": explanations,
        "sequence": sequence,
        "limitations": ["Symbolic draws are reflective prompts, not empirical evidence."],
    }
    if report["computed_facts"] != original:
        raise AssertionError("Symbol interpretation must not mutate draw facts.")
    return report
