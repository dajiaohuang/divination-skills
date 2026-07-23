from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
from divination_skills.contracts import canonical_json

from systems.western_astrology.calculator.engine import calculate_chart
from systems.western_astrology.rectifier import scan_candidates
from systems.western_astrology.synastry import compare_charts
from systems.western_astrology.timing import calculate_timing

ROOT = Path(__file__).resolve().parent / "extension_cases"


def _cases(module: str) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / module).glob("*.json"))
    ]


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


@pytest.mark.parametrize("case", _cases("timing"), ids=lambda case: case["case_id"])
def test_timing_extension_case_replays(case: dict[str, Any]) -> None:
    value = case["input"]
    result = calculate_timing(
        calculate_chart(value["natal"]),
        target_local_datetime=value["target_local_datetime"],
        timezone=value["timezone"],
    )
    assert _digest(result) == case["expected_sha256"]


@pytest.mark.parametrize("case", _cases("synastry"), ids=lambda case: case["case_id"])
def test_synastry_extension_case_replays(case: dict[str, Any]) -> None:
    value = case["input"]
    result = compare_charts(
        calculate_chart(value["chart_a"]),
        calculate_chart(value["chart_b"]),
    )
    assert _digest(result) == case["expected_sha256"]


@pytest.mark.parametrize("case", _cases("rectifier"), ids=lambda case: case["case_id"])
def test_rectifier_extension_case_replays(case: dict[str, Any]) -> None:
    assert _digest(scan_candidates(**case["input"])) == case["expected_sha256"]


def test_each_western_extension_module_has_fifty_cases() -> None:
    assert {module: len(_cases(module)) for module in ("timing", "synastry", "rectifier")} == {
        "timing": 50,
        "synastry": 50,
        "rectifier": 50,
    }
