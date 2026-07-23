"""Compare imported Bazi facts with a native calculation."""

from __future__ import annotations

from typing import Any


def compare_chart(native: dict[str, Any], imported: dict[str, Any]) -> dict[str, Any]:
    native_pillars = native.get("computed_facts", {}).get("pillars", {})
    imported_pillars = imported.get("computed_facts", {}).get("pillars", {})
    if set(native_pillars) != {"year", "month", "day", "hour"}:
        raise ValueError("Native chart must contain four pillars.")
    if set(imported_pillars) != {"year", "month", "day", "hour"}:
        return {
            "status": "invalid_import",
            "differences": [
                {
                    "path": "computed_facts.pillars",
                    "classification": "missing_or_invalid",
                }
            ],
            "native_chart_unchanged": True,
        }
    differences = []
    for position in ("year", "month", "day", "hour"):
        for component in ("stem", "branch"):
            left = native_pillars[position][component]["name"]
            right = imported_pillars[position][component]["name"]
            if left != right:
                differences.append(
                    {
                        "path": (
                            f"computed_facts.pillars.{position}.{component}.name"
                        ),
                        "classification": "pillar_difference",
                        "native": left,
                        "imported": right,
                    }
                )
    native_boundary = native.get("normalized_input", {}).get("day_boundary")
    imported_boundary = imported.get("normalized_input", {}).get("day_boundary")
    if imported_boundary is not None and imported_boundary != native_boundary:
        differences.append(
            {
                "path": "normalized_input.day_boundary",
                "classification": "boundary_policy_difference",
                "native": native_boundary,
                "imported": imported_boundary,
            }
        )
    return {
        "status": "match" if not differences else "different",
        "differences": differences,
        "native_chart_unchanged": True,
    }
