"""Run independent birth-based systems and build a bounded structural crosswalk."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from systems.bazi.calculator.engine import CalculationError
from systems.bazi.calculator.engine import calculate_chart as calculate_bazi
from systems.numerology.calculator.engine import (
    NumerologyError,
)
from systems.numerology.calculator.engine import (
    calculate_profile as calculate_numerology,
)
from systems.vedic_astrology.calculator.engine import (
    VedicAstrologyError,
)
from systems.vedic_astrology.calculator.engine import (
    calculate_chart as calculate_vedic,
)
from systems.western_astrology.calculator.engine import (
    AstrologyError,
)
from systems.western_astrology.calculator.engine import (
    calculate_chart as calculate_western,
)
from systems.ziwei.engine import ZiweiError
from systems.ziwei.engine import calculate as calculate_ziwei

ENGINE_NAME = "divination-skills-multi-natal"
ENGINE_VERSION = "0.1.0"
SCHEMA_VERSION = "0.1.0"
LINEAGE = "cross-system-structural-bridge-v0.1"
PROJECT_SOURCE = "SRC-MULTI-NATAL-PROJECT-SPEC-001"
CORE_SYSTEMS = ("bazi", "western-astrology", "ziwei", "vedic-astrology")
DEFAULT_POLICIES: dict[str, Any] = {
    "east_asian_time_basis": "civil",
    "bazi_day_boundary": "midnight",
    "bazi_luck_cycle_direction": None,
    "western_house_system": "whole_sign",
    "ziwei_year_boundary": "lunar_new_year",
    "ziwei_late_zi_policy": "current_day",
    "ziwei_leap_month_policy": "preserve",
    "vedic_lineages": ["parashari", "jaimini", "kp"],
    "jaimini_karaka_policy": "seven",
}


class NatalSynthesisError(ValueError):
    """Public fail-closed orchestration error."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _number(value: Any, *, field: str, minimum: float, maximum: float) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not minimum <= value <= maximum
    ):
        raise NatalSynthesisError(
            f"invalid_{field}",
            f"{field} must be a number from {minimum:g} to {maximum:g}.",
        )
    return float(value)


