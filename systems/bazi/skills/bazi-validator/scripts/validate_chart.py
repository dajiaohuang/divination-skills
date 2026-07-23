"""Validate one structured Bazi chart and its source references."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

SCRIPT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = (
    SCRIPT_ROOT if (SCRIPT_ROOT / "systems").is_dir() else Path(__file__).resolve().parents[5]
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))
SCHEMA_PATH = REPOSITORY_ROOT / "systems" / "bazi" / "calculator" / "output.schema.json"

from systems.bazi.validator import compare_chart  # noqa: E402


def known_source_ids() -> set[str]:
    paths = [
        REPOSITORY_ROOT / "catalog" / "sources",
        REPOSITORY_ROOT / "systems" / "bazi" / "sources",
    ]
    identifiers: set[str] = set()
    for directory in paths:
        for path in directory.glob("*.json"):
            value = json.loads(path.read_text(encoding="utf-8"))
            identifiers.add(value["source_id"])
    return identifiers


def validate_chart(path: Path) -> list[str]:
    chart = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(chart)]
    known = known_source_ids()
    for source_id in chart.get("engine", {}).get("source_ids", []):
        if source_id not in known:
            errors.append(f"Unknown engine source_id: {source_id}")
    normalized = chart.get("normalized_input", {})
    solar_applied = normalized.get("true_solar_time_applied")
    correction = normalized.get("solar_time_correction")
    if solar_applied and (
        normalized.get("time_basis") != "apparent_solar" or not isinstance(correction, dict)
    ):
        errors.append("apparent-solar charts must include a traceable solar-time correction")
    if not solar_applied and correction is not None:
        errors.append("civil-time charts must not include a solar-time correction")
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chart", type=Path)
    parser.add_argument("--imported", type=Path)
    args = parser.parse_args(argv)
    comparison = None
    try:
        errors = validate_chart(args.chart)
        if not errors and args.imported:
            native = json.loads(args.chart.read_text(encoding="utf-8"))
            imported = json.loads(args.imported.read_text(encoding="utf-8"))
            comparison = compare_chart(native, imported)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    result = {
        "status": "valid" if not errors else "invalid",
        "errors": errors,
    }
    if args.imported:
        result["comparison"] = comparison
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
