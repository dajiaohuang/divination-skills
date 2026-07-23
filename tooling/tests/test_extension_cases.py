from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from systems.iching.engine import cast as cast_iching
from systems.lenormand.engine import draw as draw_lenormand
from systems.liuyao.engine import calculate as calculate_liuyao
from systems.numerology.calculator.engine import calculate_profile
from systems.qimen.engine import calculate as calculate_qimen
from systems.runes.engine import draw as draw_runes
from systems.tarot.draw.engine import draw_cards
from systems.western_astrology.calculator.engine import calculate_chart as calculate_western
from systems.ziwei.engine import calculate as calculate_ziwei

ROOT = Path(__file__).resolve().parents[2]
CALCULATORS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "tarot": draw_cards,
    "western-astrology": calculate_western,
    "iching": cast_iching,
    "liuyao": calculate_liuyao,
    "qimen": calculate_qimen,
    "lenormand": draw_lenormand,
    "runes": draw_runes,
    "numerology": calculate_profile,
    "ziwei": calculate_ziwei,
}


def cases() -> list[dict[str, Any]]:
    values = []
    for system_dir in sorted(path for path in (ROOT / "systems").iterdir() if path.is_dir()):
        for directory in ("edge_cases", "disputes"):
            for path in sorted((system_dir / "tests" / directory).glob("*.json")):
                case = json.loads(path.read_text(encoding="utf-8"))
                if case["system"] in CALCULATORS and case["system"] != "bazi":
                    values.append(case)
    return values


@pytest.mark.parametrize("case", cases(), ids=lambda case: case["case_id"])
def test_extension_edge_and_dispute_cases_replay(case: dict[str, Any]) -> None:
    result = CALCULATORS[case["system"]](case["raw_input"])
    assert result["computed_facts"] == case["expected_output"]["computed_facts"]
