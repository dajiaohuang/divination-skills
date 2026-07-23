"""Generate 50 replay cases per Western extension module."""

from __future__ import annotations

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from divination_skills.contracts import canonical_json

from systems.western_astrology.calculator.engine import calculate_chart
from systems.western_astrology.rectifier import scan_candidates
from systems.western_astrology.synastry import compare_charts
from systems.western_astrology.timing import calculate_timing

ROOT = Path(__file__).resolve().parent / "extension_cases"


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def _write(module: str, number: int, payload: dict[str, Any], result: dict[str, Any]) -> None:
    directory = ROOT / module
    directory.mkdir(parents=True, exist_ok=True)
    case = {
        "case_id": f"CASE-WESTERN-{module.upper()}-{number:03d}",
        "system": "western-astrology",
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


def _chart_payload(value: date, hour: int) -> dict[str, Any]:
    return {
        "local_datetime": f"{value.isoformat()}T{hour:02d}:15:00",
        "timezone": "UTC",
        "longitude": 0.0,
        "latitude": 51.4779,
        "house_system": "whole_sign",
    }


def _events(offset: int) -> list[dict[str, str]]:
    return [
        {
            "event_id": f"event-{offset}-{index}",
            "start_date": f"{2010 + offset % 5 + index:04d}-06-01",
            "end_date": f"{2010 + offset % 5 + index:04d}-06-30",
            "event_type": "dated_event",
            "evidence_quality": "documented" if index % 2 == 0 else "reported",
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
        natal_payload = _chart_payload(birth, index % 24)
        natal = calculate_chart(natal_payload)
        timing_payload = {
            "natal": natal_payload,
            "target_local_datetime": f"{2000 + index:04d}-07-23T12:00:00",
            "timezone": "UTC",
        }
        timing = calculate_timing(
            natal,
            target_local_datetime=timing_payload["target_local_datetime"],
            timezone="UTC",
        )
        _write("timing", index + 1, timing_payload, timing)

        other_payload = _chart_payload(birth + timedelta(days=400 + index), (index + 7) % 24)
        synastry_payload = {"chart_a": natal_payload, "chart_b": other_payload}
        synastry = compare_charts(natal, calculate_chart(other_payload))
        _write("synastry", index + 1, synastry_payload, synastry)

        rectifier_payload = {
            "birth_date": f"{1980 + index % 20:04d}-01-15",
            "timezone": "UTC",
            "longitude": 0.0,
            "latitude": 51.4779,
            "events": _events(index),
            "interval_minutes": 60,
        }
        rectification = scan_candidates(**rectifier_payload)
        _write("rectifier", index + 1, rectifier_payload, rectification)
    print("Generated 150 Western extension cases (50 per module).")


if __name__ == "__main__":
    main()
