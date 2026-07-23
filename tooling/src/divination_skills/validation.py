"""Validate schemas, repository documents, references, and production rights gates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError
from yaml import YAMLError, safe_load

Document = dict[str, Any]

SCHEMA_FILES = {
    "sources": "source-manifest.schema.json",
    "rules": "rule.schema.json",
    "golden_cases": "golden-case.schema.json",
    "disputes": "dispute.schema.json",
}

CONTRACT_SCHEMA_FILES = {
    "reading-session": "reading-session.schema.json",
    "chart-import": "chart-import.schema.json",
    "confidence-profile": "confidence-profile.schema.json",
    "timeline": "timeline.schema.json",
    "comparison": "comparison.schema.json",
    "report-profile": "report-profile.schema.json",
}

ID_FIELDS = {
    "sources": "source_id",
    "rules": "rule_id",
    "golden_cases": "case_id",
    "disputes": "dispute_id",
}

REQUIRED_SYSTEM_FILES = (
    "SCOPE.md",
    "LINEAGE.md",
    "DATA_CONTRACT.md",
    "KNOWN_DISPUTES.md",
    "KNOWN_LIMITATIONS.md",
    "VERSION",
)

REQUIRED_SYSTEM_JSON_DIRECTORIES = (
    "sources",
    "rules",
    "tests/golden",
    "tests/edge_cases",
    "tests/disputes",
    "disputes",
)

SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True, order=True)
class ValidationIssue:
    """A stable, printable validation failure."""

    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def load_json(path: Path) -> Document:
    """Load one UTF-8 JSON object."""

    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def load_schemas(root: Path) -> dict[str, Document]:
    """Load and self-check the four repository schemas."""

    schema_dir = root / "common" / "schemas"
    schemas: dict[str, Document] = {}
    for kind, filename in SCHEMA_FILES.items():
        schema = load_json(schema_dir / filename)
        Draft202012Validator.check_schema(schema)
        schemas[kind] = schema
    return schemas


def load_contract_schemas(root: Path) -> dict[str, Document]:
    """Load and self-check the cross-system contract schemas."""

    schema_dir = root / "common" / "schemas"
    schemas: dict[str, Document] = {}
    for kind, filename in CONTRACT_SCHEMA_FILES.items():
        schema = load_json(schema_dir / filename)
        Draft202012Validator.check_schema(schema)
        schemas[kind] = schema
    return schemas


def validate_contract_examples(
    root: Path, schemas: dict[str, Document]
) -> list[ValidationIssue]:
    """Require one valid canonical example for every cross-system contract."""

    issues: list[ValidationIssue] = []
    example_dir = root / "common" / "examples" / "contracts"
    checker = FormatChecker()
    for kind, schema in schemas.items():
        path = example_dir / f"{kind}.json"
        relative = str(path.relative_to(root))
        try:
            document = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues.append(ValidationIssue(relative, str(exc)))
            continue
        validator = Draft202012Validator(schema, format_checker=checker)
        for error in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
            location = _format_json_path(error.path)
            issues.append(ValidationIssue(f"{relative}:{location}", error.message))
    return issues


def _document_directories(root: Path, include_examples: bool) -> dict[str, list[Path]]:
    directories = {
        "sources": [root / "catalog" / "sources"],
        "rules": [],
        "golden_cases": [],
        "disputes": [],
    }

    systems_dir = root / "systems"
    if systems_dir.exists():
        for system in sorted(path for path in systems_dir.iterdir() if path.is_dir()):
            directories["sources"].append(system / "sources")
            directories["rules"].append(system / "rules")
            directories["golden_cases"].extend(
                [
                    system / "tests" / "golden",
                    system / "tests" / "edge_cases",
                    system / "tests" / "disputes",
                    system / "tests" / "negative",
                ]
            )
            directories["disputes"].append(system / "disputes")

    if include_examples:
        examples = root / "common" / "examples"
        directories["sources"].append(examples / "sources")
        directories["rules"].append(examples / "rules")
        directories["golden_cases"].append(examples / "golden-cases")
        directories["disputes"].append(examples / "disputes")

    return directories


def discover_documents(
    root: Path, include_examples: bool = True
) -> tuple[dict[str, list[tuple[Path, Document]]], list[ValidationIssue]]:
    """Load repository documents without stopping at the first malformed file."""

    documents: dict[str, list[tuple[Path, Document]]] = {kind: [] for kind in SCHEMA_FILES}
    issues: list[ValidationIssue] = []
    for kind, directories in _document_directories(root, include_examples).items():
        for directory in directories:
            if not directory.exists():
                continue
            for path in sorted(directory.glob("*.json")):
                try:
                    documents[kind].append((path, load_json(path)))
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    issues.append(ValidationIssue(str(path.relative_to(root)), str(exc)))
    return documents, issues


def _format_json_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def validate_document_schemas(
    root: Path,
    schemas: dict[str, Document],
    documents: dict[str, list[tuple[Path, Document]]],
) -> list[ValidationIssue]:
    """Validate every discovered document against its schema."""

    issues: list[ValidationIssue] = []
    checker = FormatChecker()
    for kind, entries in documents.items():
        validator = Draft202012Validator(schemas[kind], format_checker=checker)
        for path, document in entries:
            relative = str(path.relative_to(root))
            for error in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
                location = _format_json_path(error.path)
                issues.append(ValidationIssue(f"{relative}:{location}", error.message))
    return issues


def _index_documents(
    root: Path, documents: dict[str, list[tuple[Path, Document]]]
) -> tuple[dict[str, dict[str, tuple[Path, Document]]], list[ValidationIssue]]:
    indexes: dict[str, dict[str, tuple[Path, Document]]] = {kind: {} for kind in SCHEMA_FILES}
    issues: list[ValidationIssue] = []
    for kind, entries in documents.items():
        id_field = ID_FIELDS[kind]
        for path, document in entries:
            identifier = document.get(id_field)
            if not isinstance(identifier, str):
                continue
            relative = str(path.relative_to(root))
            if path.stem != identifier:
                issues.append(
                    ValidationIssue(relative, f"filename must match {id_field} {identifier!r}")
                )
            previous = indexes[kind].get(identifier)
            if previous:
                previous_relative = str(previous[0].relative_to(root))
                issues.append(
                    ValidationIssue(
                        relative,
                        f"duplicate {id_field} {identifier!r}; "
                        f"first defined in {previous_relative}",
                    )
                )
            else:
                indexes[kind][identifier] = (path, document)
    return indexes, issues


def _check_source_reference(
    issues: list[ValidationIssue],
    relative: str,
    reference: Document,
    sources: dict[str, tuple[Path, Document]],
) -> None:
    source_id = reference.get("source_id")
    if isinstance(source_id, str) and source_id not in sources:
        issues.append(ValidationIssue(relative, f"unknown source_id {source_id!r}"))


def validate_cross_references(
    root: Path, documents: dict[str, list[tuple[Path, Document]]]
) -> list[ValidationIssue]:
    """Validate IDs, references, lineage selection, and production rights gates."""

    indexes, issues = _index_documents(root, documents)
    sources = indexes["sources"]
    rules = indexes["rules"]
    cases = indexes["golden_cases"]
    disputes = indexes["disputes"]

    for path, rule in documents["rules"]:
        relative = str(path.relative_to(root))
        source_ids: list[str] = []
        for reference in rule.get("sources", []):
            _check_source_reference(issues, relative, reference, sources)
            source_id = reference.get("source_id")
            if isinstance(source_id, str):
                source_ids.append(source_id)
        for case_id in rule.get("tests", []):
            if case_id not in cases:
                issues.append(ValidationIssue(relative, f"unknown test case {case_id!r}"))
        for dispute_id in rule.get("disputes", []):
            if dispute_id not in disputes:
                issues.append(ValidationIssue(relative, f"unknown dispute {dispute_id!r}"))

        if rule.get("status") == "production":
            for source_id in source_ids:
                source = sources.get(source_id, (None, {}))[1]
                if source.get("usage_status") != "production":
                    issues.append(
                        ValidationIssue(
                            relative,
                            f"production rule uses non-production source {source_id!r}",
                        )
                    )
                if source.get("rights_review", {}).get("status") != "accepted":
                    issues.append(
                        ValidationIssue(
                            relative,
                            f"production rule uses source without accepted rights {source_id!r}",
                        )
                    )
                rights = source.get("rights", {})
                for field in ("commercial_use", "derivative_use"):
                    if rights.get(field) != "allowed":
                        issues.append(
                            ValidationIssue(
                                relative,
                                f"production rule source {source_id!r} "
                                f"has {field}={rights.get(field)!r}",
                            )
                        )

    for path, case in documents["golden_cases"]:
        relative = str(path.relative_to(root))
        for rule_id in case.get("must_match_rules", []):
            if rule_id not in rules:
                issues.append(ValidationIssue(relative, f"unknown rule_id {rule_id!r}"))
        for reference in case.get("sources", []):
            _check_source_reference(issues, relative, reference, sources)
        for disagreement in case.get("allowed_disagreements", []):
            dispute_id = disagreement.get("dispute_id")
            if isinstance(dispute_id, str) and dispute_id not in disputes:
                issues.append(ValidationIssue(relative, f"unknown dispute_id {dispute_id!r}"))

    for path, dispute in documents["disputes"]:
        relative = str(path.relative_to(root))
        lineages: list[str] = []
        for position in dispute.get("positions", []):
            lineage = position.get("lineage")
            if isinstance(lineage, str):
                lineages.append(lineage)
            for rule_id in position.get("rule_ids", []):
                if rule_id not in rules:
                    issues.append(ValidationIssue(relative, f"unknown rule_id {rule_id!r}"))
            for reference in position.get("sources", []):
                _check_source_reference(issues, relative, reference, sources)
        if len(lineages) != len(set(lineages)):
            issues.append(ValidationIssue(relative, "dispute position lineages must be unique"))
        selected = dispute.get("default_policy", {}).get("selected_lineage")
        if selected not in lineages:
            issues.append(
                ValidationIssue(relative, f"selected_lineage {selected!r} has no dispute position")
            )
        for reference in dispute.get("sources", []):
            _check_source_reference(issues, relative, reference, sources)

    return issues


def validate_system_completeness(root: Path) -> list[ValidationIssue]:
    """Require every packaged system to expose the same auditable surface."""

    issues: list[ValidationIssue] = []
    systems_dir = root / "systems"
    if not systems_dir.exists():
        return [ValidationIssue("systems", "systems directory is missing")]

    systems = sorted(
        path for path in systems_dir.iterdir() if path.is_dir() and (path / "skills").is_dir()
    )
    if not systems:
        return [ValidationIssue("systems", "no packaged systems were found")]

    for system in systems:
        system_relative = system.relative_to(root)
        for filename in REQUIRED_SYSTEM_FILES:
            path = system / filename
            relative = str(path.relative_to(root))
            if not path.is_file():
                issues.append(ValidationIssue(relative, "required system file is missing"))
            elif not path.read_text(encoding="utf-8").strip():
                issues.append(ValidationIssue(relative, "required system file is empty"))

        version_path = system / "VERSION"
        if version_path.is_file():
            version = version_path.read_text(encoding="utf-8").strip()
            if version and not SEMVER_PATTERN.fullmatch(version):
                issues.append(
                    ValidationIssue(
                        str(version_path.relative_to(root)),
                        f"VERSION must be a three-part semantic version, got {version!r}",
                    )
                )

        for directory_name in REQUIRED_SYSTEM_JSON_DIRECTORIES:
            directory = system / directory_name
            relative = str(directory.relative_to(root))
            if not directory.is_dir():
                issues.append(ValidationIssue(relative, "required directory is missing"))
            elif not any(directory.glob("*.json")):
                issues.append(ValidationIssue(relative, "must contain at least one JSON document"))

        skills_dir = system / "skills"
        skill_directories = sorted(path for path in skills_dir.iterdir() if path.is_dir())
        if not skill_directories:
            issues.append(
                ValidationIssue(str(system_relative / "skills"), "must contain a Skill package")
            )
        for skill in skill_directories:
            for relative_name in ("SKILL.md", "agents/openai.yaml"):
                path = skill / relative_name
                relative = str(path.relative_to(root))
                if not path.is_file():
                    issues.append(ValidationIssue(relative, "required Skill file is missing"))
                elif not path.read_text(encoding="utf-8").strip():
                    issues.append(ValidationIssue(relative, "required Skill file is empty"))

    return issues


def validate_skill_packages(root: Path) -> list[ValidationIssue]:
    """Validate Skill frontmatter, UI metadata, size, and local references."""

    issues: list[ValidationIssue] = []
    for skill_md in sorted((root / "systems").glob("*/skills/*/SKILL.md")):
        skill_dir = skill_md.parent
        relative_skill = str(skill_md.relative_to(root))
        text = skill_md.read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) > 500:
            issues.append(ValidationIssue(relative_skill, "SKILL.md must not exceed 500 lines"))
        if not lines or lines[0] != "---":
            issues.append(ValidationIssue(relative_skill, "missing YAML frontmatter opening"))
            continue
        try:
            closing = lines.index("---", 1)
        except ValueError:
            issues.append(ValidationIssue(relative_skill, "missing YAML frontmatter closing"))
            continue
        try:
            frontmatter = safe_load("\n".join(lines[1:closing]))
        except YAMLError as exc:
            issues.append(ValidationIssue(relative_skill, f"invalid YAML frontmatter: {exc}"))
            continue
        if not isinstance(frontmatter, dict):
            issues.append(ValidationIssue(relative_skill, "frontmatter must be an object"))
            continue
        if set(frontmatter) != {"name", "description"}:
            issues.append(
                ValidationIssue(
                    relative_skill,
                    "frontmatter must contain only name and description",
                )
            )
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        if not isinstance(name, str) or not SKILL_NAME_PATTERN.fullmatch(name) or len(name) > 64:
            issues.append(ValidationIssue(relative_skill, "invalid Skill name"))
        elif name != skill_dir.name:
            issues.append(ValidationIssue(relative_skill, "Skill name must match its directory"))
        if not isinstance(description, str) or not description.strip():
            issues.append(ValidationIssue(relative_skill, "description must be non-empty"))

        for target in MARKDOWN_LINK_PATTERN.findall("\n".join(lines[closing + 1 :])):
            if target.startswith(("http://", "https://", "#")):
                continue
            path = skill_dir / target.split("#", 1)[0]
            if not path.is_file():
                issues.append(
                    ValidationIssue(relative_skill, f"linked local file does not exist: {target}")
                )

        metadata_path = skill_dir / "agents" / "openai.yaml"
        relative_metadata = str(metadata_path.relative_to(root))
        try:
            metadata = safe_load(metadata_path.read_text(encoding="utf-8"))
        except (OSError, YAMLError) as exc:
            issues.append(ValidationIssue(relative_metadata, f"invalid UI metadata: {exc}"))
            continue
        interface = metadata.get("interface") if isinstance(metadata, dict) else None
        if not isinstance(interface, dict):
            issues.append(ValidationIssue(relative_metadata, "interface must be an object"))
            continue
        for field in ("display_name", "short_description", "default_prompt"):
            if not isinstance(interface.get(field), str) or not interface[field].strip():
                issues.append(ValidationIssue(relative_metadata, f"missing interface.{field}"))
        short_description = interface.get("short_description", "")
        if isinstance(short_description, str) and not 25 <= len(short_description) <= 64:
            issues.append(
                ValidationIssue(
                    relative_metadata,
                    "interface.short_description must contain 25 to 64 characters",
                )
            )
        default_prompt = interface.get("default_prompt", "")
        if (
            isinstance(name, str)
            and isinstance(default_prompt, str)
            and f"${name}" not in default_prompt
        ):
            issues.append(
                ValidationIssue(
                    relative_metadata,
                    f"interface.default_prompt must mention ${name}",
                )
            )

    return issues


def validate_repository(root: Path, include_examples: bool = True) -> list[ValidationIssue]:
    """Run all repository validations and return stable sorted issues."""

    root = root.resolve()
    try:
        schemas = load_schemas(root)
        contract_schemas = load_contract_schemas(root)
    except (OSError, ValueError, SchemaError) as exc:
        return [ValidationIssue("common/schemas", f"schema loading failed: {exc}")]

    documents, issues = discover_documents(root, include_examples=include_examples)
    issues.extend(validate_contract_examples(root, contract_schemas))
    issues.extend(validate_document_schemas(root, schemas, documents))
    issues.extend(validate_cross_references(root, documents))
    issues.extend(validate_system_completeness(root))
    issues.extend(validate_skill_packages(root))
    return sorted(set(issues))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path, help="repository root")
    parser.add_argument("--no-examples", action="store_true", help="exclude common schema examples")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    issues = validate_repository(args.root, include_examples=not args.no_examples)
    if issues:
        for issue in issues:
            print(f"ERROR {issue}", file=sys.stderr)
        print(f"Validation failed with {len(issues)} issue(s).", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
