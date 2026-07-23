from __future__ import annotations

import copy
from pathlib import Path

from divination_skills.validation import (
    discover_documents,
    load_schemas,
    validate_cross_references,
    validate_document_schemas,
    validate_skill_packages,
    validate_source_snapshots,
    validate_system_completeness,
)

ROOT = Path(__file__).resolve().parents[2]


def test_reference_only_manifest_is_valid_but_not_production() -> None:
    schemas = load_schemas(ROOT)
    documents, loading_issues = discover_documents(ROOT)
    assert loading_issues == []
    assert validate_document_schemas(ROOT, schemas, documents) == []
    manifest = next(
        document
        for _, document in documents["sources"]
        if document["source_id"] == "SRC-VEDIC-REF-001"
    )
    assert manifest["usage_status"] == "reference_only"
    assert manifest["rights_review"]["status"] == "reference_only"


def test_cross_reference_validator_reports_unknown_source() -> None:
    documents, loading_issues = discover_documents(ROOT)
    assert loading_issues == []
    changed = copy.deepcopy(documents)
    path, rule = changed["rules"][0]
    rule["sources"][0]["source_id"] = "SRC-MISSING-001"
    issues = validate_cross_references(ROOT, changed)
    assert any("unknown source_id 'SRC-MISSING-001'" in issue.message for issue in issues)


def test_cross_reference_validator_requires_source_system_coverage() -> None:
    documents, loading_issues = discover_documents(ROOT)
    assert loading_issues == []
    changed = copy.deepcopy(documents)
    path, rule = next(
        entry for entry in changed["rules"] if "systems/liuyao/" in entry[0].as_posix()
    )
    source_id = rule["sources"][0]["source_id"]
    source = next(
        document
        for _, document in changed["sources"]
        if document["source_id"] == source_id
    )
    source["systems"] = ["unrelated"]
    issues = validate_cross_references(ROOT, changed)
    assert any(
        f"source {source_id!r} does not declare system 'liuyao'" in issue.message
        for issue in issues
    )


def test_production_rule_cannot_use_reference_only_source() -> None:
    documents, loading_issues = discover_documents(ROOT)
    assert loading_issues == []
    changed = copy.deepcopy(documents)
    path, rule = changed["rules"][0]
    rule["status"] = "production"
    rule["sources"][0]["source_id"] = "SRC-VEDIC-REF-001"
    issues = validate_cross_references(ROOT, changed)
    messages = "\n".join(issue.message for issue in issues)
    assert "non-production source 'SRC-VEDIC-REF-001'" in messages
    assert "without accepted rights 'SRC-VEDIC-REF-001'" in messages


def test_computed_output_trace_ids_must_be_registered() -> None:
    documents, loading_issues = discover_documents(ROOT)
    assert loading_issues == []
    changed = copy.deepcopy(documents)
    _, case = changed["golden_cases"][0]
    case.setdefault("expected_output", {})["synthetic_trace"] = {
        "rule_ids": ["RULE-MISSING-001"],
        "source_ids": ["SRC-MISSING-OUTPUT-001"],
    }
    issues = validate_cross_references(ROOT, changed)
    messages = "\n".join(issue.message for issue in issues)
    assert "computed output uses unknown rule_id 'RULE-MISSING-001'" in messages
    assert "unknown source_id 'SRC-MISSING-OUTPUT-001'" in messages


def test_malformed_json_is_reported_without_crashing(tmp_path: Path) -> None:
    root = tmp_path
    (root / "catalog/sources").mkdir(parents=True)
    (root / "catalog/sources/broken.json").write_text("{", encoding="utf-8")
    documents, issues = discover_documents(root)
    assert documents["sources"] == []
    assert len(issues) == 1


def test_all_packaged_systems_are_complete() -> None:
    assert validate_system_completeness(ROOT) == []


def test_all_registered_sources_have_verified_markdown_snapshots() -> None:
    documents, loading_issues = discover_documents(ROOT)
    assert loading_issues == []
    assert validate_source_snapshots(ROOT, documents) == []


def test_system_completeness_reports_missing_contract_and_corpora(tmp_path: Path) -> None:
    skill = tmp_path / "systems/demo/skills/demo"
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: demo\ndescription: demo\n---\n", encoding="utf-8")
    (skill / "agents/openai.yaml").write_text("interface: {}\n", encoding="utf-8")

    issues = validate_system_completeness(tmp_path)
    paths = {issue.path.replace("\\", "/") for issue in issues}
    assert "systems/demo/DATA_CONTRACT.md" in paths
    assert "systems/demo/tests/edge_cases" in paths


def test_all_skill_metadata_and_local_links_are_valid() -> None:
    assert validate_skill_packages(ROOT) == []


def test_skill_validator_reports_missing_skill_token(tmp_path: Path) -> None:
    skill = tmp_path / "systems/demo/skills/demo"
    (skill / "agents").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: demo\n"
        "description: Demonstration skill.\n"
        "---\n\n"
        "See [missing](references/missing.md).\n",
        encoding="utf-8",
    )
    (skill / "agents/openai.yaml").write_text(
        "interface:\n"
        '  display_name: "Demo"\n'
        '  short_description: "Demonstrate an intentionally invalid skill"\n'
        '  default_prompt: "Run this demonstration."\n',
        encoding="utf-8",
    )
    rendered = "\n".join(str(issue) for issue in validate_skill_packages(tmp_path))
    assert "linked local file does not exist" in rendered
    assert "must mention $demo" in rendered
