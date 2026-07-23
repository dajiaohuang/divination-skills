"""Deterministic project Pythagorean numerology calculations."""

from __future__ import annotations

import unicodedata
from datetime import date
from typing import Any

MASTERS = {11, 22, 33}
VOWELS = set("AEIOU")
CHALDEAN_VALUES = {
    **dict.fromkeys("AIJQY", 1),
    **dict.fromkeys("BKR", 2),
    **dict.fromkeys("CGLS", 3),
    **dict.fromkeys("DMT", 4),
    **dict.fromkeys("EHNX", 5),
    **dict.fromkeys("UVW", 6),
    **dict.fromkeys("OZ", 7),
    **dict.fromkeys("FP", 8),
}
MAPPINGS = {"pythagorean", "chaldean"}
PROJECT_SOURCE = "SRC-NUMEROLOGY-PROJECT-SPEC-001"
CHEIRO_SOURCE = "SRC-NUMEROLOGY-CHEIRO-001"
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


def reduce_number(value: int, *, preserve_masters: bool = True) -> tuple[int, list[int]]:
    steps = [value]
    while value > 9 and not (preserve_masters and value in MASTERS):
        value = sum(int(digit) for digit in str(value))
        steps.append(value)
    return value, steps


def _normalize_name_with_policy(
    name: str,
    transliteration: str | None,
) -> tuple[str, str]:
    if not isinstance(name, str) or not name.strip():
        raise NumerologyError("invalid_name", "name must be a non-empty string.")
    decomposed = unicodedata.normalize("NFKD", name)
    has_non_latin_letters = any(
        char.isalpha() and not ("A" <= char.upper() <= "Z")
        for char in decomposed
        if not unicodedata.combining(char)
    )
    if has_non_latin_letters:
        if transliteration is None:
            raise NumerologyError(
                "transliteration_required",
                "A user-supplied Latin transliteration is required for non-Latin names.",
            )
        if not isinstance(transliteration, str) or not transliteration.strip():
            raise NumerologyError(
                "invalid_transliteration",
                "transliteration must be a non-empty Latin string.",
            )
        candidate = unicodedata.normalize("NFKD", transliteration)
        if any(
            char.isalpha() and not ("A" <= char.upper() <= "Z")
            for char in candidate
            if not unicodedata.combining(char)
        ):
            raise NumerologyError(
                "invalid_transliteration",
                "transliteration must normalize entirely to Latin A-Z letters.",
            )
        policy = "user_supplied_latin_transliteration-v0.2"
    else:
        if transliteration is not None:
            raise NumerologyError(
                "unexpected_transliteration",
                (
                    "transliteration is accepted only when the original name contains "
                    "non-Latin letters."
                ),
            )
        candidate = decomposed
        policy = "latin_nfkd-v0.1"
    letters = "".join(char for char in candidate.upper() if "A" <= char <= "Z")
    if not letters:
        raise NumerologyError(
            "unsupported_name_script",
            "The selected name input does not normalize to Latin A-Z.",
        )
    return letters, policy


def normalize_name(name: str, transliteration: str | None = None) -> str:
    return _normalize_name_with_policy(name, transliteration)[0]


def letter_value(letter: str, mapping: str = "pythagorean") -> int:
    if mapping == "pythagorean":
        return (ord(letter) - ord("A")) % 9 + 1
    if mapping == "chaldean":
        return CHALDEAN_VALUES[letter]
    raise NumerologyError("invalid_mapping", "mapping must be pythagorean or chaldean.")


def _fact(
    fact_id: str,
    raw_total: int,
    *,
    preserve_masters: bool,
    source_ids: list[str],
) -> dict[str, Any]:
    value, steps = reduce_number(raw_total, preserve_masters=preserve_masters)
    return {
        "fact_id": fact_id,
        "raw_total": raw_total,
        "reduction_steps": steps,
        "value": value,
        "master_number": preserve_masters and value in MASTERS,
        "theme": THEMES[value],
        "source_ids": source_ids,
    }


