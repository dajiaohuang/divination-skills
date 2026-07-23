"""Calculate a bounded, multi-lineage sidereal Jyotisha chart."""

from __future__ import annotations

import math
from datetime import UTC, timedelta
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
SIGN_LORDS = (
    "mars",
    "venus",
    "mercury",
    "moon",
    "sun",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "saturn",
    "jupiter",
)
NAKSHATRAS = (
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishtha",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
)
VIMSHOTTARI_ORDER = (
    "ketu",
    "venus",
    "sun",
    "moon",
    "mars",
    "rahu",
    "jupiter",
    "saturn",
    "mercury",
)
VIMSHOTTARI_YEARS = {
    "ketu": 7,
    "venus": 20,
    "sun": 6,
    "moon": 10,
    "mars": 7,
    "rahu": 18,
    "jupiter": 16,
    "saturn": 19,
    "mercury": 17,
}
BODIES = (
    ("sun", astronomy.Body.Sun),
    ("moon", astronomy.Body.Moon),
    ("mercury", astronomy.Body.Mercury),
    ("venus", astronomy.Body.Venus),
    ("mars", astronomy.Body.Mars),
    ("jupiter", astronomy.Body.Jupiter),
    ("saturn", astronomy.Body.Saturn),
)
SUPPORTED_LINEAGES = ("parashari", "jaimini", "kp")
NAKSHATRA_SIZE = 360.0 / 27.0
PADA_SIZE = NAKSHATRA_SIZE / 4.0
NAVAMSHA_SIZE = 30.0 / 9.0
COMPUTATIONAL_YEAR_DAYS = 365.2425
SPICA_RA_HOURS_J2000 = 13 + 25 / 60 + 11.579 / 3600
SPICA_DEC_DEGREES_J2000 = -(11 + 9 / 60 + 40.75 / 3600)
SPICA_DISTANCE_LIGHT_YEARS = 250.0

ASTRONOMY_SOURCE = "SRC-WESTERN-ASTRONOMY-ENGINE-001"
PROJECT_SOURCE = "SRC-VEDIC-PROJECT-SPEC-001"
BPHS_SOURCE = "SRC-VEDIC-BPHS-WIKISOURCE-001"
BRIHAT_JATAKA_SOURCE = "SRC-VEDIC-BRIHAT-JATAKA-1885-001"
JAIMINI_SOURCES = (
    "SRC-VEDIC-JAIMINI-RAO-1949-001",
    "SRC-VEDIC-JAIMINI-READER-001",
)
KP_SOURCE = "SRC-VEDIC-KP-INTRO-001"
TIME_SOURCES = ("SRC-TIME-PYTHON-ZONEINFO-001", "SRC-TIME-TZDATA-001")
SOURCE_IDS = [
    ASTRONOMY_SOURCE,
    PROJECT_SOURCE,
    BPHS_SOURCE,
    BRIHAT_JATAKA_SOURCE,
    *JAIMINI_SOURCES,
    KP_SOURCE,
    *TIME_SOURCES,
]

astronomy.DefineStar(
    astronomy.Body.Star1,
    SPICA_RA_HOURS_J2000,
    SPICA_DEC_DEGREES_J2000,
    SPICA_DISTANCE_LIGHT_YEARS,
)


