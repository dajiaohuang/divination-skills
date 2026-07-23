from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CALCULATE = (
    ROOT / "systems" / "western_astrology" / "skills" / "western-natal" / "scripts" / "calculate.py"
)
EXPLAIN = (
    ROOT / "systems" / "western_astrology" / "skills" / "western-core" / "scripts" / "explain.py"
)


def test_western_skill_scripts_round_trip(tmp_path: Path) -> None:
    payload = {
        "local_datetime": "2000-01-01T12:00:00",
        "timezone": "UTC",
        "longitude": 0.0,
        "latitude": 51.4779,
    }
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")
    environment = {**os.environ, "PYTHONUTF8": "1"}
    calculated = subprocess.run(
        [sys.executable, str(CALCULATE), str(input_path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    chart = json.loads(calculated.stdout)
    chart_path = tmp_path / "chart.json"
    chart_path.write_text(calculated.stdout, encoding="utf-8")
    explained = subprocess.run(
        [sys.executable, str(EXPLAIN), str(chart_path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    report = json.loads(explained.stdout)
    assert report["computed_facts"] == chart["computed_facts"]
    assert report["narrative"]["placements"]
