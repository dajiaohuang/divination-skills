"""Calculate a bounded, project-native Zi Wei Dou Shu structural chart."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, date, timedelta
from typing import Any

from divination_skills.solar_time import apparent_solar_time
from divination_skills.time import TimeNormalizationError, localize_strict
from lunar_python import Lunar, Solar

from systems.ziwei.star_catalog import (
    CLASSICAL_SOURCE_ID,
    DOCTOR_CYCLE_NAMES,
    FIRE_BELL_STARTS,
    GENERAL_FRONT_CYCLE_NAMES,
    KUI_YUE_BY_STEM,
    LIFE_CYCLE_NAMES,
    LIFE_CYCLE_START,
    LU_CUN_BY_STEM,
    TIAN_MA_BY_GROUP,
    YEAR_FRONT_CYCLE_NAMES,
    branch_index,
    brightness,
    group_value,
    metadata,
    place_cycle,
)

SOURCE_ID = "SRC-ZIWEI-PROJECT-SPEC-001"
CALENDAR_SOURCE_ID = "SRC-ZIWEI-LUNARPY-001"
LINEAGE = "project-native-ziwei-structural-v0.5"
SCHEMA_VERSION = "0.5.0"
ENGINE_VERSION = "0.5.0"
MIN_YEAR = 1900
MAX_YEAR = 2099

STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
PALACE_BRANCHES = tuple("寅卯辰巳午未申酉戌亥子丑")
PALACE_ROLES = (
    "命宫",
    "兄弟",
    "夫妻",
    "子女",
    "财帛",
    "疾厄",
    "迁移",
    "仆役",
    "官禄",
    "田宅",
    "福德",
    "父母",
)
TIME_BRANCHES = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子")
TIME_RANGES = (
    "00:00-00:59",
    "01:00-02:59",
    "03:00-04:59",
    "05:00-06:59",
    "07:00-08:59",
    "09:00-10:59",
    "11:00-12:59",
    "13:00-14:59",
    "15:00-16:59",
    "17:00-18:59",
    "19:00-20:59",
    "21:00-22:59",
    "23:00-23:59",
)
FIVE_ELEMENT_BUREAUS = {
    "水": ("水二局", 2),
    "木": ("木三局", 3),
    "金": ("金四局", 4),
    "土": ("土五局", 5),
    "火": ("火六局", 6),
}
NAYIN_ELEMENTS = tuple("金火木土金火水土金木水土火木水金火木土金火水土金木水土火木水")
SOUL_RULERS = {
    "子": "贪狼",
    "丑": "巨门",
    "寅": "禄存",
    "卯": "文曲",
    "辰": "廉贞",
    "巳": "武曲",
    "午": "破军",
    "未": "武曲",
    "申": "廉贞",
    "酉": "文曲",
    "戌": "禄存",
    "亥": "巨门",
}
BODY_RULERS = {
    "子": "火星",
    "丑": "天相",
    "寅": "天梁",
    "卯": "天同",
    "辰": "文昌",
    "巳": "天机",
    "午": "火星",
    "未": "天相",
    "申": "天梁",
    "酉": "天同",
    "戌": "文昌",
    "亥": "天机",
}
TRANSFORMATIONS = {
    "甲": ("廉贞", "破军", "武曲", "太阳"),
    "乙": ("天机", "天梁", "紫微", "太阴"),
    "丙": ("天同", "天机", "文昌", "廉贞"),
    "丁": ("太阴", "天同", "天机", "巨门"),
    "戊": ("贪狼", "太阴", "右弼", "天机"),
    "己": ("武曲", "贪狼", "天梁", "文曲"),
    "庚": ("太阳", "武曲", "太阴", "天同"),
    "辛": ("巨门", "太阳", "文曲", "文昌"),
    "壬": ("天梁", "紫微", "天府", "武曲"),
    "癸": ("破军", "巨门", "太阴", "贪狼"),
}
TRANSFORMATION_LABELS = ("禄", "权", "科", "忌")


class ZiweiError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _time_index(hour: int) -> int:
    return (hour + 1) // 2


def _sexagenary_index(stem_index: int, branch_index: int) -> int:
    return next(
        index for index in range(60) if index % 10 == stem_index and index % 12 == branch_index
    )


def _palace_stems(year_stem_index: int) -> tuple[str, ...]:
    first = (year_stem_index * 2 + 2) % 10
    return tuple(STEMS[(first + index) % 10] for index in range(12))


def _five_elements_class(stem: str, branch: str) -> tuple[str, int]:
    cycle_index = _sexagenary_index(STEMS.index(stem), BRANCHES.index(branch))
    element = NAYIN_ELEMENTS[cycle_index // 2]
    return FIVE_ELEMENT_BUREAUS[element]


def _ziwei_index(lunar_day: int, bureau_number: int) -> int:
    """Place 紫微 from lunar day and bureau with the traditional quotient adjustment."""

    adjustment = (bureau_number - lunar_day % bureau_number) % bureau_number
    quotient = (lunar_day + adjustment) // bureau_number
    direction_adjustment = adjustment if adjustment % 2 == 0 else -adjustment
    return (quotient - 1 + direction_adjustment) % 12


def _star_positions(
    lunar_month: int,
    lunar_day: int,
    time_index: int,
    bureau_number: int,
    year_stem: str,
    year_branch: str,
    forward: bool,
    soul_index: int,
) -> tuple[dict[int, list[str]], dict[int, list[str]], dict[int, list[str]]]:
    ziwei = _ziwei_index(lunar_day, bureau_number)
    # PALACE_BRANCHES is indexed from 寅.  In that coordinate system 天府 is
    # mirrored directly across the 12-palace ring from 紫微.
    tianfu = (-ziwei) % 12
    major: dict[int, list[str]] = {index: [] for index in range(12)}
    minor: dict[int, list[str]] = {index: [] for index in range(12)}
    auxiliary: dict[int, list[str]] = {index: [] for index in range(12)}
    for name, offset in (
        ("紫微", 0),
        ("天机", -1),
        ("太阳", -3),
        ("武曲", -4),
        ("天同", -5),
        ("廉贞", -8),
    ):
        major[(ziwei + offset) % 12].append(name)
    for name, offset in (
        ("天府", 0),
        ("太阴", 1),
        ("贪狼", 2),
        ("巨门", 3),
        ("天相", 4),
        ("天梁", 5),
        ("七杀", 6),
        ("破军", 10),
    ):
        major[(tianfu + offset) % 12].append(name)
    for name, index in (
        ("文昌", (8 - time_index) % 12),
        ("文曲", (2 + time_index) % 12),
        ("左辅", (2 + lunar_month - 1) % 12),
        ("右弼", (8 - (lunar_month - 1)) % 12),
    ):
        minor[index].append(name)

    lu_cun = branch_index(LU_CUN_BY_STEM[year_stem])
    kui, yue = KUI_YUE_BY_STEM[year_stem]
    tian_ma = branch_index(group_value(year_branch, TIAN_MA_BY_GROUP))
    fire_start, bell_start = group_value(year_branch, FIRE_BELL_STARTS)
    year_offset = BRANCHES.index(year_branch)
    left = next(index for index, names in minor.items() if "左辅" in names)
    right = next(index for index, names in minor.items() if "右弼" in names)
    role_index = {name: index for index, name in enumerate(PALACE_ROLES)}
    placements = (
        ("禄存", lu_cun),
        ("擎羊", (lu_cun + 1) % 12),
        ("陀罗", (lu_cun - 1) % 12),
        ("天魁", branch_index(kui)),
        ("天钺", branch_index(yue)),
        ("天马", tian_ma),
        ("火星", (branch_index(fire_start) + time_index % 12) % 12),
        ("铃星", (branch_index(bell_start) + time_index % 12) % 12),
        ("地劫", (branch_index("亥") + time_index % 12) % 12),
        ("地空", (branch_index("亥") - time_index % 12) % 12),
        ("天刑", (branch_index("酉") + lunar_month - 1) % 12),
        ("天姚", (branch_index("丑") + lunar_month - 1) % 12),
        ("三台", (left + lunar_day - 1) % 12),
        ("八座", (right - lunar_day + 1) % 12),
        ("天哭", (branch_index("午") - year_offset) % 12),
        ("天虚", (branch_index("午") + year_offset) % 12),
        ("龙池", (branch_index("辰") + year_offset) % 12),
        ("凤阁", (branch_index("戌") - year_offset) % 12),
        ("台辅", (branch_index("午") + time_index % 12) % 12),
        ("封诰", (branch_index("寅") + time_index % 12) % 12),
        ("红鸾", (branch_index("卯") - year_offset) % 12),
        ("天喜", (branch_index("卯") - year_offset + 6) % 12),
        ("天德", (branch_index("酉") + year_offset) % 12),
        ("月德", (branch_index("巳") + year_offset) % 12),
        ("年解", (branch_index("戌") - year_offset) % 12),
        ("解神", branch_index(("申", "戌", "子", "寅", "辰", "午")[(lunar_month - 1) // 2])),
        ("天伤", (soul_index - role_index["仆役"]) % 12),
        ("天使", (soul_index - role_index["疾厄"]) % 12),
    )
    for name, index in placements:
        auxiliary[index].append(name)

    life_cycle = place_cycle(
        LIFE_CYCLE_NAMES,
        branch_index(
            LIFE_CYCLE_START[
                next(
                    name
                    for name, number in FIVE_ELEMENT_BUREAUS.values()
                    if number == bureau_number
                )
            ]
        ),
        forward,
    )
    doctor_cycle = place_cycle(DOCTOR_CYCLE_NAMES, lu_cun, forward)
    year_front = place_cycle(YEAR_FRONT_CYCLE_NAMES, branch_index(year_branch), True)
    general_start = branch_index(
        group_value(
            year_branch,
            {
                frozenset("寅午戌"): "午",
                frozenset("申子辰"): "子",
                frozenset("巳酉丑"): "酉",
                frozenset("亥卯未"): "卯",
            },
        )
    )
    general_front = place_cycle(GENERAL_FRONT_CYCLE_NAMES, general_start, True)
    for index in range(12):
        auxiliary[index].extend(life_cycle[index])
        auxiliary[index].extend(doctor_cycle[index])
        auxiliary[index].extend(year_front[index])
        auxiliary[index].extend(general_front[index])
    return major, minor, auxiliary


def _star(
    name: str,
    fact_id: str,
    kind: str,
    transformations: dict[str, str],
    earthly_branch: str,
) -> dict[str, Any]:
    attributes = metadata(name)
    brightness_value = brightness(name, earthly_branch)
    return {
        "name": name,
        "type": kind,
        "category": attributes["category"],
        "element": attributes["element"],
        "polarity": attributes["polarity"],
        "brightness": brightness_value,
        "brightness_status": (
            "classical_volume_two_matrix"
            if brightness_value is not None
            else "not_listed_in_classical_volume_two_matrix"
        ),
        "brightness_source_ids": ([CLASSICAL_SOURCE_ID] if brightness_value is not None else []),
        "mutagen": transformations.get(name),
        "self_transformations": [],
        "fact_id": fact_id,
        "source_ids": [SOURCE_ID, CLASSICAL_SOURCE_ID],
    }


def _attach_self_transformations(palaces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach explicit outward/inward palace-stem transformation paths.

    Outward means the target star is in the palace whose own stem triggers
    the transformation.  Inward means the target star is in the opposite
    palace and is triggered by that opposite palace's stem.  The direction
    naming is a selected product policy; the ten-stem star mapping is the
    classical table.
    """

    paths: list[dict[str, Any]] = []
    for target in palaces:
        origin_specs = (
            (target, "outward", "↓", "离心自化"),
            (palaces[(target["index"] + 6) % 12], "inward", "↑", "向心自化"),
        )
        stars = [
            star
            for field in ("majorStars", "minorStars", "adjectiveStars", "auxiliaryStars")
            for star in target[field]
        ]
        for origin, direction, symbol, label_zh in origin_specs:
            transformations = dict(
                zip(
                    TRANSFORMATIONS[origin["heavenlyStem"]],
                    TRANSFORMATION_LABELS,
                    strict=True,
                )
            )
            for star in stars:
                transformation = transformations.get(star["name"])
                if transformation is None:
                    continue
                fact_id = f"ziwei.self_transformation.{len(paths) + 1:03d}"
                nested = {
                    "fact_id": fact_id,
                    "direction": direction,
                    "direction_zh": label_zh,
                    "symbol": symbol,
                    "transformation": transformation,
                    "origin_palace_fact_id": origin["fact_id"],
                    "origin_stem": origin["heavenlyStem"],
                    "rule_ids": ["ZIWEI-TRANSFORMATION-PALACE-STEM-001"],
                    "source_ids": [SOURCE_ID, CLASSICAL_SOURCE_ID],
                }
                star["self_transformations"].append(nested)
                paths.append(
                    {
                        **nested,
                        "target_star": star["name"],
                        "target_star_fact_id": star["fact_id"],
                        "target_palace_fact_id": target["fact_id"],
                    }
                )
    return paths


