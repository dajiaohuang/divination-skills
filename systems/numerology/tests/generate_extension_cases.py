from __future__ import annotations

import json
from pathlib import Path

from systems.numerology.calculator import calculate_profile

ROOT = Path(__file__).resolve().parent / "extension_cases"


def main() -> None:
    cases = ROOT / "chaldean"
    cases.mkdir(parents=True, exist_ok=True)
    latin_names = ("Ada Lovelace", "Grace Hopper", "Alan Turing", "Test Person", "Example Name")
    non_latin = (
        ("张伟", "Zhang Wei"),
        ("王芳", "Wang Fang"),
        ("山田太郎", "Yamada Taro"),
        ("김민수", "Kim Minsu"),
        ("Алексей", "Aleksei"),
    )
    for number in range(1, 51):
        if number % 2:
            payload = {
                "name": latin_names[(number // 2) % len(latin_names)],
                "birth_date": (
                    f"{1980 + number % 30:04d}-{number % 12 + 1:02d}-"
                    f"{number % 27 + 1:02d}"
                ),
                "mapping": "chaldean",
            }
        else:
            original, transliteration = non_latin[(number // 2) % len(non_latin)]
            payload = {
                "name": original,
                "transliteration": transliteration,
                "birth_date": (
                    f"{1980 + number % 30:04d}-{number % 12 + 1:02d}-"
                    f"{number % 27 + 1:02d}"
                ),
                "mapping": "chaldean",
            }
        result = calculate_profile(payload)
        case_id = f"CASE-NUMEROLOGY-CHALDEAN-{number:03d}"
        case = {
            "case_id": case_id,
            "raw_input": payload,
            "expected_output": {
                "normalized_input": result["normalized_input"],
                "computed_facts": result["computed_facts"],
            },
        }
        (cases / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    disputes = ROOT / "mapping_disputes"
    disputes.mkdir(parents=True, exist_ok=True)
    policies = (
        "preserve-master-numbers-in-chaldean",
        "infer-non-latin-transliteration",
        "mix-letter-values",
        "treat-y-as-vowel",
    )
    for number in range(1, 21):
        case_id = f"CASE-NUMEROLOGY-MAPPING-DISPUTE-{number:03d}"
        case = {
            "case_id": case_id,
            "alternative_policy": policies[(number - 1) % len(policies)],
            "expected_handling": "separate_lineage_or_fail_closed",
        }
        (disputes / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
