"""Structured Western astrology JSON and CSV reader."""

from __future__ import annotations

import csv
import io
import json
from copy import deepcopy
from typing import Any


def _csv_chart(value: str) -> dict[str, Any]:
    reader = csv.DictReader(io.StringIO(value))
    required = {"body", "longitude_degrees"}
    if reader.fieldnames is None or not required <= set(reader.fieldnames):
        raise ValueError("CSV requires body and longitude_degrees columns.")
    positions = []
    for index, row in enumerate(reader, start=1):
        body = (row.get("body") or "").strip().lower()
        if not body:
            raise ValueError(f"CSV row {index} is missing body.")
        try:
            longitude = float(row["longitude_degrees"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"CSV row {index} has invalid longitude_degrees.") from exc
        if not 0 <= longitude < 360:
            raise ValueError(f"CSV row {index} longitude is outside 0–360.")
        position: dict[str, Any] = {
            "fact_id": f"western.import.position.{body}",
            "body": body,
            "longitude_degrees": longitude,
        }
        if row.get("house"):
            try:
                house = int(row["house"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"CSV row {index} has invalid house.") from exc
            if not 1 <= house <= 12:
                raise ValueError(f"CSV row {index} house is outside 1–12.")
            position["house"] = house
        positions.append(position)
    if not positions:
        raise ValueError("CSV must contain at least one position.")
    return {"computed_facts": {"positions": positions}}


def _validate_positions(positions: Any) -> None:
    if not isinstance(positions, list) or not positions:
        raise ValueError("Imported chart must contain computed_facts.positions.")
    bodies: list[str] = []
    for index, position in enumerate(positions, start=1):
        if not isinstance(position, dict):
            raise ValueError(f"Position {index} must be an object.")
        body = position.get("body")
        longitude = position.get("longitude_degrees")
        if not isinstance(body, str) or not body.strip():
            raise ValueError(f"Position {index} has an invalid body.")
        if (
            isinstance(longitude, bool)
            or not isinstance(longitude, (int, float))
            or not 0 <= longitude < 360
        ):
            raise ValueError(f"Position {index} has invalid longitude_degrees.")
        house = position.get("house")
        if house is not None and (
            isinstance(house, bool) or not isinstance(house, int) or not 1 <= house <= 12
        ):
            raise ValueError(f"Position {index} has an invalid house.")
        bodies.append(body.strip().lower())
    if len(bodies) != len(set(bodies)):
        raise ValueError("Imported position bodies must be unique.")


def read_structured(value: str | dict[str, Any], *, format: str = "json") -> dict[str, Any]:
    if format == "json":
        if isinstance(value, str):
            try:
                imported = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError("Input must be valid Western astrology JSON.") from exc
        elif isinstance(value, dict):
            imported = deepcopy(value)
        else:
            raise TypeError("JSON input must be a string or object.")
    elif format == "csv":
        if not isinstance(value, str):
            raise TypeError("CSV input must be a string.")
        imported = _csv_chart(value)
    else:
        raise ValueError("format must be json or csv.")
    positions = imported.get("computed_facts", {}).get("positions")
    _validate_positions(positions)
    return {
        "schema_version": "0.2.0",
        "system": "western-astrology",
        "format": format,
        "imported_chart": imported,
        "native_facts_overwritten": False,
        "warnings": [
            {
                "code": "untrusted_import",
                "message": "Imported positions remain untrusted until native comparison.",
            }
        ],
    }
