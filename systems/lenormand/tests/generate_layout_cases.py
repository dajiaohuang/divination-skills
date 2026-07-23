from __future__ import annotations

import json
from pathlib import Path

from systems.lenormand.engine import draw
from systems.lenormand.layouts import analyze_layout

ROOT = Path(__file__).resolve().parent / "extension_cases"


def compact(result: dict) -> dict:
    return {
        "spread": result["spread"],
        "pairs": result["pairs"],
        "nine_card": result["nine_card"],
        "grand_tableau": result["grand_tableau"],
    }


def main() -> None:
    layout_dir = ROOT / "layouts"
    layout_dir.mkdir(parents=True, exist_ok=True)
    spreads = ("three-card", "nine-card", "grand-tableau")
    for number in range(1, 51):
        spread = spreads[(number - 1) % len(spreads)]
        raw_input = {"spread": spread, "seed_hex": f"{number:064x}"}
        significator = (
            ("man" if number % 2 else "woman")
            if spread == "grand-tableau"
            else None
        )
        result = analyze_layout(draw(raw_input), significator=significator)
        case_id = f"CASE-LENORMAND-LAYOUT-{number:03d}"
        case = {
            "case_id": case_id,
            "raw_input": raw_input,
            "significator": significator,
            "expected_output": compact(result),
        }
        (layout_dir / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    disputes = ROOT / "layout_disputes"
    disputes.mkdir(parents=True, exist_ok=True)
    alternatives = ("eight-by-four-plus-four", "reversed-cards", "knighting", "diagonal-priority")
    for number in range(1, 21):
        case_id = f"CASE-LENORMAND-LAYOUT-DISPUTE-{number:03d}"
        case = {
            "case_id": case_id,
            "alternative": alternatives[(number - 1) % len(alternatives)],
            "expected_handling": "separate_lineage_not_silent_merge",
        }
        (disputes / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
