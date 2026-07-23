from __future__ import annotations

import json
from pathlib import Path

from systems.qimen.full_chart import calculate_full

ROOT = Path(__file__).resolve().parent / "extension_cases"


def summary(result: dict) -> dict:
    return {
        "rotation": result["rotation"],
        "void_branches": result["void_branches"],
        "palaces": result["palaces"],
    }


def write_case(folder: str, case_id: str, raw_input: dict) -> None:
    target = ROOT / folder
    target.mkdir(parents=True, exist_ok=True)
    result = calculate_full(raw_input)
    case = {
        "case_id": case_id,
        "raw_input": raw_input,
        "expected_output": summary(result),
    }
    (target / f"{case_id}.json").write_text(
        json.dumps(case, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    for number in range(1, 51):
        write_case(
            "full",
            f"CASE-QIMEN-FULL-{number:03d}",
            {
                "local_datetime": (
                    f"2026-{(number - 1) % 12 + 1:02d}-"
                    f"{(number * 3 - 1) % 27 + 1:02d}T"
                    f"{(number * 2) % 24:02d}:00:00"
                ),
                "timezone": "Asia/Shanghai",
                "day_boundary": "zi_initial" if number % 2 == 0 else "midnight",
            },
        )
    for number in range(1, 31):
        month = (number - 1) % 12 + 1
        day = 5 if number % 2 else 20
        hour = 23 if number % 3 == 0 else 0
        minute = 55 if number % 2 else 5
        write_case(
            "boundaries",
            f"CASE-QIMEN-FULL-BOUNDARY-{number:03d}",
            {
                "local_datetime": f"2026-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:00",
                "timezone": "Asia/Shanghai",
                "day_boundary": "zi_initial" if number % 2 else "midnight",
            },
        )
    disputes = ROOT / "disputes"
    disputes.mkdir(parents=True, exist_ok=True)
    policies = ("flying_plate", "zhirun_ju", "center_host_8", "local_solar_term")
    for number in range(1, 21):
        case_id = f"CASE-QIMEN-FULL-DISPUTE-{number:03d}"
        payload = {
            "case_id": case_id,
            "declared_alternative": policies[(number - 1) % len(policies)],
            "project_lineage": "shijia-zhuanpan-chaibu-v0.3",
            "expected_decision": "lineage_mismatch_requires_separate_calculator",
        }
        (disputes / f"{case_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
