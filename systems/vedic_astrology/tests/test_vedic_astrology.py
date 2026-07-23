from __future__ import annotations

import json
import math
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from systems.vedic_astrology.calculator.engine import (
    NAKSHATRA_SIZE,
    VedicAstrologyError,
    _kp_stellar_item,
    _navamsha,
    _rashi_drishti,
    calculate_chart,
)

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = {
    "local_datetime": "1999-09-15T19:05:00",
    "timezone": "Asia/Shanghai",
    "longitude": 119.917,
    "latitude": 31.3,
}


def _positions(result):
    return {
        item["body"]: item
        for item in result["computed_facts"]["sidereal_chart"]["positions"]
    }


def test_sample_chart_and_lineages():
    result = calculate_chart(SAMPLE)
    chart = result["computed_facts"]["sidereal_chart"]
    positions = _positions(result)
    assert result["computed_facts"]["astronomy"]["ayanamsha"]["name"] == "true_citra"
    assert result["computed_facts"]["astronomy"]["ayanamsha"]["degrees"] == pytest.approx(
        23.83352329
    )
    assert chart["lagna"]["sign"] == "Pisces"
    assert positions["sun"]["sign"] == "Leo"
    assert positions["moon"]["sign"] == "Scorpio"
    assert positions["rahu"]["node_policy"] == "mean"
    assert abs(
        (positions["ketu"]["longitude_degrees"] - positions["rahu"]["longitude_degrees"])
        % 360
        - 180
    ) < 1e-7
    assert set(result["computed_facts"]["lineages"]) == {
        "parashari",
        "jaimini",
        "kp",
    }
    assert result["derived_findings"] == []
    assert result["narrative"] is None


def test_lineage_modules_are_isolated():
    parashari = calculate_chart({**SAMPLE, "lineages": ["parashari"]})
    kp = calculate_chart({**SAMPLE, "lineages": ["kp"]})
    assert set(parashari["computed_facts"]["lineages"]) == {"parashari"}
    assert set(kp["computed_facts"]["lineages"]) == {"kp"}
    assert kp["computed_facts"]["lineages"]["kp"]["completeness"] == (
        "stellar_identity_only"
    )
    assert "placidus_cusps" in kp["computed_facts"]["lineages"]["kp"]["unsupported"]


def test_seven_and_eight_karaka_policies_do_not_merge():
    seven = calculate_chart({**SAMPLE, "lineages": ["jaimini"]})
    eight = calculate_chart(
        {
            **SAMPLE,
            "lineages": ["jaimini"],
            "jaimini_karaka_policy": "eight",
        }
    )
    seven_items = seven["computed_facts"]["lineages"]["jaimini"]["chara_karakas"]
    eight_items = eight["computed_facts"]["lineages"]["jaimini"]["chara_karakas"]
    assert len(seven_items) == 7
    assert len(eight_items) == 8
    assert all(item["body"] != "rahu" for item in seven_items)
    rahu = next(item for item in eight_items if item["body"] == "rahu")
    assert rahu["rahu_reversal_applied"] is True


def test_rashi_drishti_table():
    relations = {item["source_sign"]: item["target_signs"] for item in _rashi_drishti()}
    assert relations["Aries"] == ["Leo", "Scorpio", "Aquarius"]
    assert relations["Taurus"] == ["Cancer", "Libra", "Capricorn"]
    assert relations["Gemini"] == ["Virgo", "Sagittarius", "Pisces"]


def test_navamsha_boundaries_are_half_open():
    assert _navamsha(0.0, "test")["sign"] == "Aries"
    assert _navamsha(30.0 / 9.0, "test")["sign"] == "Taurus"
    assert _navamsha(math.nextafter(30.0 / 9.0, 0.0), "test")["sign"] == "Aries"
    assert _navamsha(math.nextafter(30.0, 0.0), "test")["sign"] == "Sagittarius"


def test_navamsha_matches_independent_element_start_formulation():
    element_starts = (0, 9, 6, 3)
    for sign_index in range(12):
        for division in range(9):
            longitude = sign_index * 30 + (division + 0.5) * (30 / 9)
            expected = (element_starts[sign_index % 4] + division) % 12
            assert _navamsha(longitude, "test")["sign_index"] == expected


def test_kp_sub_lord_boundaries_are_half_open():
    first_span = NAKSHATRA_SIZE * 7 / 120

    def item(longitude):
        return {
            "body": "test",
            "longitude_degrees": longitude,
            "sign": "Aries",
            "sign_lord": "mars",
        }

    assert _kp_stellar_item(item(0.0))["sub_lord"] == "ketu"
    assert _kp_stellar_item(item(math.nextafter(first_span, 0.0)))["sub_lord"] == "ketu"
    assert _kp_stellar_item(item(first_span))["sub_lord"] == "venus"


def test_input_validation_fails_closed():
    with pytest.raises(VedicAstrologyError, match="Unknown field"):
        calculate_chart({**SAMPLE, "school": "mixed"})
    with pytest.raises(VedicAstrologyError, match="supports only"):
        calculate_chart({**SAMPLE, "ayanamsha": "lahiri"})
    with pytest.raises(VedicAstrologyError, match="non-empty unique"):
        calculate_chart({**SAMPLE, "lineages": ["kp", "kp"]})
    with pytest.raises(VedicAstrologyError) as ambiguous:
        calculate_chart(
            {
                "local_datetime": "2021-11-07T01:30:00",
                "timezone": "America/New_York",
                "longitude": -74.006,
                "latitude": 40.7128,
            }
        )
    assert ambiguous.value.code == "ambiguous_local_time"


def test_input_and_output_schemas():
    input_schema = json.loads(
        (ROOT / "calculator" / "input.schema.json").read_text(encoding="utf-8")
    )
    output_schema = json.loads(
        (ROOT / "calculator" / "output.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(input_schema).validate(SAMPLE)
    Draft202012Validator(output_schema).validate(calculate_chart(SAMPLE))


@pytest.mark.parametrize(
    "path",
    sorted((ROOT / "tests" / "golden").glob("*.json"))
    + sorted((ROOT / "tests" / "edge_cases").glob("*.json"))
    + sorted((ROOT / "tests" / "disputes").glob("*.json")),
    ids=lambda path: path.stem,
)
def test_case_replay(path: Path):
    document = json.loads(path.read_text(encoding="utf-8"))
    assert calculate_chart(document["raw_input"]) == document["expected_output"]
