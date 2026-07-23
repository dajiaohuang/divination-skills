from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from divination_skills.contracts import canonical_json

from systems.ziwei.engine import calculate
from systems.ziwei.synastry import compare_charts

ROOT = Path(__file__).resolve().parent / "extension_cases" / "synastry"
CASES = [
    json.loads(path.read_text(encoding="utf-8"))
    for path in sorted(ROOT.glob("*.json"))
]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["case_id"])
def test_synastry_case_replays(case: dict) -> None:
    report = compare_charts(
        calculate(case["input"]["chart_a"]),
        calculate(case["input"]["chart_b"]),
    )
    digest = hashlib.sha256(canonical_json(report)).hexdigest()
    assert digest == case["expected_sha256"]


def test_ziwei_synastry_has_fifty_cases() -> None:
    assert len(CASES) == 50
