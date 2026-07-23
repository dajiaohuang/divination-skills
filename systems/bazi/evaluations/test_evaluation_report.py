from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from systems.bazi.evaluations.run_evaluation import REPORT_PATH, evaluate

ROOT = Path(__file__).resolve().parents[3]


def test_committed_evaluation_report_is_current_and_schema_valid() -> None:
    expected = evaluate()
    committed = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / "common" / "evaluation" / "evaluation-report.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(committed)
    assert committed == expected
    assert committed["overall"]["technical_pass"] is True
    assert committed["overall"]["release_ready"] is False
