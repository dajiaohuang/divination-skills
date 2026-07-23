from __future__ import annotations

import json
from pathlib import Path

from systems.runes.engine import draw
from systems.runes.layers import build_layers

ROOT = Path(__file__).resolve().parent / "extension_cases"


def main() -> None:
    layer_dir = ROOT / "layers"
    layer_dir.mkdir(parents=True, exist_ok=True)
    for number in range(1, 51):
        raw_input = {
            "spread": "single" if number % 2 else "three-rune",
            "seed_hex": f"{number:064x}",
        }
        result = build_layers(draw(raw_input))
        case_id = f"CASE-RUNES-LAYERS-{number:03d}"
        case = {
            "case_id": case_id,
            "raw_input": raw_input,
            "expected_output": {
                "historical_evidence": result["historical_evidence"],
                "modern_reflection": result["modern_reflection"],
                "cross_layer_policy": result["cross_layer_policy"],
            },
        }
        (layer_dir / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    disputes = ROOT / "layer_disputes"
    disputes.mkdir(parents=True, exist_ok=True)
    claims = (
        "historical-source-proves-modern-keyword",
        "elder-futhark-equals-futhorc",
        "modern-reversal-is-historical",
        "unbroken-divination-continuity",
    )
    for number in range(1, 21):
        case_id = f"CASE-RUNES-LAYER-DISPUTE-{number:03d}"
        case = {
            "case_id": case_id,
            "unsupported_claim": claims[(number - 1) % len(claims)],
            "expected_handling": "reject_cross_layer_inference",
        }
        (disputes / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
