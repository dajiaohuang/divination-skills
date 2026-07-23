"""Calculate traceable Bazi facts from a Gregorian local birth time."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from functools import lru_cache
from itertools import combinations
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from divination_skills.solar_time import ApparentSolarTime, apparent_solar_time
from lunar_python import Solar

ENGINE_NAME = "divination-skills-bazi"
ENGINE_VERSION = "0.2.0"
SCHEMA_VERSION = "0.2.0"
MIN_YEAR = 1900
MAX_YEAR = 2100
BEIJING = ZoneInfo("Asia/Shanghai")
TERM_REFERENCE_ZONE = timezone(timedelta(hours=8), name="UTC+08")

STEMS = ("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸")
BRANCHES = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥")
ELEMENTS = ("wood", "fire", "earth", "metal", "water")
POLARITIES = ("yang", "yin")
GROWTH_STAGES = (
    "长生",
    "沐浴",
    "冠带",
    "临官",
    "帝旺",
    "衰",
    "病",
    "死",
    "墓",
    "绝",
    "胎",
    "养",
)
GROWTH_START_BRANCH = {
    "甲": "亥",
    "乙": "午",
    "丙": "寅",
    "丁": "酉",
    "戊": "寅",
    "己": "酉",
    "庚": "巳",
    "辛": "子",
    "壬": "申",
    "癸": "卯",
}
NAYIN_NAMES = (
    "海中金",
    "炉中火",
    "大林木",
    "路旁土",
    "剑锋金",
    "山头火",
    "涧下水",
    "城头土",
    "白蜡金",
    "杨柳木",
    "泉中水",
    "屋上土",
    "霹雳火",
    "松柏木",
    "长流水",
    "沙中金",
    "山下火",
    "平地木",
    "壁上土",
    "金箔金",
    "覆灯火",
    "天河水",
    "大驿土",
    "钗钏金",
    "桑柘木",
    "大溪水",
    "沙中土",
    "天上火",
    "石榴木",
    "大海水",
)
ELEMENT_BY_HAN = {
    "木": "wood",
    "火": "fire",
    "土": "earth",
    "金": "metal",
    "水": "water",
}
BRANCH_ELEMENTS = {
    "子": "water",
    "丑": "earth",
    "寅": "wood",
    "卯": "wood",
    "辰": "earth",
    "巳": "fire",
    "午": "fire",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "戌": "earth",
    "亥": "water",
}
SEASONAL_ELEMENT = {
    "寅": "wood",
    "卯": "wood",
    "辰": "earth",
    "巳": "fire",
    "午": "fire",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "戌": "earth",
    "亥": "water",
    "子": "water",
    "丑": "earth",
}

HIDDEN_STEMS = {
    "子": ("癸",),
    "丑": ("己", "癸", "辛"),
    "寅": ("甲", "丙", "戊"),
    "卯": ("乙",),
    "辰": ("戊", "乙", "癸"),
    "巳": ("丙", "戊", "庚"),
    "午": ("丁", "己"),
    "未": ("己", "丁", "乙"),
    "申": ("庚", "壬", "戊"),
    "酉": ("辛",),
    "戌": ("戊", "辛", "丁"),
    "亥": ("壬", "甲"),
}

JIE_TERMS = (
    ("小寒", 11, 285),
    ("立春", 0, 315),
    ("惊蛰", 1, 345),
    ("清明", 2, 15),
    ("立夏", 3, 45),
    ("芒种", 4, 75),
    ("小暑", 5, 105),
    ("立秋", 6, 135),
    ("白露", 7, 165),
    ("寒露", 8, 195),
    ("立冬", 9, 225),
    ("大雪", 10, 255),
)

PAIR_RELATIONS = {
    "combine": (
        ("子", "丑"),
        ("寅", "亥"),
        ("卯", "戌"),
        ("辰", "酉"),
        ("巳", "申"),
        ("午", "未"),
    ),
    "clash": (
        ("子", "午"),
        ("丑", "未"),
        ("寅", "申"),
        ("卯", "酉"),
        ("辰", "戌"),
        ("巳", "亥"),
    ),
    "harm": (
        ("子", "未"),
        ("丑", "午"),
        ("寅", "巳"),
        ("卯", "辰"),
        ("申", "亥"),
        ("酉", "戌"),
    ),
    "break": (
        ("子", "酉"),
        ("丑", "辰"),
        ("寅", "亥"),
        ("卯", "午"),
        ("巳", "申"),
        ("未", "戌"),
    ),
    # Only the two pairs containing each harmony group's cardinal branch are
    # labeled half_harmony.  The remaining birth–tomb pair is an arching
    # relation in some lineages and is intentionally not collapsed into it.
    "half_harmony": (
        ("申", "子"),
        ("子", "辰"),
        ("亥", "卯"),
        ("卯", "未"),
        ("寅", "午"),
        ("午", "戌"),
        ("巳", "酉"),
        ("酉", "丑"),
    ),
}

THREE_HARMONIES = (
    ("申", "子", "辰"),
    ("亥", "卯", "未"),
    ("寅", "午", "戌"),
    ("巳", "酉", "丑"),
)

THREE_MEETINGS = (
    ("亥", "子", "丑"),
    ("寅", "卯", "辰"),
    ("巳", "午", "未"),
    ("申", "酉", "戌"),
)


class CalculationError(ValueError):
    """A user-correctable calculation input error."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


