"""Shared helpers for deterministic layered evaluations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def corpus_sha256(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\x00")
        digest.update(path.read_bytes())
        digest.update(b"\x00")
    return digest.hexdigest()


def ratio_metric(
    numerator: int,
    denominator: int,
    *,
    threshold: float,
    comparison: str,
    evidence: list[str],
) -> dict[str, Any]:
    if denominator <= 0:
        raise ValueError("Evaluation metrics require a positive denominator.")
    if not 0 <= numerator <= denominator:
        raise ValueError("Metric numerator must be between zero and denominator.")
    value = numerator / denominator
    if comparison == "minimum":
        passed = value >= threshold
    elif comparison == "maximum":
        passed = value <= threshold
    else:
        raise ValueError("comparison must be 'minimum' or 'maximum'.")
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": value,
        "threshold": threshold,
        "comparison": comparison,
        "passed": passed,
        "evidence": evidence,
    }


def collect_fact_ids(value: Any) -> set[str]:
    result: set[str] = set()
    if isinstance(value, dict):
        fact_id = value.get("fact_id")
        if isinstance(fact_id, str):
            result.add(fact_id)
        for child in value.values():
            result.update(collect_fact_ids(child))
    elif isinstance(value, list):
        for child in value:
            result.update(collect_fact_ids(child))
    return result


def collect_narrative_claims(narrative: Any) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    if isinstance(narrative, dict):
        if "statement" in narrative:
            claims.append(narrative)
        else:
            for key, child in narrative.items():
                if key != "limitations":
                    claims.extend(collect_narrative_claims(child))
    elif isinstance(narrative, list):
        for child in narrative:
            claims.extend(collect_narrative_claims(child))
    return claims
