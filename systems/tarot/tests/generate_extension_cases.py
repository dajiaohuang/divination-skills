from __future__ import annotations

import json
from pathlib import Path

from systems.tarot.combinations import analyze_combinations
from systems.tarot.draw.engine import draw_cards

ROOT = Path(__file__).resolve().parent / "extension_cases"


def compact(draw: dict, combinations: dict) -> dict:
    return {
        "computed_facts": draw["computed_facts"],
        "pairs": combinations["pairs"],
        "distribution": combinations["distribution"],
    }


def main() -> None:
    cases = ROOT / "spreads"
    cases.mkdir(parents=True, exist_ok=True)
    spreads = ("elemental-five", "relationship-six", "horseshoe-seven", "celtic-cross")
    for number in range(1, 51):
        raw_input = {
            "spread": spreads[(number - 1) % len(spreads)],
            "seed_hex": f"{number:064x}",
            "allow_reversals": number % 2 == 0,
        }
        draw = draw_cards(raw_input)
        combination = analyze_combinations(draw)
        case_id = f"CASE-TAROT-EXTENSION-{number:03d}"
        case = {
            "case_id": case_id,
            "raw_input": raw_input,
            "expected_output": compact(draw, combination),
        }
        (cases / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    disputes = ROOT / "spread_disputes"
    disputes.mkdir(parents=True, exist_ok=True)
    alternatives = (
        "alternate-celtic-cross-order",
        "different-element-order",
        "reversal-disabled",
        "freeform-spread",
    )
    for number in range(1, 21):
        case_id = f"CASE-TAROT-SPREAD-DISPUTE-{number:03d}"
        case = {
            "case_id": case_id,
            "alternative": alternatives[(number - 1) % len(alternatives)],
            "expected_handling": "require_registered_spread_or_separate_lineage",
        }
        (disputes / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
