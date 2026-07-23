"""Project-native Ziwei star metadata and deterministic placement tables.

The catalog stores calculation facts, not copied prose or interpretive meanings.
"""

from __future__ import annotations

from collections.abc import Iterable

CLASSICAL_SOURCE_ID = "SRC-ZIWEI-QUANSHU-001"
PROJECT_SOURCE_ID = "SRC-ZIWEI-PROJECT-SPEC-001"

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
