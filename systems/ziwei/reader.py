"""Read structured Ziwei JSON while preserving native/imported separation."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from systems.ziwei.validator import compare_chart


def read_structured(value: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, str):
        try:
            imported = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError("Input must be valid structured Ziwei JSON.") from exc
    elif isinstance(value, dict):
        imported = deepcopy(value)
    else:
        raise TypeError("Input must be a JSON string or object.")
    if not isinstance(imported.get("computed_facts"), dict):
        raise ValueError("Imported chart is missing computed_facts.")
    if not isinstance(imported["computed_facts"].get("palaces"), list):
        raise ValueError("Imported chart is missing computed_facts.palaces.")
    return {
        "schema_version": "0.5.0",
        "format": "structured_json",
        "imported_chart": imported,
        "native_facts_overwritten": False,
        "warnings": [
            {
                "code": "untrusted_import",
                "message": "Imported facts remain untrusted until compared with a native chart.",
            }
        ],
    }


def read_and_compare(
    value: str | dict[str, Any],
    native_chart: dict[str, Any],
) -> dict[str, Any]:
    result = read_structured(value)
    result["comparison"] = compare_chart(native_chart, result["imported_chart"])
    return result