class VedicAstrologyError(ValueError):
    """Public fail-closed calculator error."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _normalize(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "local_datetime",
        "timezone",
        "fold",
        "longitude",
        "latitude",
        "lineages",
        "jaimini_karaka_policy",
        "ayanamsha",
    }
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise VedicAstrologyError(
            "unknown_fields", f"Unknown field(s): {', '.join(unknown)}"
        )
    for field in ("local_datetime", "timezone", "longitude", "latitude"):
        if field not in payload:
            raise VedicAstrologyError(f"missing_{field}", f"{field} is required.")

    longitude = payload["longitude"]
    latitude = payload["latitude"]
    if (
        isinstance(longitude, bool)
        or not isinstance(longitude, (int, float))
        or not -180 <= longitude <= 180
    ):
        raise VedicAstrologyError(
            "invalid_longitude", "longitude must be a number from -180 to 180."
        )
    if (
        isinstance(latitude, bool)
        or not isinstance(latitude, (int, float))
        or not -89 <= latitude <= 89
    ):
        raise VedicAstrologyError(
            "invalid_latitude", "latitude must be a number from -89 to 89."
        )

    raw_lineages = payload.get("lineages", list(SUPPORTED_LINEAGES))
    if (
        not isinstance(raw_lineages, list)
        or not raw_lineages
        or any(item not in SUPPORTED_LINEAGES for item in raw_lineages)
        or len(set(raw_lineages)) != len(raw_lineages)
    ):
        raise VedicAstrologyError(
            "invalid_lineages",
            "lineages must be a non-empty unique list containing parashari, jaimini, or kp.",
        )
    lineages = [item for item in SUPPORTED_LINEAGES if item in raw_lineages]

    ayanamsha = payload.get("ayanamsha", "true_citra")
    if ayanamsha != "true_citra":
        raise VedicAstrologyError(
            "invalid_ayanamsha", "v0.1 supports only ayanamsha=true_citra."
        )
    karaka_policy = payload.get("jaimini_karaka_policy", "seven")
    if karaka_policy not in {"seven", "eight"}:
        raise VedicAstrologyError(
            "invalid_karaka_policy",
            "jaimini_karaka_policy must be seven or eight.",
        )

    try:
        local, fold = localize_strict(
            payload["local_datetime"], payload["timezone"], payload.get("fold")
        )
    except TimeNormalizationError as exc:
        raise VedicAstrologyError(exc.code, exc.message) from exc
    if not 1900 <= local.year <= 2100:
        raise VedicAstrologyError(
            "date_out_of_range", "Supported years are 1900 through 2100."
        )
    return {
        "local": local,
        "utc": local.astimezone(UTC),
        "timezone": payload["timezone"],
        "fold": fold,
        "longitude": float(longitude),
        "latitude": float(latitude),
        "lineages": lineages,
        "ayanamsha": ayanamsha,
        "jaimini_karaka_policy": karaka_policy,
    }


def _astro_time(utc) -> astronomy.Time:
    text = utc.isoformat(timespec="microseconds").replace("+00:00", "Z")
    return astronomy.Time.Parse(text)


def _tropical_longitude(
    body: astronomy.Body, time: astronomy.Time, *, aberration: bool = True
) -> tuple[float, float, float]:
    vector = astronomy.GeoVector(body, time, aberration)
    ecliptic = astronomy.RotateVector(astronomy.Rotation_EQJ_ECT(time), vector)
    sphere = astronomy.SphereFromVector(ecliptic)
    return sphere.lon % 360, sphere.lat, sphere.dist


def _signed_delta(later: float, earlier: float) -> float:
    return (later - earlier + 180) % 360 - 180


def _true_citra_ayanamsha(time: astronomy.Time) -> tuple[float, float]:
    # A sidereal origin is a precessing stellar reference, not an annually
    # aberrated apparent position. Planetary positions remain apparent below.
    spica_longitude, _, _ = _tropical_longitude(
        astronomy.Body.Star1, time, aberration=False
    )
    return (spica_longitude - 180.0) % 360.0, spica_longitude


def _mean_node_tropical(time: astronomy.Time) -> float:
    centuries = time.tt / 36525.0
    return (
        125.04455501
        - 1934.1361849 * centuries
        + 0.0020762 * centuries**2
        + centuries**3 / 467410.0
        - centuries**4 / 60616000.0
    ) % 360.0


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
        raise VedicAstrologyError(
            "angle_undefined", "Ascendant is undefined for this input."
        )
    return tuple(value / length for value in vector)


def _ecliptic_longitude_from_eqd(
    vector: tuple[float, float, float], time: astronomy.Time
) -> float:
    eqd = astronomy.Vector(*vector, time)
    ect = astronomy.RotateVector(astronomy.Rotation_EQD_ECT(time), eqd)
    return astronomy.SphereFromVector(ect).lon % 360


def _tropical_ascendant(
    time: astronomy.Time, longitude: float, latitude: float
) -> float:
    theta = math.radians((astronomy.SiderealTime(time) * 15 + longitude) % 360)
    phi = math.radians(latitude)
    zenith = (
        math.cos(phi) * math.cos(theta),
        math.cos(phi) * math.sin(theta),
        math.sin(phi),
    )
    east = (-math.sin(theta), math.cos(theta), 0.0)
    pole_ect = astronomy.Vector(0.0, 0.0, 1.0, time)
    pole_eqd_vector = astronomy.RotateVector(
        astronomy.Rotation_ECT_EQD(time), pole_ect
    )
    pole_eqd = (pole_eqd_vector.x, pole_eqd_vector.y, pole_eqd_vector.z)
    ascendant = _unit(_cross(pole_eqd, zenith))
    if _dot(ascendant, east) < 0:
        ascendant = tuple(-value for value in ascendant)
    return _ecliptic_longitude_from_eqd(ascendant, time)


def _nakshatra(longitude: float) -> dict[str, Any]:
    index = min(int(longitude / NAKSHATRA_SIZE), 26)
    within = longitude - index * NAKSHATRA_SIZE
    lord = VIMSHOTTARI_ORDER[index % 9]
    return {
        "fact_id": f"vedic.nakshatra.{index + 1:02d}",
        "index": index,
        "number": index + 1,
        "name": NAKSHATRAS[index],
        "lord": lord,
        "pada": min(int(within / PADA_SIZE), 3) + 1,
        "degrees_within": round(within, 8),
        "fraction_elapsed": round(within / NAKSHATRA_SIZE, 12),
        "rule_ids": ["VEDIC-CAL-NAKSHATRA-001"],
        "source_ids": [BPHS_SOURCE, PROJECT_SOURCE],
    }


def _sidereal_identity(longitude: float) -> dict[str, Any]:
    sign_index = min(int(longitude // 30), 11)
    return {
        "longitude_degrees": round(longitude, 8),
        "sign": SIGNS[sign_index],
        "sign_index": sign_index,
        "degree_in_sign": round(longitude % 30, 8),
        "sign_lord": SIGN_LORDS[sign_index],
    }


def _position(
    name: str,
    body: astronomy.Body,
    time: astronomy.Time,
    ayanamsha: float,
    ascendant_sign: int,
) -> dict[str, Any]:
    tropical, latitude, distance = _tropical_longitude(body, time)
    before = _tropical_longitude(body, time.AddDays(-0.25))[0]
    after = _tropical_longitude(body, time.AddDays(0.25))[0]
    speed = _signed_delta(after, before) / 0.5
    sidereal = (tropical - ayanamsha) % 360
    identity = _sidereal_identity(sidereal)
    return {
        "fact_id": f"vedic.position.{name}",
        "body": name,
        "tropical_longitude_degrees": round(tropical, 8),
        **identity,
        "latitude_degrees": round(latitude, 8),
        "distance_au": round(distance, 10),
        "speed_degrees_per_day": round(speed, 8),
        "retrograde": speed < 0,
        "house": (identity["sign_index"] - ascendant_sign) % 12 + 1,
        "nakshatra": _nakshatra(sidereal),
        "rule_ids": ["VEDIC-CAL-GRAHA-001", "VEDIC-CAL-SIDEREAL-001"],
        "source_ids": [ASTRONOMY_SOURCE, PROJECT_SOURCE],
    }


def _node_position(
    name: str,
    tropical: float,
    speed: float,
    ayanamsha: float,
    ascendant_sign: int,
) -> dict[str, Any]:
    sidereal = (tropical - ayanamsha) % 360
    identity = _sidereal_identity(sidereal)
    return {
        "fact_id": f"vedic.position.{name}",
        "body": name,
        "node_policy": "mean",
        "tropical_longitude_degrees": round(tropical, 8),
        **identity,
        "latitude_degrees": 0.0,
        "speed_degrees_per_day": round(speed, 8),
        "retrograde": speed < 0,
        "house": (identity["sign_index"] - ascendant_sign) % 12 + 1,
        "nakshatra": _nakshatra(sidereal),
        "rule_ids": [
            "VEDIC-CAL-MEAN-NODE-001",
            "VEDIC-CAL-SIDEREAL-001",
        ],
        "source_ids": [PROJECT_SOURCE],
    }


def _navamsha(longitude: float, body: str) -> dict[str, Any]:
    sign_index = int(longitude // 30)
    division = min(int((longitude % 30) / NAVAMSHA_SIZE), 8)
    if sign_index in {0, 3, 6, 9}:
        start = sign_index
        sign_class = "movable"
    elif sign_index in {1, 4, 7, 10}:
        start = (sign_index + 8) % 12
        sign_class = "fixed"
    else:
        start = (sign_index + 4) % 12
        sign_class = "dual"
    target = (start + division) % 12
    return {
        "fact_id": f"vedic.parashari.navamsha.{body}",
        "body": body,
        "source_sign": SIGNS[sign_index],
        "source_sign_class": sign_class,
        "division": division + 1,
        "sign": SIGNS[target],
        "sign_index": target,
        "rule_ids": ["VEDIC-PARASHARI-NAVAMSHA-001"],
        "source_ids": [BPHS_SOURCE, PROJECT_SOURCE],
    }


def _vimshottari(moon: dict[str, Any], birth_utc) -> dict[str, Any]:
    nakshatra = moon["nakshatra"]
    current_lord = nakshatra["lord"]
    current_index = VIMSHOTTARI_ORDER.index(current_lord)
    fraction_elapsed = nakshatra["fraction_elapsed"]
    elapsed_years = VIMSHOTTARI_YEARS[current_lord] * fraction_elapsed
    start = birth_utc - timedelta(days=elapsed_years * COMPUTATIONAL_YEAR_DAYS)
    periods = []
    cursor = start
    for offset in range(9):
        lord = VIMSHOTTARI_ORDER[(current_index + offset) % 9]
        end = cursor + timedelta(
            days=VIMSHOTTARI_YEARS[lord] * COMPUTATIONAL_YEAR_DAYS
        )
        periods.append(
            {
                "fact_id": f"vedic.parashari.vimshottari.{offset + 1:02d}",
                "lord": lord,
                "years": VIMSHOTTARI_YEARS[lord],
                "start_utc": cursor.isoformat().replace("+00:00", "Z"),
                "end_utc": end.isoformat().replace("+00:00", "Z"),
                "active_at_birth": offset == 0,
                "rule_ids": ["VEDIC-PARASHARI-VIMSHOTTARI-001"],
                "source_ids": [BPHS_SOURCE, PROJECT_SOURCE],
            }
        )
        cursor = end
    return {
        "fact_id": "vedic.parashari.vimshottari",
        "year_length_days": COMPUTATIONAL_YEAR_DAYS,
        "birth_nakshatra": nakshatra["name"],
        "birth_lord": current_lord,
        "elapsed_years_at_birth": round(elapsed_years, 10),
        "balance_years_at_birth": round(
            VIMSHOTTARI_YEARS[current_lord] - elapsed_years, 10
        ),
        "periods": periods,
        "rule_ids": ["VEDIC-PARASHARI-VIMSHOTTARI-001"],
        "source_ids": [BPHS_SOURCE, PROJECT_SOURCE],
    }


def _parashari(
    positions: list[dict[str, Any]], lagna: dict[str, Any], birth_utc
) -> dict[str, Any]:
    items = [lagna, *positions]
    moon = next(item for item in positions if item["body"] == "moon")
    return {
        "fact_id": "vedic.lineage.parashari",
        "lineage": "parashari-structural-v0.1",
        "house_policy": "whole_sign_from_sidereal_lagna",
        "navamsha": [
            _navamsha(item["longitude_degrees"], item["body"]) for item in items
        ],
        "vimshottari": _vimshottari(moon, birth_utc),
        "rule_ids": [
            "VEDIC-PARASHARI-WHOLE-SIGN-001",
            "VEDIC-PARASHARI-NAVAMSHA-001",
            "VEDIC-PARASHARI-VIMSHOTTARI-001",
        ],
        "source_ids": [BPHS_SOURCE, BRIHAT_JATAKA_SOURCE, PROJECT_SOURCE],
    }


def _karakas(
    positions: list[dict[str, Any]], policy: str
) -> list[dict[str, Any]]:
    candidates = [
        item
        for item in positions
        if item["body"]
        in {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    ]
    if policy == "eight":
        candidates.append(next(item for item in positions if item["body"] == "rahu"))
        labels = ("AK", "AmK", "BK", "MK", "PiK", "PK", "GK", "DK")
        rule_id = "VEDIC-JAIMINI-KARAKA-EIGHT-001"
    else:
        labels = ("AK", "AmK", "BK", "MK", "PK", "GK", "DK")
        rule_id = "VEDIC-JAIMINI-KARAKA-SEVEN-001"

    ranked: list[tuple[float, dict[str, Any]]] = []
    for item in candidates:
        degree = item["longitude_degrees"] % 30
        effective = 30.0 - degree if item["body"] == "rahu" else degree
        ranked.append((effective, item))
    ranked.sort(key=lambda pair: pair[0], reverse=True)
    for left, right in zip(ranked, ranked[1:], strict=False):
        if abs(left[0] - right[0]) < 1e-9:
            raise VedicAstrologyError(
                "karaka_tie",
                "Jaimini chara-karaka effective degrees are tied; select or define a tie policy.",
            )
    return [
        {
            "fact_id": f"vedic.jaimini.karaka.{label.lower()}",
            "rank": rank,
            "karaka": label,
            "body": item["body"],
            "effective_degree_in_sign": round(effective, 8),
            "rahu_reversal_applied": item["body"] == "rahu",
            "rule_ids": [rule_id],
            "source_ids": [*JAIMINI_SOURCES, PROJECT_SOURCE],
        }
        for rank, (label, (effective, item)) in enumerate(
            zip(labels, ranked, strict=True), start=1
        )
    ]


def _rashi_drishti() -> list[dict[str, Any]]:
    movable = {0, 3, 6, 9}
    fixed = {1, 4, 7, 10}
    dual = {2, 5, 8, 11}
    relations = []
    for source in range(12):
        if source in movable:
            targets = [
                target
                for target in sorted(fixed)
                if min((target - source) % 12, (source - target) % 12) != 1
            ]
            sign_class = "movable"
        elif source in fixed:
            targets = [
                target
                for target in sorted(movable)
                if min((target - source) % 12, (source - target) % 12) != 1
            ]
            sign_class = "fixed"
        else:
            targets = sorted(dual - {source})
            sign_class = "dual"
        relations.append(
            {
                "fact_id": f"vedic.jaimini.rashi_drishti.{source + 1:02d}",
                "source_sign": SIGNS[source],
                "source_sign_index": source,
                "source_class": sign_class,
                "target_signs": [SIGNS[target] for target in targets],
                "target_sign_indices": targets,
                "rule_ids": ["VEDIC-JAIMINI-RASHI-DRISHTI-001"],
                "source_ids": [*JAIMINI_SOURCES, PROJECT_SOURCE],
            }
        )
    return relations


def _arudha_lagna(
    positions: list[dict[str, Any]], lagna: dict[str, Any]
) -> dict[str, Any]:
    source = lagna["sign_index"]
    lord = SIGN_LORDS[source]
    lord_position = next(item for item in positions if item["body"] == lord)
    lord_sign = lord_position["sign_index"]
    distance = (lord_sign - source) % 12
    ordinary = (lord_sign + distance) % 12
    exception = ordinary in {source, (source + 6) % 12}
    result = (lord_sign + 9) % 12 if exception else ordinary
    return {
        "fact_id": "vedic.jaimini.arudha_lagna",
        "source_sign": SIGNS[source],
        "source_sign_index": source,
        "lagna_lord": lord,
        "lord_sign": SIGNS[lord_sign],
        "lord_sign_index": lord_sign,
        "distance_steps": distance,
        "ordinary_result_sign": SIGNS[ordinary],
        "exception_applied": exception,
        "exception_policy": "tenth_from_lord_when_same_or_seventh",
        "sign": SIGNS[result],
        "sign_index": result,
        "rule_ids": ["VEDIC-JAIMINI-ARUDHA-001"],
        "source_ids": [*JAIMINI_SOURCES, PROJECT_SOURCE],
    }


def _jaimini(
    positions: list[dict[str, Any]],
    lagna: dict[str, Any],
    karaka_policy: str,
) -> dict[str, Any]:
    return {
        "fact_id": "vedic.lineage.jaimini",
        "lineage": "jaimini-structural-v0.1",
        "karaka_policy": karaka_policy,
        "chara_karakas": _karakas(positions, karaka_policy),
        "rashi_drishti": _rashi_drishti(),
        "arudha_lagna": _arudha_lagna(positions, lagna),
        "rule_ids": [
            (
                "VEDIC-JAIMINI-KARAKA-SEVEN-001"
                if karaka_policy == "seven"
                else "VEDIC-JAIMINI-KARAKA-EIGHT-001"
            ),
            "VEDIC-JAIMINI-RASHI-DRISHTI-001",
            "VEDIC-JAIMINI-ARUDHA-001",
        ],
        "source_ids": [*JAIMINI_SOURCES, PROJECT_SOURCE],
    }


def _kp_stellar_item(item: dict[str, Any]) -> dict[str, Any]:
    longitude = item["longitude_degrees"]
    nak_index = min(int(longitude / NAKSHATRA_SIZE), 26)
    nak_start = nak_index * NAKSHATRA_SIZE
    within = longitude - nak_start
    star_lord = VIMSHOTTARI_ORDER[nak_index % 9]
    start_index = VIMSHOTTARI_ORDER.index(star_lord)
    sequence = [
        VIMSHOTTARI_ORDER[(start_index + offset) % 9] for offset in range(9)
    ]
    cursor = 0.0
    chosen = sequence[-1]
    chosen_start = 0.0
    chosen_end = NAKSHATRA_SIZE
    for lord in sequence:
        span = NAKSHATRA_SIZE * VIMSHOTTARI_YEARS[lord] / 120.0
        end = cursor + span
        if within < end or math.isclose(end, NAKSHATRA_SIZE):
            chosen = lord
            chosen_start = cursor
            chosen_end = end
            break
        cursor = end
    return {
        "fact_id": f"vedic.kp.stellar.{item['body']}",
        "body": item["body"],
        "longitude_degrees": item["longitude_degrees"],
        "sign": item["sign"],
        "sign_lord": item["sign_lord"],
        "nakshatra": NAKSHATRAS[nak_index],
        "star_lord": star_lord,
        "sub_lord": chosen,
        "sub_start_longitude": round(nak_start + chosen_start, 8),
        "sub_end_longitude": round(nak_start + chosen_end, 8),
        "boundary_policy": "half_open",
        "rule_ids": ["VEDIC-KP-SUBLORD-001"],
        "source_ids": [KP_SOURCE, PROJECT_SOURCE],
    }


def _kp(positions: list[dict[str, Any]], lagna: dict[str, Any]) -> dict[str, Any]:
    return {
        "fact_id": "vedic.lineage.kp",
        "lineage": "kp-stellar-v0.1",
        "completeness": "stellar_identity_only",
        "stellar_identities": [
            _kp_stellar_item(item) for item in [lagna, *positions]
        ],
        "unsupported": [
            "placidus_cusps",
            "cusp_sub_lords",
            "ruling_planets",
            "significator_ranking",
            "horary_number_chart",
            "event_judgment",
        ],
        "rule_ids": ["VEDIC-KP-SUBLORD-001", "VEDIC-BOUNDARY-001"],
        "source_ids": [KP_SOURCE, PROJECT_SOURCE],
    }


def calculate_chart(payload: dict[str, Any]) -> dict[str, Any]:
    """Return an auditable sidereal chart with only requested lineages."""

    normalized = _normalize(payload)
    time = _astro_time(normalized["utc"])
    ayanamsha, spica_tropical = _true_citra_ayanamsha(time)
    tropical_ascendant = _tropical_ascendant(
        time, normalized["longitude"], normalized["latitude"]
    )
    sidereal_ascendant = (tropical_ascendant - ayanamsha) % 360
    lagna_identity = _sidereal_identity(sidereal_ascendant)
    lagna = {
        "fact_id": "vedic.angle.lagna",
        "body": "lagna",
        "tropical_longitude_degrees": round(tropical_ascendant, 8),
        **lagna_identity,
        "house": 1,
        "nakshatra": _nakshatra(sidereal_ascendant),
        "rule_ids": ["VEDIC-CAL-LAGNA-001", "VEDIC-CAL-SIDEREAL-001"],
        "source_ids": [ASTRONOMY_SOURCE, PROJECT_SOURCE],
    }
    positions = [
        _position(
            name,
            body,
            time,
            ayanamsha,
            lagna_identity["sign_index"],
        )
        for name, body in BODIES
    ]
    mean_rahu = _mean_node_tropical(time)
    rahu_before = _mean_node_tropical(time.AddDays(-0.25))
    rahu_after = _mean_node_tropical(time.AddDays(0.25))
    node_speed = _signed_delta(rahu_after, rahu_before) / 0.5
    positions += [
        _node_position(
            "rahu",
            mean_rahu,
            node_speed,
            ayanamsha,
            lagna_identity["sign_index"],
        ),
        _node_position(
            "ketu",
            (mean_rahu + 180.0) % 360,
            node_speed,
            ayanamsha,
            lagna_identity["sign_index"],
        ),
    ]

    lineages: dict[str, Any] = {}
    if "parashari" in normalized["lineages"]:
        lineages["parashari"] = _parashari(positions, lagna, normalized["utc"])
    if "jaimini" in normalized["lineages"]:
        lineages["jaimini"] = _jaimini(
            positions, lagna, normalized["jaimini_karaka_policy"]
        )
    if "kp" in normalized["lineages"]:
        lineages["kp"] = _kp(positions, lagna)

    warnings = [
        {
            "code": "spica_proper_motion_not_applied",
            "message": "The true-Citra anchor uses declared J2000 Spica coordinates.",
        },
        {
            "code": "mean_nodes",
            "message": "Rahu and Ketu use the mean-node policy.",
        },
        {
            "code": "structural_only",
            "message": "No predictive or remedial interpretation is produced.",
        },
    ]
    if "kp" in normalized["lineages"]:
        warnings.append(
            {
                "code": "kp_stellar_only",
                "message": "KP output is a stellar identity layer, not a complete KP chart.",
            }
        )

    return {
        "schema_version": "0.1.0",
        "engine": {
            "name": "divination-skills-vedic-multilineage",
            "version": "0.1.0",
            "dependencies": {
                "astronomy-engine": "2.1.19",
                "tzdata": "2026.3",
            },
            "repository_dependencies": [],
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
            "ayanamsha": normalized["ayanamsha"],
            "lineages": normalized["lineages"],
            "jaimini_karaka_policy": normalized["jaimini_karaka_policy"],
            "coordinate_frame": "geocentric_true_ecliptic_of_date",
            "node_policy": "mean",
        },
        "computed_facts": {
            "astronomy": {
                "fact_id": "vedic.astronomy.baseline",
                "ayanamsha": {
                    "name": "true_citra",
                    "degrees": round(ayanamsha, 8),
                    "anchor_star": "Spica/Chitra",
                    "anchor_tropical_longitude_degrees": round(
                        spica_tropical, 8
                    ),
                    "anchor_sidereal_longitude_degrees": 180.0,
                    "spica_ra_hours_j2000": round(SPICA_RA_HOURS_J2000, 10),
                    "spica_dec_degrees_j2000": round(
                        SPICA_DEC_DEGREES_J2000, 10
                    ),
                    "proper_motion_applied": False,
                    "annual_aberration_applied": False,
                    "rule_ids": ["VEDIC-CAL-SIDEREAL-001"],
                    "source_ids": [ASTRONOMY_SOURCE, PROJECT_SOURCE],
                },
                "rule_ids": [
                    "VEDIC-CAL-GRAHA-001",
                    "VEDIC-CAL-MEAN-NODE-001",
                    "VEDIC-CAL-SIDEREAL-001",
                ],
                "source_ids": [ASTRONOMY_SOURCE, PROJECT_SOURCE],
            },
            "sidereal_chart": {
                "fact_id": "vedic.sidereal_chart",
                "lagna": lagna,
                "positions": positions,
                "house_policy": "whole_sign_from_sidereal_lagna",
                "rule_ids": [
                    "VEDIC-CAL-GRAHA-001",
                    "VEDIC-CAL-LAGNA-001",
                    "VEDIC-PARASHARI-WHOLE-SIGN-001",
                ],
                "source_ids": [ASTRONOMY_SOURCE, BPHS_SOURCE, PROJECT_SOURCE],
            },
            "lineages": lineages,
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {
            "status": "valid_with_warnings",
            "warnings": warnings,
        },
        "trace": [
            {
                "stage": "time_normalization",
                "rule_ids": ["VEDIC-CAL-TIME-001"],
                "source_ids": [*TIME_SOURCES, PROJECT_SOURCE],
            },
            {
                "stage": "tropical_astronomy",
                "rule_ids": ["VEDIC-CAL-GRAHA-001", "VEDIC-CAL-LAGNA-001"],
                "source_ids": [ASTRONOMY_SOURCE, PROJECT_SOURCE],
            },
            {
                "stage": "sidereal_conversion",
                "rule_ids": ["VEDIC-CAL-SIDEREAL-001"],
                "source_ids": [ASTRONOMY_SOURCE, PROJECT_SOURCE],
            },
            {
                "stage": "lineage_modules",
                "lineages": normalized["lineages"],
                "rule_ids": ["VEDIC-LINEAGE-ISOLATION-001"],
                "source_ids": [PROJECT_SOURCE],
            },
        ],
    }
