from __future__ import annotations

import json
from pathlib import Path

from systems.iching.engine import cast
from systems.iching.text_layer import build_classical_layer

ROOT = Path(__file__).resolve().parent / "extension_cases"


def main() -> None:
    standard = ROOT / "text_layer"
    standard.mkdir(parents=True, exist_ok=True)
    policies = ("all-moving-lines-v0.2", "zhu-xi-count-routing-v0.2")
    for number in range(1, 51):
        raw_input = {"seed_hex": f"{number:064x}"}
        policy_id = policies[number % 2]
        result = build_classical_layer(cast(raw_input), policy_id=policy_id)
        case_id = f"CASE-ICHING-TEXT-LAYER-{number:03d}"
        case = {
            "case_id": case_id,
            "raw_input": raw_input,
            "policy_id": policy_id,
            "expected_output": {
                "selection": result["selection"],
                "editions": result["editions"],
                "version_comparison": result["version_comparison"],
            },
        }
        (standard / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    disputes = ROOT / "policy_disputes"
    disputes.mkdir(parents=True, exist_ok=True)
    for number in range(1, 21):
        case_id = f"CASE-ICHING-POLICY-DISPUTE-{number:03d}"
        case = {
            "case_id": case_id,
            "moving_line_count": (number - 1) % 7,
            "left_policy": "all-moving-lines-v0.2",
            "right_policy": "zhu-xi-count-routing-v0.2",
            "expected_handling": "return_separate_outputs_without_merging",
        }
        (disputes / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