def calculate_profile(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {"name", "birth_date", "mapping", "transliteration"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise NumerologyError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    if "name" not in payload or "birth_date" not in payload:
        raise NumerologyError("missing_fields", "name and birth_date are required.")
    mapping = payload.get("mapping", "pythagorean")
    if mapping not in MAPPINGS:
        raise NumerologyError(
            "invalid_mapping",
            "mapping must be pythagorean or chaldean.",
        )
    letters, transliteration_policy = _normalize_name_with_policy(
        payload["name"],
        payload.get("transliteration"),
    )
    try:
        born = date.fromisoformat(payload["birth_date"])
    except (TypeError, ValueError) as exc:
        raise NumerologyError("invalid_birth_date", "birth_date must be YYYY-MM-DD.") from exc
    if not 1900 <= born.year <= 2100:
        raise NumerologyError("date_out_of_range", "Supported years are 1900 through 2100.")

    all_values = [letter_value(letter, mapping) for letter in letters]
    vowel_values = [
        letter_value(letter, mapping) for letter in letters if letter in VOWELS
    ]
    consonant_values = [
        letter_value(letter, mapping) for letter in letters if letter not in VOWELS
    ]
    if not vowel_values or not consonant_values:
        raise NumerologyError(
            "insufficient_name_parts", "The normalized name must contain a vowel and a consonant."
        )
    date_total = sum(int(digit) for digit in born.isoformat() if digit.isdigit())
    preserve_masters = mapping == "pythagorean"
    mapping_source_ids = (
        [PROJECT_SOURCE] if mapping == "pythagorean" else [PROJECT_SOURCE, CHEIRO_SOURCE]
    )
    life_path = _fact(
        "numerology.life_path",
        date_total,
        preserve_masters=preserve_masters,
        source_ids=[PROJECT_SOURCE],
    )
    expression = _fact(
        "numerology.expression",
        sum(all_values),
        preserve_masters=preserve_masters,
        source_ids=mapping_source_ids,
    )
    soul = _fact(
        "numerology.soul_urge",
        sum(vowel_values),
        preserve_masters=preserve_masters,
        source_ids=mapping_source_ids,
    )
    personality = _fact(
        "numerology.personality",
        sum(consonant_values),
        preserve_masters=preserve_masters,
        source_ids=mapping_source_ids,
    )
    birthday = _fact(
        "numerology.birthday",
        born.day,
        preserve_masters=preserve_masters,
        source_ids=[PROJECT_SOURCE],
    )
    maturity = _fact(
        "numerology.maturity",
        life_path["value"] + expression["value"],
        preserve_masters=preserve_masters,
        source_ids=mapping_source_ids,
    )
    return {
        "schema_version": "0.3.0",
        "engine": {
            "name": "divination-skills-numerology",
            "version": "0.3.0",
            "source_ids": mapping_source_ids,
        },
        "raw_input": dict(payload),
        "normalized_input": {
            "name_letters": letters,
            "birth_date": born.isoformat(),
            "mapping": (
                "pythagorean-a1-i9-repeat"
                if mapping == "pythagorean"
                else "chaldean-1-through-8-project"
            ),
            "mapping_lineage": (
                "pythagorean-project-v0.3"
                if mapping == "pythagorean"
                else "chaldean-name-cheiro-v0.3"
            ),
            "transliteration_policy": transliteration_policy,
            "masters": sorted(MASTERS) if preserve_masters else [],
        },
        "computed_facts": {
            "name_trace": {
                "fact_id": "numerology.name_trace",
                "letters": [
                    {
                        "position": index,
                        "letter": letter,
                        "category": "vowel" if letter in VOWELS else "consonant",
                        "value": value,
                    }
                    for index, (letter, value) in enumerate(
                        zip(letters, all_values, strict=True), start=1
                    )
                ],
                "raw_total": sum(all_values),
                "source_ids": mapping_source_ids,
            },
            "date_trace": {
                "fact_id": "numerology.date_trace",
                "digits": [int(digit) for digit in born.isoformat() if digit.isdigit()],
                "raw_total": date_total,
                "source_ids": [PROJECT_SOURCE],
            },
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
