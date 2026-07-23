"""Structured Bazi JSON and four-pillar text reader."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from typing import Any

from systems.bazi.calculator.engine import BRANCHES, STEMS

PILLAR_PATTERN = re.compile(
    rf"([{''.join(STEMS)}][{''.join(BRANCHES)}])"
)


def _text_chart(value: str) -> dict[str, Any]:
    pillars = PILLAR_PATTERN.findall(value)
    if len(pillars) != 4:
        raise ValueError("Text import must contain exactly four stem-branch pillars.")
    return {
        "computed_facts": {
            "pillars": {
                position: {
                    "position": position,
                    "stem": {"name": pillar[0]},
                    "branch": {"name": pillar[1]},
                }
                for position, pillar in zip(
                    ("year", "month", "day", "hour"),
                    pillars,
                    strict=True,
                )
            }
        }
    }


def read_structured(value: str | dict[str, Any], *, format: str = "json") -> dict[str, Any]:
    if format == "json":
        if isinstance(value, str):
            try:
                imported = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError("Input must be valid Bazi JSON.") from exc
        elif isinstance(value, dict):
            imported = deepcopy(value)
        else:
            raise TypeError("JSON input must be a string or object.")
    elif format == "four_pillar_text":
        if not isinstance(value, str):
            raise TypeError("Four-pillar text input must be a string.")
        imported = _text_chart(value)
    else:
        raise ValueError("format must be json or four_pillar_text.")
    pillars = imported.get("computed_facts", {}).get("pillars")
    if not isinstance(pillars, dict) or set(pillars) != {"year", "month", "day", "hour"}:
        raise ValueError("Imported chart must contain year, month, day, and hour pillars.")
    return {
        "schema_version": "0.2.0",
        "system": "bazi",
        "format": format,
        "imported_chart": imported,
        "native_facts_overwritten": False,
        "warnings": [
            {
                "code": "untrusted_import",
                "message": "Imported pillars remain untrusted until native comparison.",
            }
        ],
    }
