from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
INPUT = ROOT / "systems" / "bazi" / "examples" / "sample-input.json"
CALCULATE = ROOT / "systems" / "bazi" / "skills" / "bazi-calculator" / "scripts" / "calculate.py"
VALIDATE = ROOT / "systems" / "bazi" / "skills" / "bazi-validator" / "scripts" / "validate_chart.py"
EXPLAIN = ROOT / "systems" / "bazi" / "skills" / "bazi-core" / "scripts" / "explain.py"


def test_source_skill_scripts_calculate_and_validate(tmp_path: Path) -> None:
    environment = {**os.environ, "PYTHONUTF8": "1"}
    calculated = subprocess.run(
        [sys.executable, str(CALCULATE), str(INPUT), "--compact"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    chart = json.loads(calculated.stdout)
    assert chart["computed_facts"]["pillars"]["day"]["ganzhi"] == "癸酉"

    chart_path = tmp_path / "chart.json"
    chart_path.write_text(calculated.stdout, encoding="utf-8")
    validated = subprocess.run(
        [sys.executable, str(VALIDATE), str(chart_path)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    assert json.loads(validated.stdout) == {"status": "valid", "errors": []}

    explained = subprocess.run(
        [
            sys.executable,
            str(EXPLAIN),
            str(chart_path),
            "--strength-lineage",
            "project-seasonal-support-v0.1",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    report = json.loads(explained.stdout)
    assert report["computed_facts"] == chart["computed_facts"]
    assert len(report["narrative"]["seasonal_support_path"]) == 1
