"""Deterministic project Pythagorean numerology calculations."""

from __future__ import annotations

import unicodedata
from datetime import date
from typing import Any

MASTERS = {11, 22, 33}
VOWELS = set("AEIOU")
THEMES = {
    1: "initiative",
    2: "cooperation",
    3: "expression",
    4: "structure",
    5: "change",
    6: "care and responsibility",
    7: "inquiry",
    8: "stewardship of power and resources",
    9: "completion and broad concern",
    11: "heightened inspiration",
    22: "large-scale practical building",
    33: "service through teaching and care",
}


class NumerologyError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def reduce_number(value: int) -> tuple[int, list[int]]:
    steps = [value]
    while value > 9 and value not in MASTERS:
        value = sum(int(digit) for digit in str(value))
        steps.append(value)
    return value, steps


def normalize_name(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise NumerologyError("invalid_name", "name must be a non-empty string.")
    decomposed = unicodedata.normalize("NFKD", name)
    letters = "".join(char for char in decomposed.upper() if "A" <= char <= "Z")
    if not letters:
        raise NumerologyError(
            "unsupported_name_script",
            "v0.1 requires a name that normalizes to Latin A-Z; transliteration is not inferred.",
        )
    return letters


def letter_value(letter: str) -> int:
    return (ord(letter) - ord("A")) % 9 + 1


def _fact(fact_id: str, raw_total: int) -> dict[str, Any]:
    value, steps = reduce_number(raw_total)
    return {
        "fact_id": fact_id,
        "raw_total": raw_total,
        "reduction_steps": steps,
        "value": value,
        "master_number": value in MASTERS,
        "theme": THEMES[value],
        "source_ids": ["SRC-NUMEROLOGY-PROJECT-SPEC-001"],
    }


def calculate_profile(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {"name", "birth_date"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise NumerologyError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    if "name" not in payload or "birth_date" not in payload:
        raise NumerologyError("missing_fields", "name and birth_date are required.")
    letters = normalize_name(payload["name"])
    try:
        born = date.fromisoformat(payload["birth_date"])
    except (TypeError, ValueError) as exc:
        raise NumerologyError("invalid_birth_date", "birth_date must be YYYY-MM-DD.") from exc
    if not 1900 <= born.year <= 2100:
        raise NumerologyError("date_out_of_range", "Supported years are 1900 through 2100.")

    all_values = [letter_value(letter) for letter in letters]
    vowel_values = [letter_value(letter) for letter in letters if letter in VOWELS]
    consonant_values = [letter_value(letter) for letter in letters if letter not in VOWELS]
    if not vowel_values or not consonant_values:
        raise NumerologyError(
            "insufficient_name_parts", "The normalized name must contain a vowel and a consonant."
        )
    date_total = sum(int(digit) for digit in born.isoformat() if digit.isdigit())
    life_path = _fact("numerology.life_path", date_total)
    expression = _fact("numerology.expression", sum(all_values))
    soul = _fact("numerology.soul_urge", sum(vowel_values))
    personality = _fact("numerology.personality", sum(consonant_values))
    birthday = _fact("numerology.birthday", born.day)
    maturity = _fact("numerology.maturity", life_path["value"] + expression["value"])
    return {
        "schema_version": "0.1.0",
        "engine": {
            "name": "divination-skills-numerology",
            "version": "0.1.0",
            "source_ids": ["SRC-NUMEROLOGY-PROJECT-SPEC-001"],
        },
        "raw_input": dict(payload),
        "normalized_input": {
            "name_letters": letters,
            "birth_date": born.isoformat(),
            "mapping": "pythagorean-a1-i9-repeat",
            "masters": sorted(MASTERS),
        },
        "computed_facts": {
            "life_path": life_path,
            "birthday": birthday,
            "expression": expression,
            "soul_urge": soul,
            "personality": personality,
            "maturity": maturity,
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {"status": "valid", "warnings": []},
    }