def _representative_hour(time_index: int) -> int:
    if time_index == 0:
        return 0
    if time_index == 12:
        return 23
    return time_index * 2 - 1


def _normalize_input(
    payload: dict[str, Any],
) -> tuple[Any, Any, int, Any, Any, int, dict[str, str], dict[str, object] | None]:
    calendar_type = payload.get("calendar_type", "solar")
    if calendar_type not in {"solar", "lunar"}:
        raise ZiweiError("invalid_calendar_type", "calendar_type must be solar or lunar.")
    timezone = payload.get("timezone")
    if not isinstance(timezone, str) or not timezone:
        raise ZiweiError("missing_fields", "Missing field(s): timezone")

    if calendar_type == "solar":
        if "local_datetime" not in payload:
            raise ZiweiError("missing_fields", "Missing field(s): local_datetime")
        if any(field in payload for field in ("lunar_date", "is_leap_month", "time_index")):
            raise ZiweiError(
                "conflicting_calendar_fields",
                "Solar input cannot include lunar_date, is_leap_month, or time_index.",
            )
        local_datetime = payload["local_datetime"]
    else:
        missing = sorted({"lunar_date", "is_leap_month", "time_index"} - set(payload))
        if missing:
            raise ZiweiError("missing_fields", f"Missing field(s): {', '.join(missing)}")
        if "local_datetime" in payload:
            raise ZiweiError(
                "conflicting_calendar_fields",
                "Lunar input cannot include local_datetime.",
            )
        if not isinstance(payload["is_leap_month"], bool):
            raise ZiweiError("invalid_leap_month_flag", "is_leap_month must be boolean.")
        time_index = payload["time_index"]
        if (
            not isinstance(time_index, int)
            or isinstance(time_index, bool)
            or time_index not in range(13)
        ):
            raise ZiweiError("invalid_time_index", "time_index must be an integer from 0 to 12.")
        try:
            lunar_date = date.fromisoformat(payload["lunar_date"])
            lunar_month = -lunar_date.month if payload["is_leap_month"] else lunar_date.month
            source_lunar = Lunar.fromYmd(lunar_date.year, lunar_month, lunar_date.day)
            source_solar = source_lunar.getSolar()
        except (TypeError, ValueError, IndexError) as exc:
            raise ZiweiError("invalid_lunar_date", "lunar_date is not valid.") from exc
        if source_lunar.getMonth() != lunar_month:
            raise ZiweiError(
                "invalid_leap_month",
                "The requested leap-month flag does not exist for this lunar date.",
            )
        hour = _representative_hour(time_index)
        local_datetime = (
            f"{source_solar.getYear():04d}-{source_solar.getMonth():02d}-"
            f"{source_solar.getDay():02d}T{hour:02d}:00:00"
        )

    try:
        local, fold = localize_strict(local_datetime, timezone, payload.get("fold"))
    except TimeNormalizationError as exc:
        raise ZiweiError(exc.code, exc.message) from exc
    if not MIN_YEAR <= local.year <= MAX_YEAR:
        raise ZiweiError("unsupported_year", f"year must be between {MIN_YEAR} and {MAX_YEAR}.")

    longitude = payload.get("longitude")
    latitude = payload.get("latitude")
    if longitude is not None and (
        isinstance(longitude, bool)
        or not isinstance(longitude, (int, float))
        or not -180 <= longitude <= 180
    ):
        raise ZiweiError("invalid_longitude", "longitude must be between -180 and 180.")
    if latitude is not None and (
        isinstance(latitude, bool)
        or not isinstance(latitude, (int, float))
        or not -90 <= latitude <= 90
    ):
        raise ZiweiError("invalid_latitude", "latitude must be between -90 and 90.")

    time_basis = payload.get("time_basis")
    legacy_true_solar = payload.get("true_solar_time")
    if legacy_true_solar is not None and not isinstance(legacy_true_solar, bool):
        raise ZiweiError("invalid_true_solar_time", "true_solar_time must be boolean.")
    if time_basis is None:
        time_basis = "apparent_solar" if legacy_true_solar else "civil"
    if time_basis not in {"civil", "apparent_solar"}:
        raise ZiweiError(
            "invalid_time_basis",
            "time_basis must be civil or apparent_solar.",
        )
    if legacy_true_solar is not None and (
        (legacy_true_solar and time_basis != "apparent_solar")
        or (not legacy_true_solar and time_basis != "civil")
    ):
        raise ZiweiError(
            "conflicting_time_basis",
            "true_solar_time and time_basis select different calculation clocks.",
        )
    if time_basis == "apparent_solar":
        if calendar_type != "solar":
            raise ZiweiError(
                "solar_time_requires_solar_input",
                "apparent_solar time requires a solar local_datetime input.",
            )
        if longitude is None:
            raise ZiweiError(
                "longitude_required",
                "longitude is required when time_basis is apparent_solar.",
            )
        solar_time = apparent_solar_time(local, float(longitude))
        calculation_local = solar_time.apparent_datetime
        solar_time_fact = solar_time.to_dict()
    else:
        calculation_local = local
        solar_time_fact = None

    late_zi_policy = payload.get("late_zi_policy", "current_day")
    year_boundary = payload.get("year_boundary", "lunar_new_year")
    leap_month_policy = payload.get("leap_month_policy", "preserve")
    if late_zi_policy not in {"current_day", "next_day"}:
        raise ZiweiError(
            "invalid_late_zi_policy",
            "late_zi_policy must be current_day or next_day.",
        )
    if year_boundary not in {"lunar_new_year", "spring_commences"}:
        raise ZiweiError(
            "invalid_year_boundary",
            "year_boundary must be lunar_new_year or spring_commences.",
        )
    if leap_month_policy not in {"preserve", "split_after_15"}:
        raise ZiweiError(
            "invalid_leap_month_policy",
            "leap_month_policy must be preserve or split_after_15.",
        )

    time_index = _time_index(calculation_local.hour)
    basis_local = (
        calculation_local + timedelta(days=1)
        if time_index == 12 and late_zi_policy == "next_day"
        else calculation_local
    )
    solar = Solar.fromYmdHms(
        basis_local.year,
        basis_local.month,
        basis_local.day,
        basis_local.hour,
        basis_local.minute,
        basis_local.second,
    )
    lunar = solar.getLunar()
    return (
        local,
        calculation_local,
        fold,
        solar,
        lunar,
        time_index,
        {
            "calendar_type": calendar_type,
            "year_boundary": year_boundary,
            "late_zi_policy": late_zi_policy,
            "leap_month_policy": leap_month_policy,
            "time_basis": time_basis,
        },
        solar_time_fact,
    )


