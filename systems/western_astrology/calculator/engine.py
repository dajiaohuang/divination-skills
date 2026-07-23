"""Calculate a bounded tropical geocentric natal chart."""

from __future__ import annotations

import math
from datetime import UTC
from itertools import combinations
from typing import Any

import astronomy
from divination_skills.time import TimeNormalizationError, localize_strict

SIGNS = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)
BODIES = (
    ("sun", astronomy.Body.Sun),
    ("moon", astronomy.Body.Moon),
    ("mercury", astronomy.Body.Mercury),
    ("venus", astronomy.Body.Venus),
    ("mars", astronomy.Body.Mars),
    ("jupiter", astronomy.Body.Jupiter),
    ("saturn", astronomy.Body.Saturn),
    ("uranus", astronomy.Body.Uranus),
    ("neptune", astronomy.Body.Neptune),
    ("pluto", astronomy.Body.Pluto),
)
ASPECTS = (
    ("conjunction", 0.0, 8.0),
    ("sextile", 60.0, 5.0),
    ("square", 90.0, 7.0),
    ("trine", 120.0, 7.0),
    ("opposition", 180.0, 8.0),
)
SOURCE_IDS = [
    "SRC-WESTERN-ASTRONOMY-ENGINE-001",
    "SRC-WESTERN-PROJECT-SPEC-001",
    "SRC-WESTERN-PTOLEMY-001",
    "SRC-TIME-PYTHON-ZONEINFO-001",
    "SRC-TIME-TZDATA-001",
]
TRADITIONAL_DOMICILES = {
    "sun": ("Leo",),
    "moon": ("Cancer",),
    "mercury": ("Gemini", "Virgo"),
    "venus": ("Taurus", "Libra"),
    "mars": ("Aries", "Scorpio"),
    "jupiter": ("Sagittarius", "Pisces"),
    "saturn": ("Capricorn", "Aquarius"),
}
TRADITIONAL_EXALTATIONS = {
    "sun": "Aries",
    "moon": "Taurus",
    "mercury": "Virgo",
    "venus": "Pisces",
    "mars": "Capricorn",
    "jupiter": "Cancer",
    "saturn": "Libra",
}
OPPOSITE_SIGN = {sign: SIGNS[(index + 6) % 12] for index, sign in enumerate(SIGNS)}


