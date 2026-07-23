"""Tolerance-aware Western natal chart comparison."""

from __future__ import annotations

from typing import Any


def _angular_delta(left: float, right: float) -> float:
    return abs((left - right + 180) % 360 - 180)


def compare_chart(
    native: dict[str, Any],
    imported: dict[str, Any],
    *,
    longitude_tolerance_degrees: float = 0.01,
) -> dict[str, Any]:
    if not 0 <= longitude_tolerance_degrees <= 1:
        raise ValueError("longitude_tolerance_degrees must be between 0 and 1.")
    native_positions = {
        item["body"]: item for item in native.get("computed_facts", {}).get("positions", [])
    }
    imported_positions = {
        item["body"]: item for item in imported.get("computed_facts", {}).get("positions", [])
    }
    if not native_positions:
        raise ValueError("Native chart must contain positions.")
    differences = []
    for body in sorted(set(native_positions) | set(imported_positions)):
        if body not in native_positions:
            differences.append(
                {
                    "path": f"computed_facts.positions.{body}",
                    "classification": "native_missing_body",
                }
            )
            continue
        if body not in imported_positions:
            differences.append(
                {
                    "path": f"computed_facts.positions.{body}",
                    "classification": "import_missing_body",
                }
            )
            continue
        left = native_positions[body]
        right = imported_positions[body]
        delta = _angular_delta(
            left["longitude_degrees"],
            right["longitude_degrees"],
        )
        if delta > longitude_tolerance_degrees:
            differences.append(
                {
                    "path": f"computed_facts.positions.{body}.longitude_degrees",
                    "classification": "position_difference",
                    "native": left["longitude_degrees"],
                    "imported": right["longitude_degrees"],
                    "delta_degrees": round(delta, 8),
                    "tolerance_degrees": longitude_tolerance_degrees,
                }
            )
        if "house" in right and left.get("house") != right["house"]:
            differences.append(
                {
                    "path": f"computed_facts.positions.{body}.house",
                    "classification": "house_difference",
                    "native": left.get("house"),
                    "imported": right["house"],
                }
            )
    for angle in ("ascendant", "midheaven"):
        left = native.get("computed_facts", {}).get("angles", {}).get(angle)
        right = imported.get("computed_facts", {}).get("angles", {}).get(angle)
        if right is not None and left is not None:
            delta = _angular_delta(
                left["longitude_degrees"],
                right["longitude_degrees"],
            )
            if delta > longitude_tolerance_degrees:
                differences.append(
                    {
                        "path": f"computed_facts.angles.{angle}.longitude_degrees",
                        "classification": "angle_difference",
                        "native": left["longitude_degrees"],
                        "imported": right["longitude_degrees"],
                        "delta_degrees": round(delta, 8),
                        "tolerance_degrees": longitude_tolerance_degrees,
                    }
                )
    return {
        "status": "match" if not differences else "different",
        "differences": differences,
        "native_chart_unchanged": True,
        "tolerance_degrees": longitude_tolerance_degrees,
    }
