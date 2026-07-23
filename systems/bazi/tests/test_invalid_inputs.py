from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from systems.bazi.calculator.engine import CalculationError, calculate_chart

ROOT = Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / "invalid-input.schema.json").read_text(encoding="utf-8"))
CASES = [
    json.loads(path.read_text(encoding="utf-8"))
    for path in sorted((ROOT / "invalid_inputs").glob("*.json"))
]


def test_invalid_input_set_has_required_size_and_valid_contract() -> None:
    Draft202012Validator.check_schema(SCHEMA)
    validator = Draft202012Validator(SCHEMA)
    assert len(CASES) == 20
    for case in CASES:
        validator.validate(case)


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["case_id"])
def test_invalid_input_fails_with_documented_error(case: dict) -> None:
    with pytest.raises(CalculationError) as captured:
        calculate_chart(case["input"])
    assert captured.value.code == case["expected_error_code"]
    assert case["expected_message_contains"] in captured.value.message
