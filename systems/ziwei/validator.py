"""Validate imported Ziwei structures without replacing native facts."""

from __future__ import annotations

from typing import Any


def compare_chart(native: dict[str, Any], imported: dict[str, Any]) -> dict[str, Any]:
    native_palaces = native.get("computed_facts", {}).get("palaces", [])
    imported_palaces = imported.get("computed_facts", {}).get("palaces", [])
    if len(native_palaces) != 12:
        raise ValueError("Native chart must contain twelve palaces.")
    if len(imported_palaces) != 12:
        return {
            "status": "invalid_import",
            "differences": [
                {
                    "path": "computed_facts.palaces",
                    "classification": "missing_or_invalid",
                    "native": 12,
                    "imported": len(imported_palaces),
                }
            ],
            "native_chart_unchanged": True,
        }

    differences = []
    for index, (left, right) in enumerate(zip(native_palaces, imported_palaces, strict=True)):
        for field in ("name", "heavenlyStem", "earthlyBranch", "isBodyPalace"):
            if left.get(field) != right.get(field):
                differences.append(
                    {
                        "path": f"computed_facts.palaces.{index}.{field}",
                        "classification": "structural_difference",
                        "native": left.get(field),
                        "imported": right.get(field),
                    }
                )
        for group in ("majorStars", "minorStars", "adjectiveStars", "auxiliaryStars"):
            left_names = sorted(star["name"] for star in left.get(group, []))
            right_names = sorted(star["name"] for star in right.get(group, []))
            if left_names != right_names:
                differences.append(
                    {
                        "path": f"computed_facts.palaces.{index}.{group}",
                        "classification": "placement_difference",
                        "native": left_names,
                        "imported": right_names,
                    }
                )
    return {
        "status": "match" if not differences else "different",
        "differences": differences,
        "native_chart_unchanged": True,
    }