@dataclass(frozen=True)
class NormalizedBirth:
    civil_local: datetime
    calculation_local: datetime
    utc: datetime
    timezone: str
    fold: int
    day_boundary: str
    longitude: float | None
    latitude: float | None
    luck_cycle_direction: str | None
    time_basis: str
    solar_time: ApparentSolarTime | None

    @property
    def local(self) -> datetime:
        """Backward-compatible alias for the clock used to select pillars."""

        return self.calculation_local


@dataclass(frozen=True)
class SolarTerm:
    name: str
    month_sequence: int
    solar_longitude_degrees: int
    local_beijing: datetime
    utc: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "month_sequence": self.month_sequence,
            "solar_longitude_degrees": self.solar_longitude_degrees,
            "beijing_datetime": self.local_beijing.isoformat(),
            "utc_datetime": self.utc.isoformat().replace("+00:00", "Z"),
        }


def _strict_localize(naive: datetime, timezone_name: str, fold: int | None) -> tuple[datetime, int]:
    try:
        zone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise CalculationError(
            "unknown_timezone", f"Unknown IANA time zone: {timezone_name}"
        ) from exc

    candidates: list[tuple[int, datetime]] = []
    for candidate_fold in (0, 1):
        aware = naive.replace(tzinfo=zone, fold=candidate_fold)
        roundtrip = aware.astimezone(UTC).astimezone(zone).replace(tzinfo=None)
        if roundtrip == naive:
            candidates.append((candidate_fold, aware))

    unique_offsets = {candidate.utcoffset() for _, candidate in candidates}
    if not candidates:
        raise CalculationError(
            "nonexistent_local_time",
            "The local time does not exist because the clock moved forward.",
        )
    if len(unique_offsets) > 1 and fold is None:
        raise CalculationError(
            "ambiguous_local_time",
            "The local time occurs twice; provide fold=0 for the earlier offset "
            "or fold=1 for the later offset.",
        )
    selected_fold = 0 if fold is None else fold
    if selected_fold not in (0, 1):
        raise CalculationError("invalid_fold", "fold must be 0 or 1.")
    for candidate_fold, candidate in candidates:
        if candidate_fold == selected_fold:
            return candidate, selected_fold
    return candidates[0][1], candidates[0][0]


