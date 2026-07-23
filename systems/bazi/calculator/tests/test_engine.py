from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from systems.bazi.calculator.comparator import lunar_python_reference
from systems.bazi.calculator.engine import CalculationError, calculate_chart

CALCULATOR_DIR = Path(__file__).resolve().parents[1]

SHANGHAI_COMPARISON_CASES = [
    "1900-02-04T13:30:00",
    "1912-01-01T00:00:00",
    "1927-12-31T22:15:00",
    "1949-10-01T15:00:00",
    "1966-06-06T06:06:00",
    "1970-01-01T00:00:00",
    "1978-12-18T11:30:00",
    "1986-05-29T19:30:00",
    "1990-01-01T12:00:00",
    "1997-07-01T00:00:00",
    "2000-01-07T12:00:00",
    "2008-08-08T20:08:00",
    "2012-02-29T23:30:00",
    "2020-11-01T08:30:00",
    "2024-02-04T16:27:06",
    "2024-02-04T16:27:08",
    "2025-02-03T22:10:28",
    "2038-01-19T03:14:07",
    "2050-09-23T10:00:00",
    "2099-12-31T23:30:00",
]


def pillar_strings(chart: dict) -> dict[str, str]:
    return {
        position: value["ganzhi"] for position, value in chart["computed_facts"]["pillars"].items()
    }


@pytest.mark.parametrize("local_datetime", SHANGHAI_COMPARISON_CASES)
def test_four_pillars_match_pinned_independent_api(local_datetime: str) -> None:
    payload = {
        "local_datetime": local_datetime,
        "timezone": "Asia/Shanghai",
        "day_boundary": "midnight",
    }
    assert pillar_strings(calculate_chart(payload)) == lunar_python_reference(payload)


def test_exact_solar_term_instant_changes_year_and_month() -> None:
    before = calculate_chart({"local_datetime": "2024-02-04T16:27:06", "timezone": "Asia/Shanghai"})
    after = calculate_chart({"local_datetime": "2024-02-04T16:27:07", "timezone": "Asia/Shanghai"})
    assert pillar_strings(before)["year"] == "癸卯"
    assert pillar_strings(before)["month"] == "乙丑"
    assert pillar_strings(after)["year"] == "甲辰"
    assert pillar_strings(after)["month"] == "丙寅"


def test_late_zi_boundary_policies_are_explicit() -> None:
    base = {"local_datetime": "2024-01-01T23:30:00", "timezone": "Asia/Shanghai"}
    midnight = calculate_chart({**base, "day_boundary": "midnight"})
    zi_initial = calculate_chart({**base, "day_boundary": "zi_initial"})
    assert pillar_strings(midnight)["day"] == "甲子"
    assert pillar_strings(zi_initial)["day"] == "乙丑"
    assert pillar_strings(midnight)["hour"] == pillar_strings(zi_initial)["hour"] == "丙子"


def test_nonexistent_dst_time_is_rejected() -> None:
    with pytest.raises(CalculationError, match="does not exist") as error:
        calculate_chart(
            {
                "local_datetime": "2024-03-10T02:30:00",
                "timezone": "America/New_York",
            }
        )
    assert error.value.code == "nonexistent_local_time"


def test_ambiguous_dst_time_requires_fold_and_produces_distinct_instants() -> None:
    payload = {
        "local_datetime": "2024-11-03T01:30:00",
        "timezone": "America/New_York",
    }
    with pytest.raises(CalculationError) as error:
        calculate_chart(payload)
    assert error.value.code == "ambiguous_local_time"
    early = calculate_chart({**payload, "fold": 0})
    late = calculate_chart({**payload, "fold": 1})
    assert early["normalized_input"]["utc_datetime"] != late["normalized_input"]["utc_datetime"]


@pytest.mark.parametrize("fold", [True, False])
def test_boolean_fold_is_rejected_instead_of_coerced_to_integer(fold: bool) -> None:
    with pytest.raises(CalculationError) as error:
        calculate_chart(
            {
                "local_datetime": "2024-11-03T01:30:00",
                "timezone": "America/New_York",
                "fold": fold,
            }
        )
    assert error.value.code == "invalid_fold"


