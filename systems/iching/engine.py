"""Deterministic three-coin casting and structural reporting."""

from __future__ import annotations

import hashlib
import json
import secrets
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any

SOURCE_ID = "SRC-ICHING-PROJECT-SPEC-001"
TRIGRAM_BY_BITS = {
    (1, 1, 1): ("qian", "乾", "heaven"),
    (1, 1, 0): ("dui", "兑", "lake"),
    (1, 0, 1): ("li", "离", "fire"),
    (1, 0, 0): ("zhen", "震", "thunder"),
    (0, 1, 1): ("xun", "巽", "wind"),
    (0, 1, 0): ("kan", "坎", "water"),
    (0, 0, 1): ("gen", "艮", "mountain"),
    (0, 0, 0): ("kun", "坤", "earth"),
}
PAIR_TO_NUMBER = {
    ("qian", "qian"): 1,
    ("kun", "kun"): 2,
    ("kan", "zhen"): 3,
    ("gen", "kan"): 4,
    ("kan", "qian"): 5,
    ("qian", "kan"): 6,
    ("kun", "kan"): 7,
    ("kan", "kun"): 8,
    ("xun", "qian"): 9,
    ("qian", "dui"): 10,
    ("kun", "qian"): 11,
    ("qian", "kun"): 12,
    ("qian", "li"): 13,
    ("li", "qian"): 14,
    ("kun", "gen"): 15,
    ("zhen", "kun"): 16,
    ("dui", "zhen"): 17,
    ("gen", "xun"): 18,
    ("kun", "dui"): 19,
    ("xun", "kun"): 20,
    ("li", "zhen"): 21,
    ("gen", "li"): 22,
    ("gen", "kun"): 23,
    ("kun", "zhen"): 24,
    ("qian", "zhen"): 25,
    ("gen", "qian"): 26,
    ("gen", "zhen"): 27,
    ("dui", "xun"): 28,
    ("kan", "kan"): 29,
    ("li", "li"): 30,
    ("dui", "gen"): 31,
    ("zhen", "xun"): 32,
    ("qian", "gen"): 33,
    ("zhen", "qian"): 34,
    ("li", "kun"): 35,
    ("kun", "li"): 36,
    ("xun", "li"): 37,
    ("li", "dui"): 38,
    ("kan", "gen"): 39,
    ("zhen", "kan"): 40,
    ("gen", "dui"): 41,
    ("xun", "zhen"): 42,
    ("dui", "qian"): 43,
    ("qian", "xun"): 44,
    ("dui", "kun"): 45,
    ("kun", "xun"): 46,
    ("dui", "kan"): 47,
    ("kan", "xun"): 48,
    ("dui", "li"): 49,
    ("li", "xun"): 50,
    ("zhen", "zhen"): 51,
    ("gen", "gen"): 52,
    ("xun", "gen"): 53,
    ("zhen", "dui"): 54,
    ("zhen", "li"): 55,
    ("li", "gen"): 56,
    ("xun", "xun"): 57,
    ("dui", "dui"): 58,
    ("xun", "kan"): 59,
    ("kan", "dui"): 60,
    ("xun", "dui"): 61,
    ("zhen", "gen"): 62,
    ("kan", "li"): 63,
    ("li", "kan"): 64,
}


class CastError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


@lru_cache(maxsize=1)
def hexagrams() -> dict[int, dict[str, Any]]:
    path = Path(__file__).resolve().parent / "data" / "hexagrams.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    return {row["number"]: row for row in rows}


def identify(bits: list[int]) -> dict[str, Any]:
    if len(bits) != 6 or any(bit not in (0, 1) for bit in bits):
        raise CastError("invalid_lines", "Exactly six binary lines are required.")
    lower = TRIGRAM_BY_BITS[tuple(bits[:3])]
    upper = TRIGRAM_BY_BITS[tuple(bits[3:])]
    number = PAIR_TO_NUMBER[(upper[0], lower[0])]
    row = hexagrams()[number]
    return {
        **row,
        "lower_trigram": {"id": lower[0], "hanzi": lower[1], "image": lower[2]},
        "upper_trigram": {"id": upper[0], "hanzi": upper[1], "image": upper[2]},
        "lines_bottom_to_top": bits,
        "source_ids": [SOURCE_ID],
    }


