"""Validate imported Ziwei structures without replacing native facts."""

from __future__ import annotations

from typing import Any


def _self_transformation_signature(star: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    return sorted(
        (
            item.get("direction"),
            item.get("transformation"),
            item.get("origin_stem"),
            item.get("origin_palace_fact_id"),
        )
        for item in star.get("self_transformations", [])
    )


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
    for field in ("time_basis", "calculation_datetime", "true_solar_time_applied"):
        left_value = native.get("normalized_input", {}).get(field)
        right_value = imported.get("normalized_input", {}).get(field)
        if left_value != right_value:
            differences.append(
                {
                    "path": f"normalized_input.{field}",
                    "classification": "time_basis_difference",
                    "native": left_value,
                    "imported": right_value,
                }
            )
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
                continue
            left_by_name = {star["name"]: star for star in left.get(group, [])}
            right_by_name = {star["name"]: star for star in right.get(group, [])}
            for name in left_names:
                left_star = left_by_name[name]
                right_star = right_by_name[name]
                if left_star.get("brightness") != right_star.get("brightness"):
                    differences.append(
                        {
                            "path": (f"computed_facts.palaces.{index}.{group}.{name}.brightness"),
                            "classification": "brightness_difference",
                            "native": left_star.get("brightness"),
                            "imported": right_star.get("brightness"),
                        }
                    )
                if left_star.get("mutagen") != right_star.get("mutagen"):
                    differences.append(
                        {
                            "path": (f"computed_facts.palaces.{index}.{group}.{name}.mutagen"),
                            "classification": "transformation_difference",
                            "native": left_star.get("mutagen"),
                            "imported": right_star.get("mutagen"),
                        }
                    )
                left_self = _self_transformation_signature(left_star)
                right_self = _self_transformation_signature(right_star)
                if left_self != right_self:
                    differences.append(
                        {
                            "path": (
                                f"computed_facts.palaces.{index}.{group}."
                                f"{name}.self_transformations"
                            ),
                            "classification": "self_transformation_difference",
                            "native": left_self,
                            "imported": right_self,
                        }
                    )
    return {
        "status": "match" if not differences else "different",
        "differences": differences,
        "native_chart_unchanged": True,
    }
