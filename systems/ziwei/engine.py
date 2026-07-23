"""Calculate a bounded, project-native Zi Wei Dou Shu structural chart."""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC
from typing import Any

from divination_skills.time import TimeNormalizationError, localize_strict
from lunar_python import Solar

SOURCE_ID = "SRC-ZIWEI-PROJECT-SPEC-001"
CALENDAR_SOURCE_ID = "SRC-ZIWEI-LUNARPY-001"
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
NAYIN_ELEMENTS = tuple(
    "金火木土金火水土金木水土火木水金火木土金火水土金木水土火木水"
)
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
    "壬": ("天梁", "紫微", "左辅", "武曲"),
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
) -> tuple[dict[int, list[str]], dict[int, list[str]]]:
    ziwei = _ziwei_index(lunar_day, bureau_number)
    tianfu = (4 - ziwei) % 12
    major: dict[int, list[str]] = {index: [] for index in range(12)}
    minor: dict[int, list[str]] = {index: [] for index in range(12)}
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
        ("文昌", (10 - time_index) % 12),
        ("文曲", (4 + time_index) % 12),
        ("左辅", (3 + lunar_month - 1) % 12),
        ("右弼", (9 - (lunar_month - 1)) % 12),
    ):
        minor[index].append(name)
    return major, minor


def _star(
    name: str,
    fact_id: str,
    kind: str,
    transformations: dict[str, str],
) -> dict[str, Any]:
    return {
        "name": name,
        "type": kind,
        "brightness": None,
        "mutagen": transformations.get(name),
        "fact_id": fact_id,
        "source_ids": [SOURCE_ID],
    }


def calculate(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {"local_datetime", "timezone", "fold", "calculation_gender"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise ZiweiError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    missing = sorted({"local_datetime", "timezone", "calculation_gender"} - set(payload))
    if missing:
        raise ZiweiError("missing_fields", f"Missing field(s): {', '.join(missing)}")
    gender = payload["calculation_gender"]
    if gender not in {"male", "female"}:
        raise ZiweiError("invalid_calculation_gender", "calculation_gender must be male or female.")
    try:
        local, fold = localize_strict(
            payload["local_datetime"], payload["timezone"], payload.get("fold")
        )
    except TimeNormalizationError as exc:
        raise ZiweiError(exc.code, exc.message) from exc
    if not MIN_YEAR <= local.year <= MAX_YEAR:
        raise ZiweiError("unsupported_year", f"year must be between {MIN_YEAR} and {MAX_YEAR}.")

    time_index = _time_index(local.hour)
    solar = Solar.fromYmdHms(
        local.year,
        local.month,
        local.day,
        local.hour,
        local.minute,
        local.second,
    )
    lunar = solar.getLunar()
    lunar_month = abs(lunar.getMonth())
    lunar_day = lunar.getDay()
    year_stem = lunar.getYearGan()
    year_branch = lunar.getYearZhi()
    year_stem_index = STEMS.index(year_stem)
    soul_index = (lunar_month - 1 - time_index) % 12
    body_index = (lunar_month - 1 + time_index) % 12
    stems = _palace_stems(year_stem_index)
    five_elements_class, bureau_number = _five_elements_class(
        stems[soul_index], PALACE_BRANCHES[soul_index]
    )
    major, minor = _star_positions(lunar_month, lunar_day, time_index, bureau_number)
    transformations = dict(zip(TRANSFORMATIONS[year_stem], TRANSFORMATION_LABELS, strict=True))
    yang_year = year_stem_index % 2 == 0
    forward = (yang_year and gender == "male") or (not yang_year and gender == "female")

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
                    )
                    for number, name in enumerate(major[index], start=1)
                ],
                "minorStars": [
                    _star(
                        name,
                        f"{fact_id}.minorStars.{number:03d}",
                        "minor",
                        transformations,
                    )
                    for number, name in enumerate(minor[index], start=1)
                ],
                "adjectiveStars": [],
                "decadal": {
                    "start_age": bureau_number + decade_slot * 10,
                    "end_age": bureau_number + decade_slot * 10 + 9,
                    "direction": "forward" if forward else "reverse",
                },
                "fact_id": fact_id,
                "source_ids": [SOURCE_ID],
            }
        )

    lunar_month_label = ("闰" if lunar.getMonth() < 0 else "") + lunar.getMonthInChinese()
    return {
        "schema_version": "0.1.0",
        "engine": {
            "name": "divination-skills-ziwei-native",
            "version": "0.1.0",
            "dependencies": {"lunar_python": "1.4.8"},
            "source_ids": [
                SOURCE_ID,
                CALENDAR_SOURCE_ID,
                "SRC-TIME-PYTHON-ZONEINFO-001",
                "SRC-TIME-TZDATA-001",
            ],
        },
        "normalized_input": {
            "local_datetime": local.isoformat(),
            "utc_datetime": local.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "timezone": payload["timezone"],
            "fold": fold,
            "calculation_gender": gender,
            "time_index": time_index,
            "calendar_leap_month": lunar.getMonth() < 0,
            "lineage": "project-native-ziwei-foundation-v0.1",
        },
        "computed_facts": {
            "solar_date": f"{local.year}-{local.month:02d}-{local.day:02d}",
            "lunar_date": f"{lunar.getYear()}年{lunar_month_label}月{lunar.getDayInChinese()}",
            "chinese_date": f"{lunar.getYearInGanZhi()}年 {lunar.getTimeInGanZhi()}时",
            "raw_dates": {
                "lunar_year": lunar.getYear(),
                "lunar_month": lunar.getMonth(),
                "lunar_day": lunar_day,
                "year_stem": year_stem,
                "year_branch": year_branch,
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
            "palaces": palaces,
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "local_civil_time_basis",
                    "message": (
                        "The engine uses the validated local civil double-hour; "
                        "true solar time is not applied."
                    ),
                },
                {
                    "code": "calculation_gender_parameter",
                    "message": (
                        "calculation_gender controls decade direction only and is not "
                        "an inferred identity."
                    ),
                },
                {
                    "code": "foundation_only",
                    "message": (
                        "This project-native v0.1 calculates a bounded structural foundation "
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