def normalize_input(payload: dict[str, Any]) -> NormalizedBirth:
    """Validate and normalize calculator input without silently repairing it."""

    allowed = {
        "local_datetime",
        "timezone",
        "fold",
        "day_boundary",
        "longitude",
        "latitude",
        "luck_cycle_direction",
        "true_solar_time",
        "time_basis",
    }
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise CalculationError("unknown_fields", f"Unknown input field(s): {', '.join(unknown)}")
    raw_datetime = payload.get("local_datetime")
    timezone_name = payload.get("timezone")
    if not isinstance(raw_datetime, str) or not raw_datetime:
        raise CalculationError("missing_local_datetime", "local_datetime is required.")
    if not isinstance(timezone_name, str) or not timezone_name:
        raise CalculationError("missing_timezone", "timezone is required.")
    try:
        naive = datetime.fromisoformat(raw_datetime)
    except ValueError as exc:
        raise CalculationError(
            "invalid_local_datetime", "local_datetime must be an ISO 8601 local date and time."
        ) from exc
    if naive.tzinfo is not None:
        raise CalculationError(
            "offset_not_allowed",
            "local_datetime must not contain a UTC offset; provide an IANA timezone separately.",
        )
    if not MIN_YEAR <= naive.year <= MAX_YEAR:
        raise CalculationError(
            "date_out_of_range", f"Supported Gregorian years are {MIN_YEAR} through {MAX_YEAR}."
        )

    fold = payload.get("fold")
    if fold is not None and (isinstance(fold, bool) or not isinstance(fold, int)):
        raise CalculationError("invalid_fold", "fold must be 0 or 1.")
    local, selected_fold = _strict_localize(naive, timezone_name, fold)

    day_boundary = payload.get("day_boundary", "midnight")
    if day_boundary not in {"midnight", "zi_initial"}:
        raise CalculationError(
            "invalid_day_boundary", "day_boundary must be 'midnight' or 'zi_initial'."
        )
    direction = payload.get("luck_cycle_direction")
    if direction not in {None, "forward", "reverse"}:
        raise CalculationError(
            "invalid_luck_cycle_direction",
            "luck_cycle_direction must be 'forward' or 'reverse'.",
        )

    longitude = payload.get("longitude")
    latitude = payload.get("latitude")
    if longitude is not None and (
        isinstance(longitude, bool)
        or not isinstance(longitude, (int, float))
        or not -180 <= longitude <= 180
    ):
        raise CalculationError("invalid_longitude", "longitude must be between -180 and 180.")
    if latitude is not None and (
        isinstance(latitude, bool)
        or not isinstance(latitude, (int, float))
        or not -90 <= latitude <= 90
    ):
        raise CalculationError("invalid_latitude", "latitude must be between -90 and 90.")

    time_basis = payload.get("time_basis")
    legacy_true_solar = payload.get("true_solar_time")
    if legacy_true_solar is not None and not isinstance(legacy_true_solar, bool):
        raise CalculationError("invalid_true_solar_time", "true_solar_time must be boolean.")
    if time_basis is None:
        time_basis = "apparent_solar" if legacy_true_solar else "civil"
    if time_basis not in {"civil", "apparent_solar"}:
        raise CalculationError(
            "invalid_time_basis",
            "time_basis must be 'civil' or 'apparent_solar'.",
        )
    if legacy_true_solar is not None and (
        (legacy_true_solar and time_basis != "apparent_solar")
        or (not legacy_true_solar and time_basis != "civil")
    ):
        raise CalculationError(
            "conflicting_time_basis",
            "true_solar_time and time_basis select different calculation clocks.",
        )
    if time_basis == "apparent_solar" and longitude is None:
        raise CalculationError(
            "longitude_required",
            "longitude is required when time_basis is 'apparent_solar'.",
        )

    solar_time = (
        apparent_solar_time(local, float(longitude))
        if time_basis == "apparent_solar" and longitude is not None
        else None
    )
    calculation_local = solar_time.apparent_datetime if solar_time else local

    return NormalizedBirth(
        civil_local=local,
        calculation_local=calculation_local,
        utc=local.astimezone(UTC),
        timezone=timezone_name,
        fold=selected_fold,
        day_boundary=day_boundary,
        longitude=float(longitude) if longitude is not None else None,
        latitude=float(latitude) if latitude is not None else None,
        luck_cycle_direction=direction,
        time_basis=time_basis,
        solar_time=solar_time,
    )


@lru_cache(maxsize=256)
def _jie_terms_for_year(year: int) -> tuple[SolarTerm, ...]:
    table = Solar.fromYmdHms(year, 6, 15, 12, 0, 0).getLunar().getJieQiTable()
    terms: list[SolarTerm] = []
    for name, sequence, degrees in JIE_TERMS:
        solar = table[name]
        local_beijing = datetime(
            solar.getYear(),
            solar.getMonth(),
            solar.getDay(),
            solar.getHour(),
            solar.getMinute(),
            solar.getSecond(),
            tzinfo=TERM_REFERENCE_ZONE,
        )
        if local_beijing.year != year:
            raise RuntimeError(f"Solar-term provider returned {name} outside requested year {year}")
        terms.append(
            SolarTerm(
                name=name,
                month_sequence=sequence,
                solar_longitude_degrees=degrees,
                local_beijing=local_beijing,
                utc=local_beijing.astimezone(UTC),
            )
        )
    return tuple(sorted(terms, key=lambda item: item.utc))