def calculate(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "calendar_type",
        "local_datetime",
        "lunar_date",
        "is_leap_month",
        "time_index",
        "timezone",
        "fold",
        "calculation_gender",
        "year_boundary",
        "late_zi_policy",
        "leap_month_policy",
        "longitude",
        "latitude",
        "time_basis",
        "true_solar_time",
    }
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise ZiweiError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    missing = sorted({"timezone", "calculation_gender"} - set(payload))
    if missing:
        raise ZiweiError("missing_fields", f"Missing field(s): {', '.join(missing)}")
    gender = payload["calculation_gender"]
    if gender not in {"male", "female"}:
        raise ZiweiError("invalid_calculation_gender", "calculation_gender must be male or female.")
    (
        local,
        calculation_local,
        fold,
        solar,
        lunar,
        time_index,
        policies,
        solar_time_fact,
    ) = _normalize_input(payload)
    calendar_lunar_month = abs(lunar.getMonth())
    lunar_day = lunar.getDay()
    lunar_month = (
        calendar_lunar_month % 12 + 1
        if lunar.getMonth() < 0
        and policies["leap_month_policy"] == "split_after_15"
        and lunar_day > 15
        else calendar_lunar_month
    )
    if policies["year_boundary"] == "spring_commences":
        year_stem = lunar.getYearGanByLiChun()
        year_branch = lunar.getYearZhiByLiChun()
    else:
        year_stem = lunar.getYearGan()
        year_branch = lunar.getYearZhi()
    year_stem_index = STEMS.index(year_stem)
    soul_index = (lunar_month - 1 - time_index) % 12
    body_index = (lunar_month - 1 + time_index) % 12
    stems = _palace_stems(year_stem_index)
    five_elements_class, bureau_number = _five_elements_class(
        stems[soul_index], PALACE_BRANCHES[soul_index]
    )
    yang_year = year_stem_index % 2 == 0
    forward = (yang_year and gender == "male") or (not yang_year and gender == "female")
    major, minor, auxiliary = _star_positions(
        lunar_month,
        lunar_day,
        time_index,
        bureau_number,
        year_stem,
        year_branch,
        forward,
        soul_index,
    )
    transformations = dict(zip(TRANSFORMATIONS[year_stem], TRANSFORMATION_LABELS, strict=True))

    minor_limit_start = branch_index(
        group_value(
            year_branch,
            {
                frozenset("寅午戌"): "辰",
                frozenset("申子辰"): "戌",
                frozenset("巳酉丑"): "未",
                frozenset("亥卯未"): "丑",
            },
        )
    )
    minor_limit_forward = gender == "male"
    minor_limit_by_palace = {index: [] for index in range(12)}
    for age in range(1, 121):
        step = age - 1 if minor_limit_forward else -(age - 1)
        minor_limit_by_palace[(minor_limit_start + step) % 12].append(age)

    palaces = []
    for index, branch in enumerate(PALACE_BRANCHES):
        role_index = (soul_index - index) % 12
        decade_slot = (index - soul_index) % 12 if forward else (soul_index - index) % 12
        fact_id = f"ziwei.palace.{index:03d}"
        palaces.append(
            {
                "index": index,
                "name": PALACE_ROLES[role_index],
                "heavenlyStem": stems[index],
                "earthlyBranch": branch,
                "isBodyPalace": index == body_index,
                "isOriginalPalace": index == soul_index,
                "majorStars": [
                    _star(
                        name,
                        f"{fact_id}.majorStars.{number:03d}",
                        "major",
                        transformations,
                        branch,
                    )
                    for number, name in enumerate(major[index], start=1)
                ],
                "minorStars": [
                    _star(
                        name,
                        f"{fact_id}.minorStars.{number:03d}",
                        "minor",
                        transformations,
                        branch,
                    )
                    for number, name in enumerate(minor[index], start=1)
                ],
                "adjectiveStars": [],
                "auxiliaryStars": [
                    _star(
                        name,
                        f"{fact_id}.auxiliaryStars.{number:03d}",
                        "auxiliary",
                        transformations,
                        branch,
                    )
                    for number, name in enumerate(auxiliary[index], start=1)
                ],
                "decadal": {
                    "start_age": bureau_number + decade_slot * 10,
                    "end_age": bureau_number + decade_slot * 10 + 9,
                    "direction": "forward" if forward else "reverse",
                },
                "minor_limit_ages": minor_limit_by_palace[index],
                "fact_id": fact_id,
                "source_ids": [SOURCE_ID, CLASSICAL_SOURCE_ID],
            }
        )

    self_transformations = _attach_self_transformations(palaces)
    lunar_month_label = ("闰" if lunar.getMonth() < 0 else "") + lunar.getMonthInChinese()
    cause_palace = next(
        (palace for palace in palaces if palace["heavenlyStem"] == year_stem),
        None,
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "engine": {
            "name": "divination-skills-ziwei-native",
            "version": ENGINE_VERSION,
            "dependencies": {"lunar_python": "1.4.8"},
            "source_ids": [
                SOURCE_ID,
                CLASSICAL_SOURCE_ID,
                CALENDAR_SOURCE_ID,
                "SRC-TIME-PYTHON-ZONEINFO-001",
                "SRC-TIME-TZDATA-001",
                *(
                    ["SRC-ASTRONOMY-NOAA-SOLAR-001"]
                    if policies["time_basis"] == "apparent_solar"
                    else []
                ),
            ],
        },
        "normalized_input": {
            "local_datetime": local.isoformat(),
            "calculation_datetime": calculation_local.isoformat(),
            "utc_datetime": local.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "timezone": payload["timezone"],
            "fold": fold,
            "calculation_gender": gender,
            "time_index": time_index,
            "calendar_leap_month": lunar.getMonth() < 0,
            "effective_lunar_month": lunar_month,
            "calendar_type": policies["calendar_type"],
            "year_boundary": policies["year_boundary"],
            "late_zi_policy": policies["late_zi_policy"],
            "leap_month_policy": policies["leap_month_policy"],
            "longitude": (
                float(payload["longitude"]) if payload.get("longitude") is not None else None
            ),
            "latitude": (
                float(payload["latitude"]) if payload.get("latitude") is not None else None
            ),
            "time_basis": policies["time_basis"],
            "true_solar_time_applied": policies["time_basis"] == "apparent_solar",
            "solar_time_correction": solar_time_fact,
            "lineage": LINEAGE,
        },
        "computed_facts": {
            "solar_date": (f"{solar.getYear():04d}-{solar.getMonth():02d}-{solar.getDay():02d}"),
            "lunar_date": f"{lunar.getYear()}年{lunar_month_label}月{lunar.getDayInChinese()}",
            "chinese_date": f"{lunar.getYearInGanZhi()}年 {lunar.getTimeInGanZhi()}时",
            "raw_dates": {
                "lunar_year": lunar.getYear(),
                "lunar_month": lunar.getMonth(),
                "lunar_day": lunar_day,
                "year_stem": year_stem,
                "year_branch": year_branch,
                "calendar_year_stem": lunar.getYearGan(),
                "calendar_year_branch": lunar.getYearZhi(),
            },
            "time_label": TIME_BRANCHES[time_index],
            "time_range": TIME_RANGES[time_index],
            "western_sign": solar.getXingZuo(),
            "zodiac": lunar.getYearShengXiao(),
            "body_palace_branch": PALACE_BRANCHES[body_index],
            "soul_palace_branch": PALACE_BRANCHES[soul_index],
            "soul_ruler": SOUL_RULERS[PALACE_BRANCHES[soul_index]],
            "body_ruler": BODY_RULERS[year_branch],
            "five_elements_class": five_elements_class,
            "bureau_number": bureau_number,
            "cause_palace": (
                {
                    "palace_fact_id": cause_palace["fact_id"],
                    "palace_name": cause_palace["name"],
                    "heavenly_stem": cause_palace["heavenlyStem"],
                }
                if cause_palace
                else None
            ),
            "self_transformations": self_transformations,
            "palaces": palaces,
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {
            "status": "valid",
            "warnings": [
                (
                    {
                        "code": "apparent_solar_time_approximation",
                        "message": (
                            "The double-hour and calculation date use the NOAA fractional-year "
                            "apparent-solar-time approximation."
                        ),
                    }
                    if policies["time_basis"] == "apparent_solar"
                    else {
                        "code": "local_civil_time_basis",
                        "message": (
                            "The engine uses the validated local civil double-hour; "
                            "apparent solar time is not applied."
                        ),
                    }
                ),
                {
                    "code": "calculation_gender_parameter",
                    "message": (
                        "calculation_gender controls decade direction only and is not "
                        "an inferred identity."
                    ),
                },
                {
                    "code": "bounded_classical_brightness",
                    "message": (
                        "Brightness is emitted only for stars listed in the selected classical "
                        "Volume Two matrix; unlisted stars remain explicit nulls."
                    ),
                },
                {
                    "code": "foundation_only",
                    "message": (
                        "This project-native v0.5 calculates a bounded structural foundation "
                        "and requires independent practitioner comparison."
                    ),
                },
            ],
        },
    }


def structural_report(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Ziwei chart is required.")
    report = deepcopy(result)
    original = deepcopy(result["computed_facts"])
    facts = result["computed_facts"]
    palace_ids = [palace["fact_id"] for palace in facts["palaces"]]
    report["derived_findings"] = [
        {
            "finding_id": "ziwei.finding.structure.001",
            "fact_ids": palace_ids,
            "rule_ids": ["ZIWEI-NATIVE-NATAL-001"],
            "confidence": "medium",
            "source_ids": [SOURCE_ID],
        }
    ]
    report["narrative"] = {
        "structure": {
            "fact_ids": palace_ids,
            "rule_ids": ["ZIWEI-STRUCTURAL-BOUNDARY-001"],
            "statement": (
                f"The project-native chart contains 12 palaces under "
                f"{facts['five_elements_class']}. This structural report does not assign "
                "life-event meanings."
            ),
        },
        "limitations": [
            "No star, palace, decade, or transformation interpretation is generated.",
            "The native foundation has not passed an independent practitioner comparison.",
            "iztro is retained only as an ignored reference and is never invoked at runtime.",
        ],
    }
    if report["computed_facts"] != original:
        raise AssertionError("Ziwei reporting must not mutate chart facts.")
    return report