def _normalize(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise NatalSynthesisError("invalid_input", "Input must be a JSON object.")
    allowed = {
        "birth_date",
        "birth_time",
        "birthplace",
        "calculation_gender",
        "fold",
        "policies",
        "numerology",
    }
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise NatalSynthesisError(
            "unknown_fields", f"Unknown field(s): {', '.join(unknown)}"
        )
    missing = sorted(
        {"birth_date", "birth_time", "birthplace", "calculation_gender"} - set(payload)
    )
    if missing:
        raise NatalSynthesisError(
            "missing_fields", f"Missing field(s): {', '.join(missing)}"
        )

    try:
        local = datetime.fromisoformat(
            f"{payload['birth_date']}T{payload['birth_time']}"
        )
    except (TypeError, ValueError) as exc:
        raise NatalSynthesisError(
            "invalid_birth_datetime",
            "birth_date and birth_time must form an ISO local date and time.",
        ) from exc
    if local.tzinfo is not None:
        raise NatalSynthesisError(
            "offset_not_allowed",
            "Birth time must not contain a UTC offset; use birthplace.timezone.",
        )
    if not 1900 <= local.year <= 2099:
        raise NatalSynthesisError(
            "date_out_of_range", "The shared supported years are 1900 through 2099."
        )
    local_datetime = local.isoformat(timespec="seconds")

    birthplace = payload["birthplace"]
    if not isinstance(birthplace, dict):
        raise NatalSynthesisError("invalid_birthplace", "birthplace must be an object.")
    place_allowed = {
        "name",
        "timezone",
        "longitude",
        "latitude",
        "resolution_source",
        "source_url",
    }
    place_unknown = sorted(set(birthplace) - place_allowed)
    if place_unknown:
        raise NatalSynthesisError(
            "unknown_birthplace_fields",
            f"Unknown birthplace field(s): {', '.join(place_unknown)}",
        )
    place_missing = sorted(
        {"name", "timezone", "longitude", "latitude", "resolution_source"}
        - set(birthplace)
    )
    if place_missing:
        raise NatalSynthesisError(
            "unresolved_birthplace",
            (
                "Birthplace must include a confirmed name, IANA timezone, longitude, "
                f"latitude, and resolution_source; missing: {', '.join(place_missing)}."
            ),
        )
    if not isinstance(birthplace["name"], str) or not birthplace["name"].strip():
        raise NatalSynthesisError("invalid_place_name", "birthplace.name must be non-empty.")
    if not isinstance(birthplace["timezone"], str) or not birthplace["timezone"].strip():
        raise NatalSynthesisError(
            "invalid_timezone", "birthplace.timezone must be a non-empty IANA name."
        )
    resolution_source = birthplace["resolution_source"]
    if resolution_source not in {"user_confirmed", "gazetteer", "geocoder"}:
        raise NatalSynthesisError(
            "invalid_resolution_source",
            "resolution_source must be user_confirmed, gazetteer, or geocoder.",
        )
    source_url = birthplace.get("source_url")
    if source_url is not None and (
        not isinstance(source_url, str)
        or not source_url.startswith(("https://", "http://"))
    ):
        raise NatalSynthesisError(
            "invalid_source_url", "birthplace.source_url must be an HTTP(S) URL."
        )
    normalized_place = {
        "name": birthplace["name"].strip(),
        "timezone": birthplace["timezone"].strip(),
        "longitude": _number(
            birthplace["longitude"],
            field="longitude",
            minimum=-180,
            maximum=180,
        ),
        "latitude": _number(
            birthplace["latitude"],
            field="latitude",
            minimum=-89,
            maximum=89,
        ),
        "resolution_source": resolution_source,
        "source_url": source_url,
    }

    gender = payload["calculation_gender"]
    if gender not in {"male", "female"}:
        raise NatalSynthesisError(
            "invalid_calculation_gender",
            "calculation_gender must be explicitly supplied as male or female for Ziwei.",
        )
    fold = payload.get("fold")
    if fold is not None and (
        isinstance(fold, bool) or not isinstance(fold, int) or fold not in {0, 1}
    ):
        raise NatalSynthesisError("invalid_fold", "fold must be 0 or 1.")

    raw_policies = payload.get("policies", {})
    if not isinstance(raw_policies, dict):
        raise NatalSynthesisError("invalid_policies", "policies must be an object.")
    policy_unknown = sorted(set(raw_policies) - set(DEFAULT_POLICIES))
    if policy_unknown:
        raise NatalSynthesisError(
            "unknown_policy_fields",
            f"Unknown policy field(s): {', '.join(policy_unknown)}",
        )
    policies = deepcopy(DEFAULT_POLICIES)
    policies.update(raw_policies)
    allowed_policies = {
        "east_asian_time_basis": {"civil", "apparent_solar"},
        "bazi_day_boundary": {"midnight", "zi_initial"},
        "western_house_system": {"whole_sign", "equal"},
        "ziwei_year_boundary": {"lunar_new_year", "spring_commences"},
        "ziwei_late_zi_policy": {"current_day", "next_day"},
        "ziwei_leap_month_policy": {"preserve", "previous_month", "next_month", "split_after_15"},
        "jaimini_karaka_policy": {"seven", "eight"},
    }
    for field, accepted in allowed_policies.items():
        if policies[field] not in accepted:
            raise NatalSynthesisError(
                f"invalid_{field}",
                f"{field} must be one of: {', '.join(sorted(accepted))}.",
            )
    if policies["bazi_luck_cycle_direction"] not in {None, "forward", "reverse"}:
        raise NatalSynthesisError(
            "invalid_bazi_luck_cycle_direction",
            "bazi_luck_cycle_direction must be forward, reverse, or null.",
        )
    lineages = policies["vedic_lineages"]
    if (
        not isinstance(lineages, list)
        or not lineages
        or len(lineages) != len(set(lineages))
        or any(item not in {"parashari", "jaimini", "kp"} for item in lineages)
    ):
        raise NatalSynthesisError(
            "invalid_vedic_lineages",
            "vedic_lineages must be a non-empty unique subset of parashari, jaimini, kp.",
        )
    policies["vedic_lineages"] = [
        item for item in ("parashari", "jaimini", "kp") if item in lineages
    ]

    numerology = payload.get("numerology")
    if numerology is not None:
        if not isinstance(numerology, dict):
            raise NatalSynthesisError("invalid_numerology", "numerology must be an object.")
        numeral_allowed = {"name", "transliteration", "mappings"}
        numeral_unknown = sorted(set(numerology) - numeral_allowed)
        if numeral_unknown:
            raise NatalSynthesisError(
                "unknown_numerology_fields",
                f"Unknown numerology field(s): {', '.join(numeral_unknown)}",
            )
        if not isinstance(numerology.get("name"), str) or not numerology["name"].strip():
            raise NatalSynthesisError(
                "numerology_name_required",
                "numerology.name is required when numerology is selected.",
            )
        mappings = numerology.get("mappings", ["pythagorean", "chaldean"])
        if (
            not isinstance(mappings, list)
            or not mappings
            or len(mappings) != len(set(mappings))
            or any(item not in {"pythagorean", "chaldean"} for item in mappings)
        ):
            raise NatalSynthesisError(
                "invalid_numerology_mappings",
                "numerology.mappings must contain pythagorean and/or chaldean once.",
            )
        numerology = {
            "name": numerology["name"],
            "transliteration": numerology.get("transliteration"),
            "mappings": [
                item for item in ("pythagorean", "chaldean") if item in mappings
            ],
        }

    return {
        "birth_date": local.date().isoformat(),
        "birth_time": local.time().isoformat(timespec="seconds"),
        "local_datetime": local_datetime,
        "birthplace": normalized_place,
        "calculation_gender": gender,
        "fold": fold,
        "policies": policies,
        "numerology": numerology,
    }


def _run_native_charts(normalized: dict[str, Any]) -> dict[str, Any]:
    place = normalized["birthplace"]
    common = {
        "local_datetime": normalized["local_datetime"],
        "timezone": place["timezone"],
        "longitude": place["longitude"],
        "latitude": place["latitude"],
    }
    if normalized["fold"] is not None:
        common["fold"] = normalized["fold"]
    policies = normalized["policies"]
    bazi_input = {
        **common,
        "day_boundary": policies["bazi_day_boundary"],
        "time_basis": policies["east_asian_time_basis"],
    }
    if policies["bazi_luck_cycle_direction"] is not None:
        bazi_input["luck_cycle_direction"] = policies["bazi_luck_cycle_direction"]
    western_input = {
        **common,
        "house_system": policies["western_house_system"],
    }
    ziwei_input = {
        **common,
        "calendar_type": "solar",
        "calculation_gender": normalized["calculation_gender"],
        "year_boundary": policies["ziwei_year_boundary"],
        "late_zi_policy": policies["ziwei_late_zi_policy"],
        "leap_month_policy": policies["ziwei_leap_month_policy"],
        "time_basis": policies["east_asian_time_basis"],
    }
    vedic_input = {
        **common,
        "lineages": policies["vedic_lineages"],
        "jaimini_karaka_policy": policies["jaimini_karaka_policy"],
        "ayanamsha": "true_citra",
    }
    calculators = (
        ("bazi", calculate_bazi, bazi_input),
        ("western-astrology", calculate_western, western_input),
        ("ziwei", calculate_ziwei, ziwei_input),
        ("vedic-astrology", calculate_vedic, vedic_input),
    )
    charts: dict[str, Any] = {}
    for system, calculator, native_input in calculators:
        try:
            charts[system] = calculator(native_input)
        except (CalculationError, AstrologyError, ZiweiError, VedicAstrologyError) as exc:
            code = getattr(exc, "code", "calculation_failed")
            raise NatalSynthesisError(
                f"{system}.{code}", f"{system} calculation failed: {exc}"
            ) from exc

    if normalized["numerology"] is not None:
        profiles = {}
        for mapping in normalized["numerology"]["mappings"]:
            numeral_input = {
                "name": normalized["numerology"]["name"],
                "birth_date": normalized["birth_date"],
                "mapping": mapping,
            }
            transliteration = normalized["numerology"]["transliteration"]
            if transliteration is not None:
                numeral_input["transliteration"] = transliteration
            try:
                profiles[mapping] = calculate_numerology(numeral_input)
            except NumerologyError as exc:
                raise NatalSynthesisError(
                    f"numerology.{exc.code}", f"numerology calculation failed: {exc}"
                ) from exc
        charts["numerology"] = profiles
    return charts


def _position(chart: dict[str, Any], body: str) -> dict[str, Any]:
    facts = chart["computed_facts"]
    positions = facts.get("positions")
    if positions is None:
        positions = facts["sidereal_chart"]["positions"]
    return next(
        item for item in positions if item["body"] == body
    )


def _palace(chart: dict[str, Any], name: str) -> dict[str, Any]:
    return next(
        item for item in chart["computed_facts"]["palaces"] if item["name"] == name
    )


def _circular_difference(left: float, right: float) -> float:
    return abs((left - right + 180.0) % 360.0 - 180.0)


def _cross_checks(charts: dict[str, Any]) -> dict[str, Any]:
    utc_values = {
        system: charts[system]["normalized_input"]["utc_datetime"]
        for system in CORE_SYSTEMS
    }
    utc_check = {
        "fact_id": "multi-natal.cross-check.utc",
        "utc_by_system": utc_values,
        "all_equal": len(set(utc_values.values())) == 1,
        "rule_ids": ["MULTI-NATAL-ROUTING-001"],
        "source_ids": [PROJECT_SOURCE],
    }

    western = charts["western-astrology"]
    vedic = charts["vedic-astrology"]
    comparisons = []
    for body in ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"):
        western_position = _position(western, body)
        vedic_position = _position(vedic, body)
        comparisons.append(
            {
                "body": body,
                "western_fact_id": western_position["fact_id"],
                "vedic_fact_id": vedic_position["fact_id"],
                "western_tropical_longitude": western_position["longitude_degrees"],
                "vedic_retained_tropical_longitude": vedic_position[
                    "tropical_longitude_degrees"
                ],
                "absolute_difference_degrees": round(
                    _circular_difference(
                        western_position["longitude_degrees"],
                        vedic_position["tropical_longitude_degrees"],
                    ),
                    10,
                ),
            }
        )
    western_asc = western["computed_facts"]["angles"]["ascendant"]
    vedic_lagna = vedic["computed_facts"]["sidereal_chart"]["lagna"]
    comparisons.append(
        {
            "body": "ascendant",
            "western_fact_id": western_asc["fact_id"],
            "vedic_fact_id": vedic_lagna["fact_id"],
            "western_tropical_longitude": western_asc["longitude_degrees"],
            "vedic_retained_tropical_longitude": vedic_lagna[
                "tropical_longitude_degrees"
            ],
            "absolute_difference_degrees": round(
                _circular_difference(
                    western_asc["longitude_degrees"],
                    vedic_lagna["tropical_longitude_degrees"],
                ),
                10,
            ),
        }
    )
    maximum = max(item["absolute_difference_degrees"] for item in comparisons)
    astronomy_check = {
        "fact_id": "multi-natal.cross-check.tropical-astronomy",
        "comparisons": comparisons,
        "maximum_absolute_difference_degrees": maximum,
        "tolerance_degrees": 0.000001,
        "status": "consistent" if maximum <= 0.000001 else "mismatch",
        "note": (
            "This compares retained tropical coordinates only; it does not compare "
            "Western tropical signs with Vedic sidereal signs."
        ),
        "rule_ids": ["MULTI-NATAL-ASTRONOMY-CHECK-001"],
        "source_ids": [PROJECT_SOURCE],
    }
    return {"utc": utc_check, "tropical_astronomy": astronomy_check}


def _system_summaries(charts: dict[str, Any]) -> dict[str, Any]:
    bazi = charts["bazi"]["computed_facts"]
    western = charts["western-astrology"]["computed_facts"]
    ziwei = charts["ziwei"]["computed_facts"]
    vedic = charts["vedic-astrology"]["computed_facts"]
    western_sun = _position(charts["western-astrology"], "sun")
    western_moon = _position(charts["western-astrology"], "moon")
    vedic_sun = _position(charts["vedic-astrology"], "sun")
    vedic_moon = _position(charts["vedic-astrology"], "moon")
    life_palace = _palace(charts["ziwei"], "命宫")
    body_palace = next(item for item in ziwei["palaces"] if item["isBodyPalace"])
    summaries: dict[str, Any] = {
        "bazi": {
            "fact_id": "multi-natal.summary.bazi",
            "pillars": {
                key: bazi["pillars"][key]["ganzhi"]
                for key in ("year", "month", "day", "hour")
            },
            "day_master": {
                "name": bazi["day_master"]["name"],
                "element": bazi["day_master"]["element"],
                "polarity": bazi["day_master"]["polarity"],
            },
            "source_fact_ids": [
                *(bazi["pillars"][key]["fact_id"] for key in ("year", "month", "day", "hour")),
                bazi["day_master"]["fact_id"],
            ],
            "rule_ids": ["MULTI-NATAL-SUMMARY-001"],
            "source_ids": [PROJECT_SOURCE],
        },
        "western-astrology": {
            "fact_id": "multi-natal.summary.western",
            "sun_sign": western_sun["sign"],
            "moon_sign": western_moon["sign"],
            "ascendant_sign": western["angles"]["ascendant"]["sign"],
            "midheaven_sign": western["angles"]["midheaven"]["sign"],
            "house_system": charts["western-astrology"]["normalized_input"]["house_system"],
            "source_fact_ids": [
                western_sun["fact_id"],
                western_moon["fact_id"],
                western["angles"]["ascendant"]["fact_id"],
                western["angles"]["midheaven"]["fact_id"],
            ],
            "rule_ids": ["MULTI-NATAL-SUMMARY-001"],
            "source_ids": [PROJECT_SOURCE],
        },
        "ziwei": {
            "fact_id": "multi-natal.summary.ziwei",
            "life_palace_branch": life_palace["earthlyBranch"],
            "life_palace_major_stars": [
                item["name"] for item in life_palace["majorStars"]
            ],
            "body_palace": body_palace["name"],
            "body_palace_branch": body_palace["earthlyBranch"],
            "soul_ruler": ziwei["soul_ruler"],
            "body_ruler": ziwei["body_ruler"],
            "five_elements_class": ziwei["five_elements_class"],
            "source_fact_ids": [life_palace["fact_id"], body_palace["fact_id"]],
            "rule_ids": ["MULTI-NATAL-SUMMARY-001"],
            "source_ids": [PROJECT_SOURCE],
        },
        "vedic-astrology": {
            "fact_id": "multi-natal.summary.vedic",
            "lagna_sign": vedic["sidereal_chart"]["lagna"]["sign"],
            "sun_sign": vedic_sun["sign"],
            "moon_sign": vedic_moon["sign"],
            "moon_nakshatra": vedic_moon["nakshatra"]["name"],
            "moon_pada": vedic_moon["nakshatra"]["pada"],
            "ayanamsha": vedic["astronomy"]["ayanamsha"]["name"],
            "selected_lineages": sorted(vedic["lineages"]),
            "source_fact_ids": [
                vedic["sidereal_chart"]["lagna"]["fact_id"],
                vedic_sun["fact_id"],
                vedic_moon["fact_id"],
            ],
            "rule_ids": ["MULTI-NATAL-SUMMARY-001"],
            "source_ids": [PROJECT_SOURCE],
        },
    }
    if "numerology" in charts:
        mappings = {}
        fact_ids = []
        for mapping, profile in charts["numerology"].items():
            facts = profile["computed_facts"]
            mappings[mapping] = {
                key: facts[key]["value"]
                for key in ("life_path", "birthday", "expression", "soul_urge", "personality")
            }
            fact_ids.extend(
                facts[key]["fact_id"]
                for key in ("life_path", "birthday", "expression", "soul_urge", "personality")
            )
        summaries["numerology"] = {
            "fact_id": "multi-natal.summary.numerology",
            "mappings": mappings,
            "source_fact_ids": fact_ids,
            "rule_ids": ["MULTI-NATAL-NUMEROLOGY-001"],
            "source_ids": [PROJECT_SOURCE],
        }
    return summaries


def _observation(
    system: str,
    lineage: str,
    facts: list[dict[str, Any]],
    values: dict[str, Any],
) -> dict[str, Any]:
    return {
        "system": system,
        "lineage": lineage,
        "fact_ids": [item["fact_id"] for item in facts],
        "values": values,
    }


def _synthesis_axes(charts: dict[str, Any]) -> list[dict[str, Any]]:
    bazi = charts["bazi"]["computed_facts"]
    western = charts["western-astrology"]
    ziwei = charts["ziwei"]
    vedic = charts["vedic-astrology"]
    western_facts = western["computed_facts"]
    vedic_facts = vedic["computed_facts"]
    bazi_lineage = "project-bazi-structural-v0.2"
    western_lineage = "tropical-natal-structural-v0.3"
    ziwei_lineage = ziwei["normalized_input"]["lineage"]
    vedic_lineage = "true-citra-common-v0.1"

    sun_w = _position(western, "sun")
    moon_w = _position(western, "moon")
    venus_w = _position(western, "venus")
    sun_v = _position(vedic, "sun")
    moon_v = _position(vedic, "moon")
    venus_v = _position(vedic, "venus")
    lagna_v = vedic_facts["sidereal_chart"]["lagna"]
    life = _palace(ziwei, "命宫")
    wellbeing = _palace(ziwei, "福德")
    career = _palace(ziwei, "官禄")
    spouse = _palace(ziwei, "夫妻")
    wealth = _palace(ziwei, "财帛")
    ascendant_w = western_facts["angles"]["ascendant"]
    midheaven_w = western_facts["angles"]["midheaven"]
    house10_w = [item for item in western_facts["positions"] if item["house"] == 10]
    house7_w = [item for item in western_facts["positions"] if item["house"] == 7]
    house2_w = [item for item in western_facts["positions"] if item["house"] == 2]
    house10_v = [item for item in vedic_facts["sidereal_chart"]["positions"] if item["house"] == 10]
    house7_v = [item for item in vedic_facts["sidereal_chart"]["positions"] if item["house"] == 7]
    house2_v = [item for item in vedic_facts["sidereal_chart"]["positions"] if item["house"] == 2]

    axes = [
        {
            "axis_id": "core-identity",
            "label": "Core identity structures",
            "observations": [
                _observation(
                    "bazi",
                    bazi_lineage,
                    [bazi["pillars"]["day"], bazi["day_master"]],
                    {
                        "day_pillar": bazi["pillars"]["day"]["ganzhi"],
                        "day_master": bazi["day_master"]["name"],
                    },
                ),
                _observation(
                    "western-astrology",
                    western_lineage,
                    [sun_w, ascendant_w],
                    {"sun": sun_w["sign"], "ascendant": ascendant_w["sign"]},
                ),
                _observation(
                    "ziwei",
                    ziwei_lineage,
                    [life],
                    {
                        "life_palace_branch": life["earthlyBranch"],
                        "major_stars": [item["name"] for item in life["majorStars"]],
                    },
                ),
                _observation(
                    "vedic-astrology",
                    vedic_lineage,
                    [sun_v, lagna_v],
                    {"sun": sun_v["sign"], "lagna": lagna_v["sign"]},
                ),
            ],
        },
        {
            "axis_id": "inner-reflection",
            "label": "Inner and reflective structures",
            "observations": [
                _observation(
                    "western-astrology",
                    western_lineage,
                    [moon_w],
                    {"moon": moon_w["sign"], "house": moon_w["house"]},
                ),
                _observation(
                    "ziwei",
                    ziwei_lineage,
                    [wellbeing],
                    {
                        "palace": "福德",
                        "branch": wellbeing["earthlyBranch"],
                        "major_stars": [item["name"] for item in wellbeing["majorStars"]],
                    },
                ),
                _observation(
                    "vedic-astrology",
                    vedic_lineage,
                    [moon_v],
                    {
                        "moon": moon_v["sign"],
                        "nakshatra": moon_v["nakshatra"]["name"],
                        "pada": moon_v["nakshatra"]["pada"],
                    },
                ),
            ],
        },
        {
            "axis_id": "vocation",
            "label": "Vocation-related structures",
            "observations": [
                _observation(
                    "bazi",
                    bazi_lineage,
                    [bazi["pillars"]["month"], bazi["day_master"]],
                    {
                        "month_pillar": bazi["pillars"]["month"]["ganzhi"],
                        "day_master": bazi["day_master"]["name"],
                    },
                ),
                _observation(
                    "western-astrology",
                    western_lineage,
                    [midheaven_w, *house10_w],
                    {
                        "midheaven": midheaven_w["sign"],
                        "tenth_house_bodies": [item["body"] for item in house10_w],
                    },
                ),
                _observation(
                    "ziwei",
                    ziwei_lineage,
                    [career],
                    {
                        "palace": "官禄",
                        "branch": career["earthlyBranch"],
                        "major_stars": [item["name"] for item in career["majorStars"]],
                    },
                ),
                _observation(
                    "vedic-astrology",
                    vedic_lineage,
                    house10_v or [lagna_v],
                    {"tenth_house_bodies": [item["body"] for item in house10_v]},
                ),
            ],
        },
        {
            "axis_id": "relationships",
            "label": "Relationship-related structures",
            "observations": [
                _observation(
                    "bazi",
                    bazi_lineage,
                    bazi["branch_relations"] or [bazi["pillars"]["day"]],
                    {
                        "branch_relations": [
                            {
                                "type": item["type"],
                                "positions": item["positions"],
                            }
                            for item in bazi["branch_relations"]
                        ]
                    },
                ),
                _observation(
                    "western-astrology",
                    western_lineage,
                    [venus_w, *house7_w],
                    {
                        "venus": venus_w["sign"],
                        "seventh_house_bodies": [item["body"] for item in house7_w],
                    },
                ),
                _observation(
                    "ziwei",
                    ziwei_lineage,
                    [spouse],
                    {
                        "palace": "夫妻",
                        "branch": spouse["earthlyBranch"],
                        "major_stars": [item["name"] for item in spouse["majorStars"]],
                    },
                ),
                _observation(
                    "vedic-astrology",
                    vedic_lineage,
                    [venus_v, *(house7_v or [])],
                    {
                        "venus": venus_v["sign"],
                        "seventh_house_bodies": [item["body"] for item in house7_v],
                    },
                ),
            ],
        },
        {
            "axis_id": "resources",
            "label": "Resource-related structures",
            "observations": [
                _observation(
                    "bazi",
                    bazi_lineage,
                    [bazi["ten_gods"]],
                    {"ten_gods_recorded": True},
                ),
                _observation(
                    "western-astrology",
                    western_lineage,
                    house2_w or [ascendant_w],
                    {"second_house_bodies": [item["body"] for item in house2_w]},
                ),
                _observation(
                    "ziwei",
                    ziwei_lineage,
                    [wealth],
                    {
                        "palace": "财帛",
                        "branch": wealth["earthlyBranch"],
                        "major_stars": [item["name"] for item in wealth["majorStars"]],
                    },
                ),
                _observation(
                    "vedic-astrology",
                    vedic_lineage,
                    house2_v or [lagna_v],
                    {"second_house_bodies": [item["body"] for item in house2_v]},
                ),
            ],
        },
    ]
    for axis in axes:
        axis["fact_id"] = f"multi-natal.axis.{axis['axis_id']}"
        axis["rule_ids"] = ["MULTI-NATAL-BRIDGE-001"]
        axis["source_ids"] = [PROJECT_SOURCE]
        axis["statement"] = (
            "These independently calculated structures are displayed together for "
            "navigation only; no equivalence or agreement score is asserted."
        )
        axis["dispute_ids"] = ["DSP-MULTI-NATAL-COMPARABILITY-001"]
    return axes


def calculate_natal_synthesis(payload: dict[str, Any]) -> dict[str, Any]:
    """Calculate every supported birth-based chart and a non-merging synthesis."""

    normalized = _normalize(payload)
    charts = _run_native_charts(normalized)
    original_charts = deepcopy(charts)
    cross_checks = _cross_checks(charts)
    if not cross_checks["utc"]["all_equal"]:
        raise NatalSynthesisError(
            "utc_mismatch", "Native systems did not normalize to one UTC instant."
        )
    if cross_checks["tropical_astronomy"]["status"] != "consistent":
        raise NatalSynthesisError(
            "astronomy_mismatch",
            "Western and Vedic retained tropical coordinates exceeded tolerance.",
        )
    summaries = _system_summaries(charts)
    axes = _synthesis_axes(charts)
    if charts != original_charts:
        raise AssertionError("Synthesis must not mutate native charts.")

    derived_findings = [
        {
            "finding_id": "multi-natal.finding.utc-consistency",
            "fact_ids": [cross_checks["utc"]["fact_id"]],
            "rule_ids": ["MULTI-NATAL-ROUTING-001"],
            "source_ids": [PROJECT_SOURCE],
            "confidence": "deterministic",
            "statement": "All native charts use the same normalized UTC instant.",
        },
        {
            "finding_id": "multi-natal.finding.astronomy-consistency",
            "fact_ids": [cross_checks["tropical_astronomy"]["fact_id"]],
            "rule_ids": ["MULTI-NATAL-ASTRONOMY-CHECK-001"],
            "source_ids": [PROJECT_SOURCE],
            "confidence": "deterministic",
            "statement": (
                "Western and Vedic retained tropical coordinates agree within the "
                "declared numerical tolerance."
            ),
        },
        *[
            {
                "finding_id": f"multi-natal.finding.axis.{axis['axis_id']}",
                "fact_ids": [
                    axis["fact_id"],
                    *[
                        fact_id
                        for observation in axis["observations"]
                        for fact_id in observation["fact_ids"]
                    ],
                ],
                "rule_ids": ["MULTI-NATAL-BRIDGE-001"],
                "source_ids": [PROJECT_SOURCE],
                "confidence": "low",
                "statement": axis["statement"],
            }
            for axis in axes
        ],
    ]
    included = [*CORE_SYSTEMS, *(["numerology"] if "numerology" in charts else [])]
    return {
        "schema_version": SCHEMA_VERSION,
        "engine": {
            "name": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "lineage": LINEAGE,
            "repository_dependencies": [],
            "source_ids": [PROJECT_SOURCE],
        },
        "raw_input": deepcopy(payload),
        "normalized_input": {
            "birth_date": normalized["birth_date"],
            "birth_time": normalized["birth_time"],
            "local_datetime": normalized["local_datetime"],
            "birthplace": normalized["birthplace"],
            "calculation_gender": normalized["calculation_gender"],
            "fold": normalized["fold"],
            "policies": normalized["policies"],
            "included_systems": included,
            "numerology_selected": normalized["numerology"] is not None,
        },
        "computed_facts": {
            "charts": charts,
            "cross_checks": cross_checks,
            "system_summaries": summaries,
            "synthesis_axes": axes,
        },
        "derived_findings": derived_findings,
        "narrative": {
            "calculation_basis": {
                "fact_ids": [
                    cross_checks["utc"]["fact_id"],
                    cross_checks["tropical_astronomy"]["fact_id"],
                ],
                "rule_ids": [
                    "MULTI-NATAL-ROUTING-001",
                    "MULTI-NATAL-ASTRONOMY-CHECK-001",
                ],
                "statement": (
                    f"Calculated {len(included)} independent system outputs from one "
                    "confirmed local birth profile."
                ),
            },
            "system_summaries": [
                {
                    "fact_ids": [summary["fact_id"], *summary["source_fact_ids"]],
                    "rule_ids": summary["rule_ids"],
                    "statement": f"See the independent {system} structural summary.",
                }
                for system, summary in summaries.items()
            ],
            "cross_system_synthesis": [
                {
                    "fact_ids": [
                        axis["fact_id"],
                        *[
                            fact_id
                            for observation in axis["observations"]
                            for fact_id in observation["fact_ids"]
                        ],
                    ],
                    "rule_ids": ["MULTI-NATAL-BRIDGE-001"],
                    "statement": f"{axis['label']}: {axis['statement']}",
                }
                for axis in axes
            ],
            "limitations": [
                "The crosswalk does not make different systems or symbols equivalent.",
                "No recurrence count is treated as probability, truth, or predictive accuracy.",
                (
                    "No medical, legal, financial, employment, safety, or "
                    "relationship verdict is produced."
                ),
                (
                    "Birth data is sensitive personal data and must not be "
                    "persisted without explicit consent."
                ),
            ],
        },
        "validation": {
            "status": "valid_with_warnings",
            "warnings": [
                {
                    "code": "cross_system_non_equivalence",
                    "message": (
                        "Synthesis axes are navigation aids and do not establish "
                        "conceptual equivalence."
                    ),
                },
                {
                    "code": "symbolic_not_predictive",
                    "message": (
                        "The report is structural and reflective, not a "
                        "guaranteed prediction."
                    ),
                },
            ],
        },
    }