def _surrounding_terms(instant_utc: datetime) -> tuple[SolarTerm, SolarTerm]:
    year = instant_utc.astimezone(TERM_REFERENCE_ZONE).year
    terms = sorted(
        (
            term
            for candidate_year in (year - 1, year, year + 1)
            for term in _jie_terms_for_year(candidate_year)
        ),
        key=lambda item: item.utc,
    )
    previous = max((term for term in terms if term.utc <= instant_utc), key=lambda item: item.utc)
    following = min((term for term in terms if term.utc > instant_utc), key=lambda item: item.utc)
    return previous, following


def _solar_year(instant_utc: datetime) -> int:
    beijing_year = instant_utc.astimezone(TERM_REFERENCE_ZONE).year
    li_chun = next(term for term in _jie_terms_for_year(beijing_year) if term.name == "立春")
    return beijing_year if instant_utc >= li_chun.utc else beijing_year - 1


def solar_year_boundaries(solar_year: int) -> tuple[SolarTerm, SolarTerm]:
    """Return the exact UTC Li Chun interval for one solar-term year."""

    start = next(
        term for term in _jie_terms_for_year(solar_year) if term.name == "立春"
    )
    end = next(
        term for term in _jie_terms_for_year(solar_year + 1) if term.name == "立春"
    )
    return start, end


def _pillar_index(stem_index: int, branch_index: int) -> int:
    return next(
        index for index in range(60) if index % 10 == stem_index and index % 12 == branch_index
    )


