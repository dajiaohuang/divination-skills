from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from systems.multi_natal.engine import NatalSynthesisError, calculate_natal_synthesis

ROOT = Path(__file__).resolve().parents[3]
SYSTEM = ROOT / "systems" / "multi_natal"


def sample_input() -> dict:
    return {
        "birth_date": "2000-01-01",
        "birth_time": "12:00",
        "birthplace": {
            "name": "Shanghai, China",
            "timezone": "Asia/Shanghai",
            "longitude": 121.4737,
            "latitude": 31.2304,
            "resolution_source": "user_confirmed",
        },
        "calculation_gender": "female",
    }


def expected_subset(result: dict) -> dict:
    cross_checks = result["computed_facts"]["cross_checks"]
    return {
        "included_systems": result["normalized_input"]["included_systems"],
        "system_summaries": result["computed_facts"]["system_summaries"],
        "axis_ids": [
            item["axis_id"] for item in result["computed_facts"]["synthesis_axes"]
        ],
        "utc_all_equal": cross_checks["utc"]["all_equal"],
        "astronomy_status": cross_checks["tropical_astronomy"]["status"],
        "maximum_astronomy_difference_degrees": cross_checks[
            "tropical_astronomy"
        ]["maximum_absolute_difference_degrees"],
    }


def test_calculates_four_native_systems_without_repository_dependencies() -> None:
    result = calculate_natal_synthesis(sample_input())
    assert result["normalized_input"]["included_systems"] == [
        "bazi",
        "western-astrology",
        "ziwei",
        "vedic-astrology",
    ]
    assert set(result["computed_facts"]["charts"]) == {
        "bazi",
        "western-astrology",
        "ziwei",
        "vedic-astrology",
    }
    assert result["engine"]["repository_dependencies"] == []
    assert result["computed_facts"]["charts"]["vedic-astrology"]["engine"][
        "repository_dependencies"
    ] == []


def test_cross_checks_one_utc_instant_and_tropical_astronomy() -> None:
    result = calculate_natal_synthesis(sample_input())
    checks = result["computed_facts"]["cross_checks"]
    assert checks["utc"]["all_equal"] is True
    assert checks["tropical_astronomy"]["status"] == "consistent"
    assert checks["tropical_astronomy"]["maximum_absolute_difference_degrees"] <= 0.000001
    assert "does not compare Western tropical signs" in checks[
        "tropical_astronomy"
    ]["note"]


def test_synthesis_does_not_mutate_native_charts_or_score_agreement() -> None:
    result = calculate_natal_synthesis(sample_input())
    charts = result["computed_facts"]["charts"]
    original = deepcopy(charts)
    axes = result["computed_facts"]["synthesis_axes"]
    assert charts == original
    assert {item["axis_id"] for item in axes} == {
        "core-identity",
        "inner-reflection",
        "vocation",
        "relationships",
        "resources",
    }
    assert all("agreement" not in item for item in axes)
    assert all(
        item["dispute_ids"] == ["DSP-MULTI-NATAL-COMPARABILITY-001"]
        for item in axes
    )


def test_optional_numerology_runs_selected_mappings_separately() -> None:
    payload = sample_input()
    payload["numerology"] = {
        "name": "Alex Example",
        "mappings": ["pythagorean", "chaldean"],
    }
    result = calculate_natal_synthesis(payload)
    assert set(result["computed_facts"]["charts"]["numerology"]) == {
        "pythagorean",
        "chaldean",
    }
    summary = result["computed_facts"]["system_summaries"]["numerology"]
    assert set(summary["mappings"]) == {"pythagorean", "chaldean"}


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (lambda value: value["birthplace"].pop("timezone"), "unresolved_birthplace"),
        (
            lambda value: value.__setitem__("calculation_gender", "unspecified"),
            "invalid_calculation_gender",
        ),
        (
            lambda value: value["birthplace"].__setitem__("resolution_source", "guessed"),
            "invalid_resolution_source",
        ),
    ],
)
def test_required_birth_metadata_fails_closed(mutation, code: str) -> None:
    payload = sample_input()
    mutation(payload)
    with pytest.raises(NatalSynthesisError) as caught:
        calculate_natal_synthesis(payload)
    assert caught.value.code == code


def test_ambiguous_dst_requires_fold() -> None:
    payload = {
        "birth_date": "2021-11-07",
        "birth_time": "01:30",
        "birthplace": {
            "name": "New York, New York, United States",
            "timezone": "America/New_York",
            "longitude": -74.006,
            "latitude": 40.7128,
            "resolution_source": "user_confirmed",
        },
        "calculation_gender": "male",
    }
    with pytest.raises(NatalSynthesisError) as caught:
        calculate_natal_synthesis(payload)
    assert caught.value.code == "bazi.ambiguous_local_time"
    payload["fold"] = 1
    result = calculate_natal_synthesis(payload)
    assert result["computed_facts"]["cross_checks"]["utc"]["all_equal"] is True


def test_input_and_output_schemas_accept_runtime_document() -> None:
    input_schema = json.loads(
        (SYSTEM / "calculator" / "input.schema.json").read_text(encoding="utf-8")
    )
    output_schema = json.loads(
        (SYSTEM / "calculator" / "output.schema.json").read_text(encoding="utf-8")
    )
    payload = sample_input()
    Draft202012Validator(
        input_schema, format_checker=FormatChecker()
    ).validate(payload)
    Draft202012Validator(output_schema).validate(
        calculate_natal_synthesis(payload)
    )
    invalid_time = deepcopy(payload)
    invalid_time["birth_time"] = "29:00"
    assert list(
        Draft202012Validator(
            input_schema, format_checker=FormatChecker()
        ).iter_errors(invalid_time)
    )


def test_committed_cases_replay() -> None:
    for directory in ("golden", "edge_cases", "disputes"):
        for path in sorted((SYSTEM / "tests" / directory).glob("*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            result = calculate_natal_synthesis(case["raw_input"])
            assert result["normalized_input"] == case["normalized_input"]
            assert expected_subset(result) == case["expected_output"]
            assert all(
                status
                == case["expected_intermediate"]["native_validation"][system]
                for system, status in {
                    system: chart["validation"]["status"]
                    for system, chart in result["computed_facts"]["charts"].items()
                    if system != "numerology"
                }.items()
            )
