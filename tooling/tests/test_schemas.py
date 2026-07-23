from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from divination_skills.validation import load_schemas, validate_repository
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]

EXAMPLE_FILES = {
    "sources": ROOT / "common/examples/sources/SRC-EXAMPLE-STANDARD-001.json",
    "rules": ROOT / "common/examples/rules/EXAMPLE-CAL-001.json",
    "golden_cases": ROOT
    / "common/examples/golden-cases/CASE-EXAMPLE-STANDARD-001.json",
    "disputes": ROOT / "common/examples/disputes/DSP-EXAMPLE-BOUNDARY-001.json",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mutate(document: dict, path: tuple[str, ...], value: object, *, delete: bool = False) -> dict:
    changed = copy.deepcopy(document)
    target = changed
    for part in path[:-1]:
        target = target[part]
    if delete:
        del target[path[-1]]
    else:
        target[path[-1]] = value
    return changed


INVALID_MUTATIONS = {
    "sources": [
        (("title",), None, True),
        (("source_id",), "bad-id", False),
        (("rights", "commercial_use"), "maybe", False),
    ],
    "rules": [
        (("conditions",), [], False),
        (("priority",), 1001, False),
        (("version",), "version-one", False),
    ],
    "golden_cases": [
        (("must_match_rules",), [], False),
        (("category",), "ordinary", False),
        (("reviewers",), [], False),
    ],
    "disputes": [
        (("positions",), [], False),
        (("user_disclosure",), "", False),
        (("sources",), [], False),
    ],
}


def test_repository_passes_all_validations() -> None:
    assert validate_repository(ROOT) == []


@pytest.mark.parametrize("kind", sorted(EXAMPLE_FILES))
def test_each_schema_has_three_valid_examples(kind: str) -> None:
    directory = EXAMPLE_FILES[kind].parent
    schemas = load_schemas(ROOT)
    validator = Draft202012Validator(schemas[kind], format_checker=FormatChecker())
    examples = sorted(directory.glob("*.json"))
    assert len(examples) >= 3
    for example in examples:
        validator.validate(load(example))


@pytest.mark.parametrize(
    ("kind", "path", "value", "delete"),
    [
        (kind, path, value, delete)
        for kind, mutations in INVALID_MUTATIONS.items()
        for path, value, delete in mutations
    ],
)
def test_each_schema_rejects_three_invalid_variants(
    kind: str, path: tuple[str, ...], value: object, delete: bool
) -> None:
    schemas = load_schemas(ROOT)
    validator = Draft202012Validator(schemas[kind], format_checker=FormatChecker())
    invalid = mutate(load(EXAMPLE_FILES[kind]), path, value, delete=delete)
    assert list(validator.iter_errors(invalid)), f"{kind} unexpectedly accepted mutation {path}"
