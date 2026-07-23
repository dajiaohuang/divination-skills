"""Compare exported Ziwei JSON without importing or executing a reference repository."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ALLOWED_CLASSIFICATIONS = {
    "display_name_difference",
    "lineage_difference",
    "boundary_policy_difference",
    "project_error",
    "reference_error",
    "pending_research",
}


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result = {}
        for key in sorted(value):
            path = f"{prefix}.{key}" if prefix else key
            result.update(_flatten(value[key], path))
        return result
    if isinstance(value, list):
        result = {}
        for index, item in enumerate(value):
            path = f"{prefix}.{index}" if prefix else str(index)
            result.update(_flatten(item, path))
        return result
    return {prefix: value}


def compare(
    native: dict[str, Any],
    reference: dict[str, Any],
    classifications: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return a non-authoritative local difference report."""

    labels = classifications or {}
    invalid = sorted(set(labels.values()) - ALLOWED_CLASSIFICATIONS)
    if invalid:
        raise ValueError(f"Unsupported classifications: {', '.join(invalid)}")
    left = _flatten(native)
    right = _flatten(reference)
    details = []
    counts: Counter[str] = Counter()
    for path in sorted(set(left) | set(right)):
        if path not in left:
            classification = "project_missing"
        elif path not in right:
            classification = "reference_missing"
        elif left[path] == right[path]:
            classification = "exact_match"
        else:
            classification = labels.get(path, "pending_research")
        counts[classification] += 1
        if classification != "exact_match":
            details.append(
                {
                    "path": path,
                    "classification": classification,
                    "native": left.get(path),
                    "reference": right.get(path),
                }
            )
    return {
        "format": "ziwei-reference-diff-v1",
        "authoritative": False,
        "runtime_dependency": False,
        "counts": dict(sorted(counts.items())),
        "differences": details,
        "warnings": [
            "This report is not a Golden Set and cannot update production cases.",
            "Unclassified value differences remain pending_research.",
            "The comparator reads exported JSON and never executes a reference repository.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--classifications", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    native = json.loads(args.native.read_text(encoding="utf-8"))
    reference = json.loads(args.reference.read_text(encoding="utf-8"))
    classifications = (
        json.loads(args.classifications.read_text(encoding="utf-8"))
        if args.classifications
        else None
    )
    report = compare(native, reference, classifications)
    rendered = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
