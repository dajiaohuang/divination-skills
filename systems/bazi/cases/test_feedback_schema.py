from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


def test_feedback_example_separates_prior_analysis_from_later_outcome() -> None:
    root = Path(__file__).resolve().parent
    schema = json.loads((root / "feedback.schema.json").read_text(encoding="utf-8"))
    example = json.loads((root / "feedback.example.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    validator.validate(example)
    assert example["analysis"]["recorded_at"] < example["outcome"]["recorded_at"]
    assert example["analysis"]["timing"] == "pre_outcome"