def cast(payload: dict[str, Any]) -> dict[str, Any]:
    unknown = sorted(set(payload) - {"question", "seed_hex"})
    if unknown:
        raise CastError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    question = payload.get("question", "")
    if not isinstance(question, str) or len(question) > 2000:
        raise CastError("invalid_question", "question must be at most 2000 characters.")
    raw_seed = payload.get("seed_hex")
    warnings = []
    if raw_seed is None:
        seed = secrets.token_bytes(32)
        warnings.append({"code": "seed_generated", "message": "A replay seed was generated."})
    elif not isinstance(raw_seed, str) or len(raw_seed) != 64:
        raise CastError("invalid_seed", "seed_hex must be 64 hexadecimal characters.")
    else:
        try:
            seed = bytes.fromhex(raw_seed)
        except ValueError as exc:
            raise CastError("invalid_seed", "seed_hex must be hexadecimal.") from exc

    lines = []
    primary_bits = []
    changed_bits = []
    for line_number in range(1, 7):
        coins = []
        for coin_number in range(1, 4):
            digest = hashlib.sha256(
                b"divination-iching-three-coin-v1\x00" + seed + bytes((line_number, coin_number))
            ).digest()
            coins.append(2 + (digest[0] & 1))
        value = sum(coins)
        polarity = 1 if value in (7, 9) else 0
        moving = value in (6, 9)
        changed = 1 - polarity if moving else polarity
        primary_bits.append(polarity)
        changed_bits.append(changed)
        lines.append(
            {
                "fact_id": f"iching.cast.line.{line_number:03d}",
                "position_from_bottom": line_number,
                "coins": coins,
                "value": value,
                "polarity": "yang" if polarity else "yin",
                "moving": moving,
                "changed_polarity": "yang" if changed else "yin",
                "source_ids": [SOURCE_ID],
            }
        )
    primary = identify(primary_bits)
    changed = identify(changed_bits)
    normalized = {
        "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
        "line_order": "bottom-to-top",
        "lineage": "three-coin-king-wen-structural-v0.1",
    }
    audit_basis = {"normalized_input": normalized, "seed_hex": seed.hex(), "lines": lines}
    return {
        "schema_version": "0.1.0",
        "engine": {
            "name": "divination-skills-iching-cast",
            "version": "0.1.0",
            "source_ids": [SOURCE_ID],
        },
        "normalized_input": normalized,
        "audit": {
            "algorithm": "sha256-three-coin-v1",
            "seed_hex": seed.hex(),
            "seed_commitment": hashlib.sha256(b"iching-seed-v1\x00" + seed).hexdigest(),
            "cast_id": hashlib.sha256(_canonical(audit_basis)).hexdigest(),
        },
        "computed_facts": {
            "lines": lines,
            "moving_line_positions": [
                line["position_from_bottom"] for line in lines if line["moving"]
            ],
            "primary_hexagram": primary,
            "changed_hexagram": changed,
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {"status": "valid", "warnings": warnings},
    }


def explain(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid I Ching cast is required.")
    report = deepcopy(result)
    original = deepcopy(result["computed_facts"])
    facts = result["computed_facts"]
    primary = facts["primary_hexagram"]
    changed = facts["changed_hexagram"]
    moving_ids = [line["fact_id"] for line in facts["lines"] if line["moving"]]
    report["derived_findings"] = [
        {
            "finding_id": "iching.finding.primary.001",
            "fact_ids": [line["fact_id"] for line in facts["lines"]],
            "rule_ids": ["ICHING-HEXAGRAM-MAP-001"],
            "confidence": "high",
            "value": primary["number"],
            "source_ids": [SOURCE_ID],
        },
        {
            "finding_id": "iching.finding.change.001",
            "fact_ids": moving_ids or [line["fact_id"] for line in facts["lines"]],
            "rule_ids": ["ICHING-MOVING-LINES-001"],
            "confidence": "high",
            "value": changed["number"],
            "source_ids": [SOURCE_ID],
        },
    ]
    report["narrative"] = {
        "primary": {
            "fact_ids": [line["fact_id"] for line in facts["lines"]],
            "rule_ids": ["ICHING-STRUCTURAL-REFLECTION-001"],
            "statement": (
                f"Hexagram {primary['number']} {primary['english']} frames the present structure. "
                "Observe the named conditions before assuming an outcome."
            ),
        },
        "change": {
            "fact_ids": moving_ids or [line["fact_id"] for line in facts["lines"]],
            "rule_ids": ["ICHING-MOVING-LINES-001", "ICHING-STRUCTURAL-REFLECTION-001"],
            "statement": (
                f"Moving lines {facts['moving_line_positions']} produce hexagram "
                f"{changed['number']} {changed['english']}. This is a structural comparison, "
                "not a guaranteed future."
            ),
        },
        "limitations": [
            "No classical judgment or line text is reproduced.",
            "The cast is a reflective structure, not empirical evidence or professional advice.",
        ],
    }
    if report["computed_facts"] != original:
        raise AssertionError("I Ching explanation must not mutate cast facts.")
    return report