def _stem_data(stem_index: int) -> dict[str, Any]:
    return {
        "index": stem_index,
        "name": STEMS[stem_index],
        "element": ELEMENTS[stem_index // 2],
        "polarity": POLARITIES[stem_index % 2],
    }


def _branch_data(branch_index: int) -> dict[str, Any]:
    branch = BRANCHES[branch_index]
    return {
        "index": branch_index,
        "name": branch,
        "hidden_stems": list(HIDDEN_STEMS[branch]),
    }


def _pillar(index: int, position: str) -> dict[str, Any]:
    normalized_index = index % 60
    stem_index = normalized_index % 10
    branch_index = normalized_index % 12
    return {
        "fact_id": f"bazi.pillar.{position}",
        "index": normalized_index,
        "ganzhi": STEMS[stem_index] + BRANCHES[branch_index],
        "stem": _stem_data(stem_index),
        "branch": _branch_data(branch_index),
        "source_ids": ["SRC-BAZI-LUNARPY-001"],
    }


def _gregorian_jdn(year: int, month: int, day: int) -> int:
    a = (14 - month) // 12
    shifted_year = year + 4800 - a
    shifted_month = month + 12 * a - 3
    return (
        day
        + (153 * shifted_month + 2) // 5
        + 365 * shifted_year
        + shifted_year // 4
        - shifted_year // 100
        + shifted_year // 400
        - 32045
    )


def _ten_god(day_stem_index: int, target_stem_index: int) -> str:
    day_element = day_stem_index // 2
    target_element = target_stem_index // 2
    same_polarity = day_stem_index % 2 == target_stem_index % 2
    relation = (target_element - day_element) % 5
    if relation == 0:
        return "比肩" if same_polarity else "劫财"
    if relation == 1:
        return "食神" if same_polarity else "伤官"
    if relation == 2:
        return "偏财" if same_polarity else "正财"
    if relation == 3:
        return "七杀" if same_polarity else "正官"
    return "偏印" if same_polarity else "正印"


def _ten_gods(pillars: dict[str, dict[str, Any]]) -> dict[str, Any]:
    day_stem_index = pillars["day"]["stem"]["index"]
    visible: dict[str, str] = {}
    hidden: dict[str, list[dict[str, str]]] = {}
    for position, pillar in pillars.items():
        visible[position] = _ten_god(day_stem_index, pillar["stem"]["index"])
        hidden[position] = [
            {"stem": stem, "ten_god": _ten_god(day_stem_index, STEMS.index(stem))}
            for stem in pillar["branch"]["hidden_stems"]
        ]
    return {
        "fact_id": "bazi.ten_gods",
        "day_master": STEMS[day_stem_index],
        "visible": visible,
        "hidden": hidden,
        "source_ids": ["SRC-BAZI-LUNARPY-001"],
    }


def _nayin(pillars: dict[str, dict[str, Any]]) -> dict[str, Any]:
    by_pillar = {}
    for position, pillar in pillars.items():
        name = NAYIN_NAMES[pillar["index"] // 2]
        by_pillar[position] = {
            "name": name,
            "element": ELEMENT_BY_HAN[name[-1]],
        }
    return {
        "fact_id": "bazi.nayin",
        "by_pillar": by_pillar,
        "source_ids": ["SRC-BAZI-SANMING-001"],
    }


def _growth_stage(stem: str, branch: str) -> str:
    start = BRANCHES.index(GROWTH_START_BRANCH[stem])
    target = BRANCHES.index(branch)
    forward = STEMS.index(stem) % 2 == 0
    offset = (target - start) % 12 if forward else (start - target) % 12
    return GROWTH_STAGES[offset]


def _growth_stages(pillars: dict[str, dict[str, Any]]) -> dict[str, Any]:
    day_stem = pillars["day"]["stem"]["name"]
    return {
        "fact_id": "bazi.growth_stages",
        "method": "ten_stems_yang_forward_yin_reverse",
        "day_master_by_pillar": {
            position: _growth_stage(day_stem, pillar["branch"]["name"])
            for position, pillar in pillars.items()
        },
        "pillar_self": {
            position: _growth_stage(
                pillar["stem"]["name"],
                pillar["branch"]["name"],
            )
            for position, pillar in pillars.items()
        },
        "source_ids": ["SRC-BAZI-SANMING-001"],
        "dispute_ids": ["DSP-BAZI-GROWTH-STAGE-001"],
    }


def _seasonal_element_states(month_branch: str) -> dict[str, Any]:
    commanding_element = SEASONAL_ELEMENT[month_branch]
    commanding_index = ELEMENTS.index(commanding_element)
    states = {
        ELEMENTS[commanding_index]: "旺",
        ELEMENTS[(commanding_index + 1) % 5]: "相",
        ELEMENTS[(commanding_index - 1) % 5]: "休",
        ELEMENTS[(commanding_index - 2) % 5]: "囚",
        ELEMENTS[(commanding_index + 2) % 5]: "死",
    }
    return {
        "fact_id": "bazi.seasonal_element_states",
        "month_branch": month_branch,
        "commanding_element": commanding_element,
        "states": states,
        "source_ids": ["SRC-BAZI-SANMING-001"],
        "limitations": [
            "The four earth storage months are represented by the selected whole-month baseline.",
            "These states do not by themselves determine Day Master strength.",
        ],
    }


def _visible_element_counts(pillars: dict[str, dict[str, Any]]) -> dict[str, Any]:
    counts = dict.fromkeys(ELEMENTS, 0)
    for pillar in pillars.values():
        counts[pillar["stem"]["element"]] += 1
        counts[BRANCH_ELEMENTS[pillar["branch"]["name"]]] += 1
    highest = max(counts.values())
    return {
        "fact_id": "bazi.visible_element_counts",
        "scope": "four_visible_stems_and_four_visible_branches",
        "counts": counts,
        "most_present": [
            {"element": element, "count": count}
            for element, count in counts.items()
            if count == highest
        ],
        "hidden_stems_included": False,
        "source_ids": ["SRC-BAZI-PROJECT-SPEC-001", "SRC-BAZI-SANMING-001"],
    }


def _branch_relations(pillars: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    positions = list(pillars)
    branch_by_position = {position: pillars[position]["branch"]["name"] for position in positions}
    relations: list[dict[str, Any]] = []
    relation_number = 1

    def add_relation(kind: str, members: list[str], branches: list[str]) -> None:
        nonlocal relation_number
        relations.append(
            {
                "fact_id": f"bazi.branch_relation.{relation_number:03d}",
                "type": kind,
                "positions": members,
                "branches": branches,
                "source_ids": [
                    "SRC-BAZI-PROJECT-SPEC-001",
                    "SRC-BAZI-LUNARPY-001",
                ],
            }
        )
        relation_number += 1

    for left, right in combinations(positions, 2):
        pair = {branch_by_position[left], branch_by_position[right]}
        for kind, configured_pairs in PAIR_RELATIONS.items():
            if any(pair == set(configured) for configured in configured_pairs):
                add_relation(
                    kind,
                    [left, right],
                    [branch_by_position[left], branch_by_position[right]],
                )
        if pair == {"子", "卯"}:
            add_relation(
                "punishment",
                [left, right],
                [branch_by_position[left], branch_by_position[right]],
            )
        if branch_by_position[left] == branch_by_position[right] and branch_by_position[left] in {
            "辰",
            "午",
            "酉",
            "亥",
        }:
            add_relation("self_punishment", [left, right], [branch_by_position[left]])

    present = set(branch_by_position.values())
    for group in THREE_HARMONIES:
        if set(group) <= present:
            members = [position for position in positions if branch_by_position[position] in group]
            add_relation("three_harmony", members, list(group))
    for group in THREE_MEETINGS:
        if set(group) <= present:
            members = [position for position in positions if branch_by_position[position] in group]
            add_relation("three_meeting", members, list(group))
    for group in (("寅", "巳", "申"), ("丑", "戌", "未")):
        if set(group) <= present:
            members = [position for position in positions if branch_by_position[position] in group]
            add_relation("three_punishment", members, list(group))
    return relations


def _luck_cycles(
    birth: NormalizedBirth,
    month_pillar_index: int,
    previous_term: SolarTerm,
    next_term: SolarTerm,
) -> dict[str, Any] | None:
    direction = birth.luck_cycle_direction
    if direction is None:
        return None
    if direction == "forward":
        interval_seconds = (next_term.utc - birth.utc).total_seconds()
        step = 1
        boundary_term = next_term
    else:
        interval_seconds = (birth.utc - previous_term.utc).total_seconds()
        step = -1
        boundary_term = previous_term
    start_age = interval_seconds / (3 * 86_400)
    cycles = []
    for number in range(1, 11):
        cycle_start = start_age + (number - 1) * 10
        cycles.append(
            {
                "number": number,
                "pillar": _pillar(month_pillar_index + step * number, f"luck_cycle_{number}"),
                "start_age_years": round(cycle_start, 6),
                "end_age_years": round(cycle_start + 10, 6),
            }
        )
    return {
        "fact_id": "bazi.luck_cycles",
        "direction": direction,
        "start_method": "three_days_per_year",
        "boundary_term": boundary_term.to_dict(),
        "start_age_years": round(start_age, 6),
        "cycles": cycles,
        "source_ids": ["SRC-BAZI-LUNARPY-001"],
        "dispute_ids": ["DSP-BAZI-LUCK-DIRECTION-001", "DSP-BAZI-LUCK-START-001"],
    }


def calculate_chart(payload: dict[str, Any]) -> dict[str, Any]:
    """Return deterministic facts; do not produce an interpretive narrative."""

    birth = normalize_input(payload)
    previous_term, next_term = _surrounding_terms(birth.utc)
    solar_year = _solar_year(birth.utc)

    year_index = (solar_year - 4) % 60
    year_stem_index = year_index % 10
    month_sequence = previous_term.month_sequence
    month_stem_index = (year_stem_index * 2 + 2 + month_sequence) % 10
    month_branch_index = (2 + month_sequence) % 12
    month_index = _pillar_index(month_stem_index, month_branch_index)

    base_day_index = (
        _gregorian_jdn(birth.local.year, birth.local.month, birth.local.day) + 49
    ) % 60
    late_zi = birth.local.hour == 23
    day_index = (
        base_day_index + 1 if birth.day_boundary == "zi_initial" and late_zi else base_day_index
    )
    hour_branch_index = ((birth.local.hour + 1) // 2) % 12
    hour_basis_day_index = base_day_index + 1 if late_zi else base_day_index
    hour_stem_index = ((hour_basis_day_index % 10) * 2 + hour_branch_index) % 10
    hour_index = _pillar_index(hour_stem_index, hour_branch_index)

    pillars = {
        "year": _pillar(year_index, "year"),
        "month": _pillar(month_index, "month"),
        "day": _pillar(day_index, "day"),
        "hour": _pillar(hour_index, "hour"),
    }

    warnings: list[dict[str, str]] = []
    if birth.time_basis == "civil" and (birth.longitude is not None or birth.latitude is not None):
        warnings.append(
            {
                "code": "coordinates_not_applied",
                "message": (
                    "Coordinates are retained as metadata under the selected civil-time basis."
                ),
            }
        )
    if birth.time_basis == "apparent_solar":
        warnings.append(
            {
                "code": "apparent_solar_time_approximation",
                "message": (
                    "Pillar date and hour use the NOAA fractional-year apparent-solar-time "
                    "approximation; the physical UTC instant and solar-term boundaries "
                    "are unchanged."
                ),
            }
        )
    if birth.luck_cycle_direction is None:
        warnings.append(
            {
                "code": "luck_cycle_direction_missing",
                "message": (
                    "Luck cycles were omitted because direction was not explicitly supplied."
                ),
            }
        )
    if birth.day_boundary == "zi_initial":
        warnings.append(
            {
                "code": "non_default_day_boundary",
                "message": "The day pillar advances at 23:00 under the selected zi_initial policy.",
            }
        )
    seconds_to_boundary = min(
        (birth.utc - previous_term.utc).total_seconds(),
        (next_term.utc - birth.utc).total_seconds(),
    )
    if seconds_to_boundary <= 300:
        warnings.append(
            {
                "code": "solar_term_boundary_sensitive",
                "message": (
                    "The input is within five minutes of a month boundary; "
                    "verify recorded time and time zone."
                ),
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "engine": {
            "name": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "dependencies": {"lunar_python": "1.4.8", "tzdata": "2026.3"},
            "source_ids": [
                "SRC-BAZI-LUNARPY-001",
                "SRC-BAZI-SANMING-001",
                "SRC-TIME-PYTHON-ZONEINFO-001",
                "SRC-TIME-TZDATA-001",
                *(["SRC-ASTRONOMY-NOAA-SOLAR-001"] if birth.time_basis == "apparent_solar" else []),
            ],
        },
        "raw_input": dict(payload),
        "normalized_input": {
            "local_datetime": birth.civil_local.isoformat(),
            "calculation_datetime": birth.calculation_local.isoformat(),
            "utc_datetime": birth.utc.isoformat().replace("+00:00", "Z"),
            "beijing_datetime": birth.utc.astimezone(BEIJING).isoformat(),
            "timezone": birth.timezone,
            "utc_offset_seconds": int(birth.civil_local.utcoffset().total_seconds()),
            "fold": birth.fold,
            "day_boundary": birth.day_boundary,
            "longitude": birth.longitude,
            "latitude": birth.latitude,
            "time_basis": birth.time_basis,
            "true_solar_time_applied": birth.time_basis == "apparent_solar",
            "solar_time_correction": (
                birth.solar_time.to_dict() if birth.solar_time is not None else None
            ),
            "luck_cycle_direction": birth.luck_cycle_direction,
        },
        "computed_facts": {
            "solar_year": solar_year,
            "previous_month_boundary": previous_term.to_dict(),
            "next_month_boundary": next_term.to_dict(),
            "pillars": pillars,
            "day_master": {
                "fact_id": "bazi.day_master",
                **pillars["day"]["stem"],
                "source_ids": ["SRC-BAZI-LUNARPY-001"],
            },
            "ten_gods": _ten_gods(pillars),
            "nayin": _nayin(pillars),
            "growth_stages": _growth_stages(pillars),
            "seasonal_element_states": _seasonal_element_states(pillars["month"]["branch"]["name"]),
            "visible_element_counts": _visible_element_counts(pillars),
            "branch_relations": _branch_relations(pillars),
            "luck_cycles": _luck_cycles(birth, month_index, previous_term, next_term),
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {"status": "valid", "warnings": warnings},
    }
