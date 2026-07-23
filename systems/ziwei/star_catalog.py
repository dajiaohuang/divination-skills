"""Project-native Ziwei star metadata and deterministic placement tables.

The catalog stores calculation facts, not copied prose or interpretive meanings.
"""

from __future__ import annotations

from collections.abc import Iterable

CLASSICAL_SOURCE_ID = "SRC-ZIWEI-QUANSHU-001"
PROJECT_SOURCE_ID = "SRC-ZIWEI-PROJECT-SPEC-001"

_BRIGHTNESS_GROUPS = {
    "子": {
        "庙": "天机天府太阴天相天梁破军禄存",
        "旺": "武曲天同贪狼巨门七杀",
        "得": "文昌文曲",
        "平": "紫微廉贞",
        "陷": "太阳擎羊火星铃星",
    },
    "丑": {
        "庙": "紫微武曲天府太阴贪狼天相七杀文昌文曲擎羊陀罗",
        "旺": "天梁破军",
        "得": "火星铃星",
        "利": "廉贞",
        "不": "太阳天同巨门",
        "陷": "天机",
    },
    "寅": {
        "庙": "廉贞天府巨门天相天梁七杀禄存火星铃星",
        "旺": "紫微太阳太阴",
        "得": "天机武曲破军",
        "利": "天同",
        "平": "贪狼文曲",
        "陷": "文昌陀罗",
    },
    "卯": {
        "庙": "太阳巨门天梁禄存",
        "旺": "紫微天机七杀文曲",
        "得": "天府",
        "利": "武曲贪狼文昌火星铃星",
        "平": "天同廉贞",
        "陷": "太阴天相破军擎羊",
    },
    "辰": {
        "庙": "武曲天府贪狼天梁七杀擎羊陀罗",
        "旺": "太阳破军",
        "得": "紫微天相文昌文曲",
        "利": "天机廉贞",
        "平": "天同",
        "陷": "太阴巨门火星铃星",
    },
    "巳": {
        "庙": "天同文昌文曲禄存",
        "旺": "紫微太阳巨门",
        "得": "天府天相火星铃星",
        "平": "天机武曲七杀破军",
        "陷": "廉贞太阴贪狼天梁陀罗",
    },
    "午": {
        "庙": "紫微天机天相天梁破军禄存火星铃星",
        "旺": "太阳武曲天府贪狼巨门七杀",
        "平": "廉贞",
        "不": "太阴",
        "陷": "天同文昌文曲擎羊",
    },
    "未": {
        "庙": "紫微武曲天府贪狼七杀擎羊陀罗",
        "旺": "天梁破军文曲",
        "得": "太阳天相",
        "利": "廉贞文昌火星铃星",
        "不": "天同太阴巨门",
        "陷": "天机",
    },
    "申": {
        "庙": "廉贞巨门天相七杀禄存",
        "旺": "紫微天同",
        "得": "天机太阳武曲天府破军文昌文曲",
        "利": "太阴",
        "平": "贪狼",
        "陷": "天梁陀罗火星铃星",
    },
    "酉": {
        "庙": "巨门文昌文曲禄存",
        "旺": "紫微天机天府太阴七杀",
        "得": "天梁火星铃星",
        "利": "武曲贪狼",
        "平": "太阳天同廉贞",
        "陷": "天相破军擎羊",
    },
    "戌": {
        "庙": "武曲天府贪狼天梁七杀擎羊陀罗火星铃星",
        "旺": "太阴破军",
        "得": "紫微天相",
        "利": "天机廉贞",
        "平": "天同",
        "不": "太阳",
        "陷": "巨门文昌文曲",
    },
    "亥": {
        "庙": "天同太阴禄存",
        "旺": "紫微巨门文曲",
        "得": "天府天相",
        "利": "文昌火星铃星",
        "平": "天机武曲七杀破军",
        "陷": "太阳廉贞贪狼天梁陀罗",
    },
}

# The source prints one-character star abbreviations in a matrix.  Expand each
# row into an explicit star -> grade table once so runtime lookup remains
# deterministic and reviewable.
_BRIGHTNESS_STAR_NAMES = (
    "紫微",
    "天机",
    "太阳",
    "武曲",
    "天同",
    "廉贞",
    "天府",
    "太阴",
    "贪狼",
    "巨门",
    "天相",
    "天梁",
    "七杀",
    "破军",
    "文昌",
    "文曲",
    "禄存",
    "擎羊",
    "陀罗",
    "火星",
    "铃星",
)


def _build_brightness_table() -> dict[str, dict[str, str]]:
    table: dict[str, dict[str, str]] = {}
    for branch, grades in _BRIGHTNESS_GROUPS.items():
        table[branch] = {}
        for grade, joined_names in grades.items():
            for star_name in _BRIGHTNESS_STAR_NAMES:
                if star_name in joined_names:
                    table[branch][star_name] = grade
    return table


BRIGHTNESS_BY_BRANCH = _build_brightness_table()


def brightness(name: str, branch: str) -> str | None:
    """Return the classical 卷二 matrix grade when that star is tabulated."""

    return BRIGHTNESS_BY_BRANCH.get(branch, {}).get(name)


PALACE_BRANCHES = tuple("寅卯辰巳午未申酉戌亥子丑")
BRANCH_INDEX = {branch: index for index, branch in enumerate(PALACE_BRANCHES)}

