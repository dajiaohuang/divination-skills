"""Generate 50 replay cases per Bazi extension module."""

from __future__ import annotations

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from divination_skills.contracts import canonical_json

from systems.bazi.calculator.engine import calculate_chart
from systems.bazi.rectifier import scan_candidates
from systems.bazi.synastry import compare_charts
from systems.bazi.timing import calculate_timing

ROOT = Path(__file__).resolve().parent / "extension_cases"


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def _write(module: str, number: int, payload: dict[str, Any], result: dict[str, Any]) -> None:
    directory = ROOT / module
    directory.mkdir(parents=True, exist_ok=True)
    case = {
        "case_id": f"CASE-BAZI-{module.upper()}-{number:03d}",
        "system": "bazi",
        "module": module,
        "category": "standard",
        "data_classification": "synthetic",
        "input": payload,
        "expected_sha256": _digest(result),
        "status": "tested",
    }
    (directory / f"{case['case_id']}.json").write_text(
        json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _events(offset: int) -> list[dict[str, str]]:
    return [
        {
            "event_id": f"event-{offset}-{index}",
            "start_date": f"{2010 + offset % 5 + index:04d}-06-01",
            "end_date": f"{2010 + offset % 5 + index:04d}-06-30",
            "split": "training" if index < 4 else "holdout",
        }
        for index in range(5)
    ]


def main() -> None:
    for directory in ROOT.glob("*"):
        if directory.is_dir():
            for path in directory.glob("*.json"):
                path.unlink()
    start = date(1950, 1, 15)
    for index in range(50):
        birth = start + timedelta(days=index * 367)
        natal_payload = {
            "local_datetime": f"{birth.isoformat()}T{(index * 2) % 24:02d}:30:00",
            "timezone": "Asia/Shanghai",
            "day_boundary": "midnight",
            "luck_cycle_direction": "forward" if index % 2 == 0 else "reverse",
        }
        natal = calculate_chart(natal_payload)
        target_year = min(2099, birth.year + 30)
        timing_payload = {
            "natal": natal_payload,
            "target_local_datetime": f"{target_year:04d}-07-23T12:00:00",
            "timezone": "Asia/Shanghai",
        }
        timing = calculate_timing(
            natal,
            target_local_datetime=timing_payload["target_local_datetime"],
            timezone=timing_payload["timezone"],
        )
        _write("timing", index + 1, timing_payload, timing)

        other_birth = birth + timedelta(days=400 + index)
        other_payload = {
            "local_datetime": f"{other_birth.isoformat()}T{(index * 3) % 24:02d}:15:00",
            "timezone": "Asia/Shanghai",
            "day_boundary": "midnight",
            "luck_cycle_direction": "reverse" if index % 2 == 0 else "forward",
        }
        synastry_payload = {"chart_a": natal_payload, "chart_b": other_payload}
        synastry = compare_charts(natal, calculate_chart(other_payload))
        _write("synastry", index + 1, synastry_payload, synastry)

        rectifier_payload = {
            "birth_date": f"{1980 + index % 20:04d}-01-15",
            "timezone": "Asia/Shanghai",
            "events": _events(index),
            "day_boundary": "midnight",
        }
        rectification = scan_candidates(**rectifier_payload)
        _write("rectifier", index + 1, rectifier_payload, rectification)
    print("Generated 150 Bazi extension cases (50 per module).")


if __name__ == "__main__":
    main()
