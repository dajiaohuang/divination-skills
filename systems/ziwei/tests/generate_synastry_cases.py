"""Generate 50 Ziwei structural synastry replay cases."""

from __future__ import annotations

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from divination_skills.contracts import canonical_json

from systems.ziwei.engine import calculate
from systems.ziwei.synastry import compare_charts

OUTPUT = Path(__file__).resolve().parent / "extension_cases" / "synastry"


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT.glob("*.json"):
        path.unlink()
    start = date(1950, 1, 15)
    for index in range(50):
        date_a = start + timedelta(days=index * 367)
        date_b = date_a + timedelta(days=400 + index)
        input_a = {
            "local_datetime": f"{date_a.isoformat()}T{index % 24:02d}:15:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male" if index % 2 == 0 else "female",
        }
        input_b = {
            "local_datetime": f"{date_b.isoformat()}T{(index + 7) % 24:02d}:45:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "female" if index % 2 == 0 else "male",
        }
        report = compare_charts(calculate(input_a), calculate(input_b))
        case = {
            "case_id": f"CASE-ZIWEI-SYNASTRY-{index + 1:03d}",
            "system": "ziwei",
            "module": "synastry",
            "category": "standard",
            "data_classification": "synthetic",
            "input": {"chart_a": input_a, "chart_b": input_b},
            "expected_sha256": _digest(report),
            "status": "tested",
        }
        (OUTPUT / f"{case['case_id']}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print("Generated 50 Ziwei synastry cases.")


if __name__ == "__main__":
    main()
