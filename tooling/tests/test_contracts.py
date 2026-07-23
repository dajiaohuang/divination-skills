from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from divination_skills.contracts import (
    build_confidence_profile,
    build_reading_session,
    copy_without_sensitive_input,
    legacy_chart_reference,
    redact_session_for_log,
    select_report_sections,
    stable_identifier,
    validate_timeline_intervals,
)
from divination_skills.validation import load_contract_schemas
from jsonschema import Draft202012Validator, FormatChecker

from systems.ziwei.engine import calculate as calculate_ziwei

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "common" / "examples" / "contracts"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(kind: str, value: dict) -> None:
    schema = load_contract_schemas(ROOT)[kind]
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)


def test_all_contract_schemas_have_valid_canonical_examples() -> None:
    schemas = load_contract_schemas(ROOT)
    assert set(schemas) == {
        "chart-import",
        "comparison",
        "confidence-profile",
        "reading-session",
        "report-profile",
        "timeline",
    }
    for kind, schema in schemas.items():
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(
            load(EXAMPLES / f"{kind}.json")
        )


@pytest.mark.parametrize(
    ("kind", "mutation"),
    [
        ("reading-session", lambda value: value["privacy"].update(log_policy="full")),
        ("chart-import", lambda value: value.update(canonical_authority="external")),
        (
            "confidence-profile",
            lambda value: value["input_precision"].update(level="second_exact"),
        ),
        ("timeline", lambda value: value["entries"][0].update(scope="fortune")),
        (
            "comparison",
            lambda value: value["directional_facts"][0].update(direction="both"),
        ),
        ("report-profile", lambda value: value.update(mode="medical")),
    ],
)
def test_each_contract_rejects_a_policy_breaking_variant(kind: str, mutation) -> None:
    value = copy.deepcopy(load(EXAMPLES / f"{kind}.json"))
    mutation(value)
    schema = load_contract_schemas(ROOT)[kind]
    assert list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value))


def test_stable_identifiers_ignore_dictionary_order() -> None:
    assert stable_identifier("SESSION", {"b": 2, "a": 1}) == stable_identifier(
        "SESSION", {"a": 1, "b": 2}
    )


def test_confidence_profile_degrades_and_blocks_by_declared_precision() -> None:
    profile = build_confidence_profile(
        level="hour_range",
        source="reported",
        uncertainty_minutes=60,
        requested_modules=["natal.date", "timing.day", "minute_sensitive"],
    )
    validate("confidence-profile", profile)
    assert profile["module_access"] == {
        "minute_sensitive": "blocked",
        "natal.date": "allowed",
        "timing.day": "degraded",
    }
    assert profile["disabled_modules"] == ["minute_sensitive"]


def test_reading_session_defaults_are_ephemeral_and_log_safe() -> None:
    session = build_reading_session(
        data_classification="synthetic",
        question_category="natal",
        question_text="Synthetic private-looking date 1990-01-01 must not enter logs.",
        chart_refs=[
            {
                "chart_id": "CHART-EXAMPLE-001",
                "system": "bazi",
                "role": "primary",
                "validation_status": "valid",
            }
        ],
    )
    validate("reading-session", session)
    logged = redact_session_for_log(session)
    serialized = json.dumps(logged, ensure_ascii=False)
    assert "1990-01-01" not in serialized
    assert "CHART-EXAMPLE-001" not in serialized
    assert logged["systems"] == ["bazi"]
    assert logged["persistence"] is False


def test_ephemeral_session_rejects_retention_or_persistence() -> None:
    with pytest.raises(ValueError, match="Ephemeral"):
        build_reading_session(
            data_classification="synthetic",
            question_category="general",
            question_text="Fixture",
            chart_refs=[
                {
                    "chart_id": "CHART-EXAMPLE-001",
                    "system": "bazi",
                    "role": "primary",
                    "validation_status": "valid",
                }
            ],
            persistence=True,
            retention_days=1,
        )


def test_legacy_chart_wrapper_does_not_copy_birth_input() -> None:
    chart = {
        "raw_input": {"local_datetime": "1990-01-01T12:00:00"},
        "normalized_input": {"timezone": "Asia/Shanghai"},
        "computed_facts": {"pillars": {"day": {"ganzhi": "甲子"}}},
        "validation": {"status": "valid"},
    }
    reference = legacy_chart_reference(chart, system="bazi")
    assert reference["chart_id"].startswith("CHART-")
    assert "1990" not in json.dumps(reference)
    assert copy_without_sensitive_input(chart) == {
        "computed_facts": chart["computed_facts"],
        "validation": {"status": "valid"},
    }


def test_every_existing_system_golden_chart_can_be_wrapped_without_migration() -> None:
    systems = sorted(
        path for path in (ROOT / "systems").iterdir() if (path / "skills").is_dir()
    )
    assert len(systems) == 10
    for system in systems:
        case_path = next(iter(sorted((system / "tests" / "golden").glob("*.json"))))
        case = load(case_path)
        chart = case["expected_output"]
        if "computed_facts" not in chart and case["system"] == "ziwei":
            chart = calculate_ziwei(case["raw_input"])
        reference = legacy_chart_reference(chart, system=case["system"])
        validate(
            "reading-session",
            build_reading_session(
                data_classification="synthetic",
                question_category="validation",
                question_text=f"Wrap the existing {case['system']} chart.",
                chart_refs=[reference],
            ),
        )


def test_timeline_semantic_validation_rejects_reverse_and_duplicate_intervals() -> None:
    timeline = load(EXAMPLES / "timeline.json")
    timeline["entries"].append(copy.deepcopy(timeline["entries"][0]))
    timeline["entries"][1]["start"] = "2040-01-01T00:00:00Z"
    timeline["entries"][1]["end"] = "2039-01-01T00:00:00Z"
    errors = validate_timeline_intervals(timeline)
    assert any("duplicates" in error for error in errors)
    assert any("ends before" in error for error in errors)


def test_report_selector_fails_closed_for_missing_required_sections() -> None:
    profile = load(EXAMPLES / "report-profile.json")
    selected = select_report_sections(
        profile,
        available_fact_ids=["bazi.pillars.year"],
        available_rule_ids=[],
    )
    assert selected["included_sections"] == []
    assert selected["ready"] is False
    assert selected["omitted_sections"][0]["missing_rule_prefixes"] == ["BAZI-FACT-"]