STAR_METADATA: dict[str, dict[str, str | None]] = {
    "紫微": {"category": "major", "element": "土", "polarity": "阴"},
    "天机": {"category": "major", "element": "木", "polarity": "阴"},
    "太阳": {"category": "major", "element": "火", "polarity": "阳"},
    "武曲": {"category": "major", "element": "金", "polarity": "阴"},
    "天同": {"category": "major", "element": "水", "polarity": "阳"},
    "廉贞": {"category": "major", "element": "火", "polarity": "阴"},
    "天府": {"category": "major", "element": "土", "polarity": "阳"},
    "太阴": {"category": "major", "element": "水", "polarity": "阴"},
    "贪狼": {"category": "major", "element": "水木", "polarity": "阳"},
    "巨门": {"category": "major", "element": "水", "polarity": "阴"},
    "天相": {"category": "major", "element": "水", "polarity": "阳"},
    "天梁": {"category": "major", "element": "土", "polarity": "阳"},
    "七杀": {"category": "major", "element": "金", "polarity": "阴"},
    "破军": {"category": "major", "element": "水", "polarity": "阴"},
}

for _name, _category, _element in (
    ("文昌", "minor", "金"),
    ("文曲", "minor", "水"),
    ("左辅", "minor", "土"),
    ("右弼", "minor", "水"),
    ("天魁", "auxiliary", "火"),
    ("天钺", "auxiliary", "火"),
    ("禄存", "auxiliary", "土"),
    ("擎羊", "malefic", "金"),
    ("陀罗", "malefic", "金"),
    ("天马", "auxiliary", "火"),
    ("火星", "malefic", "火"),
    ("铃星", "malefic", "火"),
    ("地劫", "malefic", "火"),
    ("地空", "malefic", "火"),
    ("天刑", "auxiliary", "火"),
    ("天姚", "auxiliary", "水"),
    ("三台", "auxiliary", "土"),
    ("八座", "auxiliary", "土"),
    ("天哭", "auxiliary", "金"),
    ("天虚", "auxiliary", "土"),
    ("龙池", "auxiliary", "水"),
    ("凤阁", "auxiliary", "土"),
    ("台辅", "auxiliary", "土"),
    ("封诰", "auxiliary", "土"),
    ("红鸾", "romance", "水"),
    ("天喜", "romance", "水"),
    ("天德", "resolution", "火"),
    ("月德", "resolution", "火"),
    ("年解", "resolution", "木"),
    ("解神", "resolution", "木"),
    ("天伤", "auxiliary", None),
    ("天使", "auxiliary", None),
):
    STAR_METADATA[_name] = {
        "category": _category,
        "element": _element,
        "polarity": None,
    }

LU_CUN_BY_STEM = {
    "甲": "寅",
    "乙": "卯",
    "丙": "巳",
    "丁": "午",
    "戊": "巳",
    "己": "午",
    "庚": "申",
    "辛": "酉",
    "壬": "亥",
    "癸": "子",
}

KUI_YUE_BY_STEM = {
    "甲": ("丑", "未"),
    "乙": ("子", "申"),
    "丙": ("亥", "酉"),
    "丁": ("亥", "酉"),
    "戊": ("丑", "未"),
    "己": ("子", "申"),
    "庚": ("丑", "未"),
    "辛": ("午", "寅"),
    "壬": ("卯", "巳"),
    "癸": ("卯", "巳"),
}

TIAN_MA_BY_GROUP = {
    frozenset("寅午戌"): "申",
    frozenset("申子辰"): "寅",
    frozenset("巳酉丑"): "亥",
    frozenset("亥卯未"): "巳",
}

FIRE_BELL_STARTS = {
    frozenset("寅午戌"): ("丑", "卯"),
    frozenset("申子辰"): ("寅", "戌"),
    frozenset("巳酉丑"): ("卯", "戌"),
    frozenset("亥卯未"): ("酉", "戌"),
}

LIFE_CYCLE_START = {
    "水二局": "申",
    "木三局": "亥",
    "金四局": "巳",
    "土五局": "申",
    "火六局": "寅",
}

LIFE_CYCLE_NAMES = (
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
DOCTOR_CYCLE_NAMES = (
    "博士",
    "力士",
    "青龙",
    "小耗",
    "将军",
    "奏书",
    "飞廉",
    "喜神",
    "病符",
    "大耗",
    "伏兵",
    "官府",
)
YEAR_FRONT_CYCLE_NAMES = (
    "岁建",
    "晦气",
    "丧门",
    "贯索",
    "官符",
    "小耗",
    "大耗",
    "龙德",
    "白虎",
    "天德",
    "吊客",
    "病符",
)
GENERAL_FRONT_CYCLE_NAMES = (
    "将星",
    "攀鞍",
    "岁驿",
    "息神",
    "华盖",
    "劫煞",
    "灾煞",
    "天煞",
    "指背",
    "咸池",
    "月煞",
    "亡神",
)


def branch_index(branch: str) -> int:
    return BRANCH_INDEX[branch]


def group_value(branch: str, table: dict[frozenset[str], str | tuple[str, str]]):
    return next(value for group, value in table.items() if branch in group)


def place_cycle(names: Iterable[str], start_index: int, forward: bool) -> dict[int, list[str]]:
    result = {index: [] for index in range(12)}
    step = 1 if forward else -1
    for offset, name in enumerate(names):
        result[(start_index + step * offset) % 12].append(name)
    return result


def metadata(name: str) -> dict[str, str | None]:
    return STAR_METADATA.get(
        name,
        {"category": "cycle", "element": None, "polarity": None},
    )
