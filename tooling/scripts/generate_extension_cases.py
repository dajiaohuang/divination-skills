"""Generate one edge and one explicit dispute case for every post-Bazi system."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

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


def write_case(system_dir: str, directory: str, case: dict[str, Any]) -> None:
    target = ROOT / "systems" / system_dir / "tests" / directory
    target.mkdir(parents=True, exist_ok=True)
    (target / f"{case['case_id']}.json").write_text(
        json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def base_case(
    *,
    case_id: str,
    title: str,
    system: str,
    lineage: str,
    category: str,
    payload: dict[str, Any],
    result: dict[str, Any],
    rules: list[str],
    source_id: str,
    dispute: tuple[str, str, list[Any]] | None = None,
) -> dict[str, Any]:
    allowed = []
    if dispute is not None:
        dispute_id, field_path, values = dispute
        allowed.append(
            {"dispute_id": dispute_id, "field_path": field_path, "allowed_values": values}
        )
    return {
        "case_id": case_id,
        "title": title,
        "system": system,
        "lineage": lineage,
        "category": category,
        "data_classification": "synthetic",
        "raw_input": payload,
        "normalized_input": result["normalized_input"],
        "expected_intermediate": {
            "engine": result["engine"]["name"],
            "engine_version": result["engine"]["version"],
        },
        "expected_output": {"computed_facts": result["computed_facts"]},
        "must_match_rules": rules,
        "allowed_disagreements": allowed,
        "forbidden_conclusions": [
            "A fixed future or life event is guaranteed.",
            "An unstated lineage or calculation policy was silently substituted.",
        ],
        "sources": [{"source_id": source_id, "locator": "v0.1 engine and lineage contract"}],
        "reviewers": [
            {
                "reviewer_id": "deterministic-extension-review",
                "role": "quality",
                "reviewed_at": "2026-07-23",
                "decision": "accepted",
                "notes": (
                    "Synthetic regression review; independent domain acceptance remains pending."
                ),
            }
        ],
    }


def first_no_moving_seed() -> str:
    for value in range(10_000):
        seed = f"{value:064x}"
        result = cast_iching({"seed_hex": seed})
        if not result["computed_facts"]["moving_line_positions"]:
            return seed
    raise AssertionError("Unable to locate deterministic no-moving-line fixture.")


def emit_pair(
    *,
    system_dir: str,
    system: str,
    lineage: str,
    calculate: Callable[[dict[str, Any]], dict[str, Any]],
    edge_id: str,
    edge_title: str,
    edge_payload: dict[str, Any],
    dispute_id: str,
    dispute_case_id: str,
    dispute_title: str,
    dispute_payload: dict[str, Any],
    dispute_field: str,
    dispute_values: list[Any],
    rules: list[str],
    source_id: str,
) -> None:
    edge_result = calculate(edge_payload)
    dispute_result = calculate(dispute_payload)
    write_case(
        system_dir,
        "edge_cases",
        base_case(
            case_id=edge_id,
            title=edge_title,
            system=system,
            lineage=lineage,
            category="edge_case",
            payload=edge_payload,
            result=edge_result,
            rules=rules,
            source_id=source_id,
        ),
    )
    write_case(
        system_dir,
        "disputes",
        base_case(
            case_id=dispute_case_id,
            title=dispute_title,
            system=system,
            lineage=lineage,
            category="dispute",
            payload=dispute_payload,
            result=dispute_result,
            rules=rules,
            source_id=source_id,
            dispute=(dispute_id, dispute_field, dispute_values),
        ),
    )


def main() -> None:
    emit_pair(
        system_dir="tarot",
        system="tarot",
        lineage="rws-text-baseline-v0.1",
        calculate=draw_cards,
        edge_id="CASE-TAROT-EDGE-SEED-ZERO-001",
        edge_title="All-zero replay seed with reversals disabled",
        edge_payload={"spread": "single", "seed_hex": "00" * 32, "allow_reversals": False},
        dispute_id="DSP-TAROT-REVERSALS-001",
        dispute_case_id="CASE-TAROT-DISPUTE-REVERSALS-001",
        dispute_title="Explicit Tarot reversal policy",
        dispute_payload={"spread": "single", "seed_hex": "11" * 32, "allow_reversals": True},
        dispute_field="normalized_input.allow_reversals",
        dispute_values=[True, False],
        rules=["TAROT-DRAW-UNIQUE-001", "TAROT-ORIENTATION-UPRIGHT-001", "TAROT-POSITION-001"],
        source_id="SRC-TAROT-DECK-SPEC-001",
    )
    emit_pair(
        system_dir="western_astrology",
        system="western-astrology",
        lineage="tropical-geocentric-natal-v0.1",
        calculate=calculate_western,
        edge_id="CASE-WESTERN-EDGE-DST-FOLD-001",
        edge_title="Explicit second occurrence of an ambiguous DST time",
        edge_payload={
            "local_datetime": "2024-11-03T01:30:00",
            "timezone": "America/New_York",
            "fold": 1,
            "longitude": -74.006,
            "latitude": 40.7128,
            "house_system": "whole_sign",
        },
        dispute_id="DSP-WESTERN-HOUSE-SYSTEM-001",
        dispute_case_id="CASE-WESTERN-DISPUTE-HOUSE-SYSTEM-001",
        dispute_title="Whole-sign versus equal-house selection",
        dispute_payload={
            "local_datetime": "2000-01-01T12:00:00",
            "timezone": "UTC",
            "longitude": 0.0,
            "latitude": 51.5,
            "house_system": "whole_sign",
        },
        dispute_field="normalized_input.house_system",
        dispute_values=["whole_sign", "equal"],
        rules=["WESTERN-CAL-POSITION-001", "WESTERN-CAL-ANGLES-001", "WESTERN-HOUSE-WHOLE-001"],
        source_id="SRC-WESTERN-PROJECT-SPEC-001",
    )
    emit_pair(
        system_dir="iching",
        system="iching",
        lineage="three-coin-king-wen-structural-v0.1",
        calculate=cast_iching,
        edge_id="CASE-ICHING-EDGE-NO-MOVING-001",
        edge_title="Three-coin cast with no moving lines",
        edge_payload={"seed_hex": first_no_moving_seed()},
        dispute_id="DSP-ICHING-MOVING-LINE-PRIORITY-001",
        dispute_case_id="CASE-ICHING-DISPUTE-MOVING-LINES-001",
        dispute_title="Report-all moving-line policy",
        dispute_payload={"seed_hex": "22" * 32},
        dispute_field="interpretation.moving_line_policy",
        dispute_values=["report_all", "school_specific_priority"],
        rules=[
            "ICHING-HEXAGRAM-MAP-001",
            "ICHING-MOVING-LINES-001",
            "ICHING-STRUCTURAL-REFLECTION-001",
        ],
        source_id="SRC-ICHING-PROJECT-SPEC-001",
    )
    emit_pair(
        system_dir="liuyao",
        system="liuyao",
        lineage="wen-wang-najia-structural-v0.1",
        calculate=calculate_liuyao,
        edge_id="CASE-LIUYAO-EDGE-LATE-ZI-001",
        edge_title="Late-Zi cast with explicit zi_initial day boundary",
        edge_payload={
            "local_datetime": "2026-03-20T23:30:00",
            "timezone": "Asia/Shanghai",
            "day_boundary": "zi_initial",
            "seed_hex": "33" * 32,
        },
        dispute_id="DSP-LIUYAO-DAY-BOUNDARY-001",
        dispute_case_id="CASE-LIUYAO-DISPUTE-DAY-BOUNDARY-001",
        dispute_title="Explicit Liuyao day-boundary choice",
        dispute_payload={
            "local_datetime": "2026-03-20T23:30:00",
            "timezone": "Asia/Shanghai",
            "day_boundary": "midnight",
            "seed_hex": "33" * 32,
        },
        dispute_field="normalized_input.day_boundary",
        dispute_values=["midnight", "zi_initial"],
        rules=["LIUYAO-NAJIA-001", "LIUYAO-PALACE-SHIYING-001", "LIUYAO-CALENDAR-CONTEXT-001"],
        source_id="SRC-LIUYAO-PROJECT-SPEC-001",
    )
    emit_pair(
        system_dir="qimen",
        system="qimen",
        lineage="shijia-zhuanpan-chaibu-v0.1",
        calculate=calculate_qimen,
        edge_id="CASE-QIMEN-EDGE-SOLSTICE-001",
        edge_title="First full day after the summer-solstice dun change",
        edge_payload={"local_datetime": "2026-06-22T00:30:00", "timezone": "Asia/Shanghai"},
        dispute_id="DSP-QIMEN-JU-METHOD-001",
        dispute_case_id="CASE-QIMEN-DISPUTE-JU-METHOD-001",
        dispute_title="Chaibu ju method selection",
        dispute_payload={"local_datetime": "2026-07-23T12:00:00", "timezone": "Asia/Shanghai"},
        dispute_field="calculation.ju_method",
        dispute_values=["chaibu", "zhirun"],
        rules=["QIMEN-CHAIBU-JU-001", "QIMEN-EARTH-PLATE-001", "QIMEN-DUTY-ORIGIN-001"],
        source_id="SRC-QIMEN-PROJECT-SPEC-001",
    )
    emit_pair(
        system_dir="lenormand",
        system="lenormand",
        lineage="lenormand-36-project-v0.1",
        calculate=draw_lenormand,
        edge_id="CASE-LENORMAND-EDGE-NINE-CARD-001",
        edge_title="Maximum supported nine-card Lenormand spread",
        edge_payload={"spread": "nine-card", "seed_hex": "44" * 32},
        dispute_id="DSP-LENORMAND-REVERSALS-001",
        dispute_case_id="CASE-LENORMAND-DISPUTE-REVERSALS-001",
        dispute_title="Upright-only Lenormand policy",
        dispute_payload={"spread": "three-card", "seed_hex": "45" * 32},
        dispute_field="normalized_input.reversal_policy",
        dispute_values=["upright_only", "modern_reversals"],
        rules=["LENORMAND-CARD-UPRIGHT-001", "LENORMAND-POSITION-001", "LENORMAND-SEQUENCE-001"],
        source_id="SRC-LENORMAND-PROJECT-SPEC-001",
    )
    emit_pair(
        system_dir="runes",
        system="runes",
        lineage="elder-futhark-project-v0.1",
        calculate=draw_runes,
        edge_id="CASE-RUNES-EDGE-SINGLE-001",
        edge_title="Single-rune all-zero-seed draw",
        edge_payload={"spread": "single", "seed_hex": "00" * 32},
        dispute_id="DSP-RUNES-REVERSALS-001",
        dispute_case_id="CASE-RUNES-DISPUTE-REVERSALS-001",
        dispute_title="Upright-only rune policy",
        dispute_payload={"spread": "three-rune", "seed_hex": "55" * 32},
        dispute_field="normalized_input.reversal_policy",
        dispute_values=["upright_only", "modern_merkstave"],
        rules=["RUNES-SYMBOL-UPRIGHT-001", "RUNES-POSITION-001", "RUNES-SEQUENCE-001"],
        source_id="SRC-RUNES-PROJECT-SPEC-001",
    )
    emit_pair(
        system_dir="numerology",
        system="numerology",
        lineage="pythagorean-latin-project-v0.1",
        calculate=calculate_profile,
        edge_id="CASE-NUMEROLOGY-EDGE-DIACRITIC-001",
        edge_title="Latin name with removable diacritics on leap day",
        edge_payload={"name": "Élodie Test", "birth_date": "2000-02-29"},
        dispute_id="DSP-NUMEROLOGY-MAPPING-001",
        dispute_case_id="CASE-NUMEROLOGY-DISPUTE-MAPPING-001",
        dispute_title="Pythagorean mapping selection",
        dispute_payload={"name": "Synthetic Example", "birth_date": "2000-01-01"},
        dispute_field="normalized_input.mapping",
        dispute_values=["pythagorean-a1-i9-repeat", "chaldean"],
        rules=[
            "NUMEROLOGY-CAL-DATE-001",
            "NUMEROLOGY-CAL-NAME-001",
            "NUMEROLOGY-INTERPRET-THEME-001",
        ],
        source_id="SRC-NUMEROLOGY-PROJECT-SPEC-001",
    )
    emit_pair(
        system_dir="ziwei",
        system="ziwei",
        lineage="project-native-ziwei-foundation-v0.1",
        calculate=calculate_ziwei,
        edge_id="CASE-ZIWEI-EDGE-LATE-ZI-001",
        edge_title="Late-Zi time index 12",
        edge_payload={
            "local_datetime": "2000-01-01T23:30:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "female",
        },
        dispute_id="DSP-ZIWEI-TIME-BASIS-001",
        dispute_case_id="CASE-ZIWEI-DISPUTE-TIME-BASIS-001",
        dispute_title="Local-civil Ziwei time basis",
        dispute_payload={
            "local_datetime": "2000-01-01T12:00:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male",
        },
        dispute_field="calculation.time_basis",
        dispute_values=["local_civil", "true_solar_time"],
        rules=["ZIWEI-NATIVE-NATAL-001", "ZIWEI-TIME-INDEX-001", "ZIWEI-STRUCTURAL-BOUNDARY-001"],
        source_id="SRC-ZIWEI-PROJECT-SPEC-001",
    )
    print("Generated 18 extension edge/dispute cases.")


if __name__ == "__main__":
    main()
