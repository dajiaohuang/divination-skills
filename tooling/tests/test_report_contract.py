from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from systems.bazi.calculator.engine import calculate_chart as calculate_bazi
from systems.bazi.core.report import build_report as report_bazi
from systems.iching.engine import cast as cast_iching
from systems.iching.engine import explain as explain_iching
from systems.lenormand.engine import draw as draw_lenormand
from systems.lenormand.engine import explain as explain_lenormand
from systems.liuyao.engine import calculate as calculate_liuyao
from systems.liuyao.engine import explain as explain_liuyao
from systems.numerology.calculator.engine import calculate_profile
from systems.numerology.core.report import build_report as report_numerology
from systems.qimen.engine import calculate as calculate_qimen
from systems.qimen.engine import explain as explain_qimen
from systems.runes.engine import draw as draw_runes
from systems.runes.engine import explain as explain_runes
from systems.tarot.core.report import build_report as report_tarot
from systems.tarot.draw.engine import draw_cards
from systems.western_astrology.calculator.engine import calculate_chart as calculate_western
from systems.western_astrology.core.report import build_report as report_western
from systems.ziwei.engine import calculate as calculate_ziwei
from systems.ziwei.engine import structural_report as report_ziwei

ROOT = Path(__file__).resolve().parents[2]


def reports() -> dict[str, dict]:
    return {
        "bazi": report_bazi(
            calculate_bazi({"local_datetime": "2000-01-01T12:00:00", "timezone": "Asia/Shanghai"})
        ),
        "iching": explain_iching(cast_iching({"seed_hex": "01" * 32})),
        "lenormand": explain_lenormand(
            draw_lenormand({"spread": "three-card", "seed_hex": "02" * 32})
        ),
        "liuyao": explain_liuyao(
            calculate_liuyao(
                {
                    "local_datetime": "2026-07-23T12:00:00",
                    "timezone": "Asia/Shanghai",
                    "seed_hex": "03" * 32,
                }
            )
        ),
        "numerology": report_numerology(
            calculate_profile({"birth_date": "2000-01-01", "name": "Synthetic Example"})
        ),
        "qimen": explain_qimen(
            calculate_qimen({"local_datetime": "2026-07-23T12:00:00", "timezone": "Asia/Shanghai"})
        ),
        "runes": explain_runes(draw_runes({"spread": "three-rune", "seed_hex": "04" * 32})),
        "tarot": report_tarot(
            draw_cards(
                {
                    "spread": "situation-challenge-guidance",
                    "seed_hex": "05" * 32,
                }
            )
        ),
        "western-astrology": report_western(
            calculate_western(
                {
                    "local_datetime": "2000-01-01T12:00:00",
                    "timezone": "UTC",
                    "longitude": 0.0,
                    "latitude": 51.5,
                    "house_system": "whole_sign",
                }
            )
        ),
        "ziwei": report_ziwei(
            calculate_ziwei(
                {
                    "local_datetime": "2000-01-01T12:00:00",
                    "timezone": "Asia/Shanghai",
                    "calculation_gender": "female",
                }
            )
        ),
    }


REPORTS = reports()


@pytest.mark.parametrize("system", sorted(REPORTS))
def test_every_system_report_uses_the_common_envelope(system: str) -> None:
    schema = json.loads(
        (ROOT / "common" / "report-spec" / "auditable-report.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(REPORTS[system])


@pytest.mark.parametrize(
    "relative",
    [
        "common/report-spec/auditable-report.schema.json",
        "common/evaluation/evaluation-report.schema.json",
    ],
)
def test_supplemental_schemas_are_valid(relative: str) -> None:
    schema = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