class AstrologyError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _normalize(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {"local_datetime", "timezone", "fold", "longitude", "latitude", "house_system"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise AstrologyError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    for field in ("local_datetime", "timezone", "longitude", "latitude"):
        if field not in payload:
            raise AstrologyError(f"missing_{field}", f"{field} is required.")
    longitude = payload["longitude"]
    latitude = payload["latitude"]
    if (
        isinstance(longitude, bool)
        or not isinstance(longitude, (int, float))
        or not -180 <= longitude <= 180
    ):
        raise AstrologyError("invalid_longitude", "longitude must be a number from -180 to 180.")
    if (
        isinstance(latitude, bool)
        or not isinstance(latitude, (int, float))
        or not -89 <= latitude <= 89
    ):
        raise AstrologyError("invalid_latitude", "latitude must be a number from -89 to 89.")
    house_system = payload.get("house_system", "whole_sign")
    if house_system not in {"whole_sign", "equal"}:
        raise AstrologyError("invalid_house_system", "house_system must be whole_sign or equal.")
    try:
        local, fold = localize_strict(
            payload["local_datetime"], payload["timezone"], payload.get("fold")
        )
    except TimeNormalizationError as exc:
        raise AstrologyError(exc.code, exc.message) from exc
    if not 1900 <= local.year <= 2100:
        raise AstrologyError("date_out_of_range", "Supported years are 1900 through 2100.")
    utc = local.astimezone(UTC)
    return {
        "local": local,
        "utc": utc,
        "timezone": payload["timezone"],
        "fold": fold,
        "longitude": float(longitude),
        "latitude": float(latitude),
        "house_system": house_system,
    }


def _astro_time(utc) -> astronomy.Time:
    text = utc.isoformat(timespec="microseconds").replace("+00:00", "Z")
    return astronomy.Time.Parse(text)


def _longitude(body: astronomy.Body, time: astronomy.Time) -> tuple[float, float, float]:
    vector = astronomy.GeoVector(body, time, True)
    ecliptic = astronomy.RotateVector(astronomy.Rotation_EQJ_ECT(time), vector)
    sphere = astronomy.SphereFromVector(ecliptic)
    return sphere.lon % 360, sphere.lat, sphere.dist


def _signed_delta(later: float, earlier: float) -> float:
    return (later - earlier + 180) % 360 - 180


def traditional_condition(body: str, sign: str) -> dict[str, Any] | None:
    """Return unscored Ptolemaic domicile/exaltation facts for the seven traditional planets."""

    if body not in TRADITIONAL_DOMICILES:
        return None
    domiciles = TRADITIONAL_DOMICILES[body]
    exaltation = TRADITIONAL_EXALTATIONS[body]
    detriments = tuple(OPPOSITE_SIGN[item] for item in domiciles)
    fall = OPPOSITE_SIGN[exaltation]
    statuses = []
    if sign in domiciles:
        statuses.append("domicile")
    if sign in detriments:
        statuses.append("detriment")
    if sign == exaltation:
        statuses.append("exaltation")
    if sign == fall:
        statuses.append("fall")
    return {
        "fact_id": f"western.traditional_condition.{body}",
        "lineage": "tropical-traditional-condition-v0.3",
        "statuses": statuses,
        "domicile_signs": list(domiciles),
        "detriment_signs": list(detriments),
        "exaltation_sign": exaltation,
        "fall_sign": fall,
        "scoring_applied": False,
        "source_ids": ["SRC-WESTERN-PTOLEMY-001"],
    }


def _position(name: str, body: astronomy.Body, time: astronomy.Time) -> dict[str, Any]:
    longitude, latitude, distance = _longitude(body, time)
    before = _longitude(body, time.AddDays(-0.25))[0]
    after = _longitude(body, time.AddDays(0.25))[0]
    speed = _signed_delta(after, before) / 0.5
    sign_index = int(longitude // 30)
    position = {
        "fact_id": f"western.position.{name}",
        "body": name,
        "longitude_degrees": round(longitude, 8),
        "latitude_degrees": round(latitude, 8),
        "distance_au": round(distance, 10),
        "speed_degrees_per_day": round(speed, 8),
        "retrograde": speed < 0,
        "sign": SIGNS[sign_index],
        "sign_index": sign_index,
        "degree_in_sign": round(longitude % 30, 8),
        "source_ids": ["SRC-WESTERN-ASTRONOMY-ENGINE-001"],
    }
    condition = traditional_condition(name, position["sign"])
    if condition is not None:
        position["traditional_condition"] = condition
    return position


def _cross(
    left: tuple[float, float, float], right: tuple[float, float, float]
) -> tuple[float, float, float]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def _dot(left: tuple[float, float, float], right: tuple[float, float, float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _unit(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    length = math.sqrt(_dot(vector, vector))
    if length < 1e-12:
        raise AstrologyError("angle_undefined", "Ascendant or Midheaven is undefined here.")
    return tuple(value / length for value in vector)


def _ecliptic_longitude_from_eqd(vector: tuple[float, float, float], time: astronomy.Time) -> float:
    eqd = astronomy.Vector(*vector, time)
    ect = astronomy.RotateVector(astronomy.Rotation_EQD_ECT(time), eqd)
    return astronomy.SphereFromVector(ect).lon % 360


def _angles(time: astronomy.Time, longitude: float, latitude: float) -> tuple[float, float]:
    theta = math.radians((astronomy.SiderealTime(time) * 15 + longitude) % 360)
    phi = math.radians(latitude)
    zenith = (math.cos(phi) * math.cos(theta), math.cos(phi) * math.sin(theta), math.sin(phi))
    east = (-math.sin(theta), math.cos(theta), 0.0)
    pole_ect = astronomy.Vector(0.0, 0.0, 1.0, time)
    pole_eqd_vector = astronomy.RotateVector(astronomy.Rotation_ECT_EQD(time), pole_ect)
    pole_eqd = (pole_eqd_vector.x, pole_eqd_vector.y, pole_eqd_vector.z)

    ascendant = _unit(_cross(pole_eqd, zenith))
    if _dot(ascendant, east) < 0:
        ascendant = tuple(-value for value in ascendant)
    midheaven = _unit(_cross(pole_eqd, east))
    if _dot(midheaven, zenith) < 0:
        midheaven = tuple(-value for value in midheaven)
    return (
        _ecliptic_longitude_from_eqd(ascendant, time),
        _ecliptic_longitude_from_eqd(midheaven, time),
    )


def _houses(ascendant: float, system: str) -> list[dict[str, Any]]:
    start = math.floor(ascendant / 30) * 30 if system == "whole_sign" else ascendant
    return [
        {
            "fact_id": f"western.house_cusp.{number:02d}",
            "house": number,
            "longitude_degrees": round((start + (number - 1) * 30) % 360, 8),
            "sign": SIGNS[int(((start + (number - 1) * 30) % 360) // 30)],
            "source_ids": ["SRC-WESTERN-PROJECT-SPEC-001"],
        }
        for number in range(1, 13)
    ]


def _assign_houses(positions: list[dict[str, Any]], cusps: list[dict[str, Any]]) -> None:
    start = cusps[0]["longitude_degrees"]
    for position in positions:
        position["house"] = int(((position["longitude_degrees"] - start) % 360) // 30) + 1


def _aspects(positions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aspects = []
    for left, right in combinations(positions, 2):
        difference = abs(_signed_delta(left["longitude_degrees"], right["longitude_degrees"]))
        matches = [
            (abs(difference - angle), name, angle, orb)
            for name, angle, orb in ASPECTS
            if abs(difference - angle) <= orb
        ]
        if not matches:
            continue
        distance, name, exact_angle, allowed_orb = min(matches)
        aspects.append(
            {
                "fact_id": f"western.aspect.{len(aspects) + 1:03d}",
                "body_a": left["body"],
                "body_b": right["body"],
                "aspect": name,
                "exact_angle_degrees": exact_angle,
                "separation_degrees": round(difference, 8),
                "orb_degrees": round(distance, 8),
                "allowed_orb_degrees": allowed_orb,
                "source_ids": ["SRC-WESTERN-PROJECT-SPEC-001"],
            }
        )
    return aspects


def calculate_chart(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = _normalize(payload)
    time = _astro_time(normalized["utc"])
    positions = [_position(name, body, time) for name, body in BODIES]
    ascendant, midheaven = _angles(time, normalized["longitude"], normalized["latitude"])
    cusps = _houses(ascendant, normalized["house_system"])
    _assign_houses(positions, cusps)
    return {
        "schema_version": "0.3.0",
        "engine": {
            "name": "divination-skills-western-natal",
            "version": "0.3.0",
            "dependencies": {"astronomy-engine": "2.1.19", "tzdata": "2026.3"},
            "source_ids": SOURCE_IDS,
        },
        "raw_input": dict(payload),
        "normalized_input": {
            "local_datetime": normalized["local"].isoformat(),
            "utc_datetime": normalized["utc"].isoformat().replace("+00:00", "Z"),
            "timezone": normalized["timezone"],
            "fold": normalized["fold"],
            "longitude": normalized["longitude"],
            "latitude": normalized["latitude"],
            "house_system": normalized["house_system"],
            "zodiac": "tropical",
            "coordinate_frame": "geocentric_true_ecliptic_of_date",
            "traditional_condition_lineage": "tropical-traditional-condition-v0.3",
        },
        "computed_facts": {
            "positions": positions,
            "angles": {
                "ascendant": {
                    "fact_id": "western.angle.ascendant",
                    "longitude_degrees": round(ascendant, 8),
                    "sign": SIGNS[int(ascendant // 30)],
                    "degree_in_sign": round(ascendant % 30, 8),
                    "source_ids": SOURCE_IDS[:2],
                },
                "midheaven": {
                    "fact_id": "western.angle.midheaven",
                    "longitude_degrees": round(midheaven, 8),
                    "sign": SIGNS[int(midheaven // 30)],
                    "degree_in_sign": round(midheaven % 30, 8),
                    "source_ids": SOURCE_IDS[:2],
                },
            },
            "house_cusps": cusps,
            "aspects": _aspects(positions),
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {"status": "valid", "warnings": []},
    }