def test_same_instant_has_same_year_month_and_local_day_hour() -> None:
    shanghai = calculate_chart(
        {"local_datetime": "2024-02-04T16:27:08", "timezone": "Asia/Shanghai"}
    )
    new_york = calculate_chart(
        {"local_datetime": "2024-02-04T03:27:08", "timezone": "America/New_York"}
    )
    shanghai_pillars = pillar_strings(shanghai)
    new_york_pillars = pillar_strings(new_york)
    assert shanghai_pillars["year"] == new_york_pillars["year"]
    assert shanghai_pillars["month"] == new_york_pillars["month"]
    assert shanghai_pillars["hour"] != new_york_pillars["hour"]


def test_solar_term_provider_uses_fixed_utc8_not_historical_dst() -> None:
    chart = calculate_chart({"local_datetime": "1986-05-29T19:30:00", "timezone": "Asia/Shanghai"})
    assert chart["normalized_input"]["local_datetime"].endswith("+09:00")
    assert chart["computed_facts"]["previous_month_boundary"]["beijing_datetime"].endswith("+08:00")


@pytest.mark.parametrize(
    ("payload", "code"),
    [
        ({"local_datetime": "1899-12-31T23:59:59", "timezone": "UTC"}, "date_out_of_range"),
        ({"local_datetime": "2101-01-01T00:00:00", "timezone": "UTC"}, "date_out_of_range"),
        ({"local_datetime": "2024-01-01T00:00:00", "timezone": "Mars/Olympus"}, "unknown_timezone"),
        (
            {"local_datetime": "2024-01-01T00:00:00+08:00", "timezone": "Asia/Shanghai"},
            "offset_not_allowed",
        ),
        (
            {
                "local_datetime": "2024-01-01T00:00:00",
                "timezone": "UTC",
                "true_solar_time": True,
            },
            "longitude_required",
        ),
    ],
)
def test_invalid_inputs_fail_closed(payload: dict, code: str) -> None:
    with pytest.raises(CalculationError) as error:
        calculate_chart(payload)
    assert error.value.code == code


def test_luck_cycles_require_explicit_direction() -> None:
    payload = {"local_datetime": "1990-01-01T12:00:00", "timezone": "Asia/Shanghai"}
    without = calculate_chart(payload)
    forward = calculate_chart({**payload, "luck_cycle_direction": "forward"})
    reverse = calculate_chart({**payload, "luck_cycle_direction": "reverse"})
    assert without["computed_facts"]["luck_cycles"] is None
    assert len(forward["computed_facts"]["luck_cycles"]["cycles"]) == 10
    assert (
        forward["computed_facts"]["luck_cycles"]["cycles"][0]["pillar"]["ganzhi"]
        != reverse["computed_facts"]["luck_cycles"]["cycles"][0]["pillar"]["ganzhi"]
    )


def test_output_matches_contract_schema() -> None:
    chart = calculate_chart(
        {
            "local_datetime": "1986-05-29T19:30:00",
            "timezone": "Asia/Shanghai",
            "longitude": 121.47,
            "latitude": 31.23,
            "luck_cycle_direction": "forward",
        }
    )
    schema = json.loads((CALCULATOR_DIR / "output.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(chart)
    assert chart["computed_facts"]["day_master"]["name"] == "癸"
    assert chart["computed_facts"]["ten_gods"]["visible"]["day"] == "比肩"


def test_input_schema_accepts_explicit_true_solar_time_policy() -> None:
    schema = json.loads((CALCULATOR_DIR / "input.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    assert not list(
        validator.iter_errors({"local_datetime": "2024-01-01T00:00:00", "timezone": "UTC"})
    )
    assert not list(
        validator.iter_errors(
            {
                "local_datetime": "2024-01-01T00:00:00",
                "timezone": "UTC",
                "true_solar_time": True,
                "longitude": 0,
            }
        )
    )


def test_same_input_reproduces_identical_facts() -> None:
    payload = {
        "local_datetime": "1986-05-29T19:30:00",
        "timezone": "Asia/Shanghai",
        "luck_cycle_direction": "forward",
    }
    first = calculate_chart(payload)
    second = calculate_chart(payload)
    assert first["computed_facts"] == second["computed_facts"]
    assert first["normalized_input"] == second["normalized_input"]
