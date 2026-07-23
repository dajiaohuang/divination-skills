"""Calculate a bounded Chaibu Shijia Qimen foundation."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from lunar_python import Solar

from systems.bazi.calculator.engine import CalculationError, calculate_chart

SOURCE_ID = "SRC-QIMEN-PROJECT-SPEC-001"
STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
YANG_TERMS = (
    "冬至",
    "小寒",
    "大寒",
    "立春",
    "雨水",
    "惊蛰",
    "春分",
    "清明",
    "谷雨",
    "立夏",
    "小满",
    "芒种",
)
YIN_TERMS = (
    "夏至",
    "小暑",
    "大暑",
    "立秋",
    "处暑",
    "白露",
    "秋分",
    "寒露",
    "霜降",
    "立冬",
    "小雪",
    "大雪",
)
JU_TABLE = {
    "冬至": (1, 7, 4),
    "小寒": (2, 8, 5),
    "大寒": (3, 9, 6),
    "立春": (8, 5, 2),
    "雨水": (9, 6, 3),
    "惊蛰": (1, 7, 4),
    "春分": (3, 9, 6),
    "清明": (4, 1, 7),
    "谷雨": (5, 2, 8),
    "立夏": (4, 1, 7),
    "小满": (5, 2, 8),
    "芒种": (6, 3, 9),
    "夏至": (9, 3, 6),
    "小暑": (8, 2, 5),
    "大暑": (7, 1, 4),
    "立秋": (2, 5, 8),
    "处暑": (1, 4, 7),
    "白露": (9, 3, 6),
    "秋分": (7, 1, 4),
    "寒露": (6, 9, 3),
    "霜降": (5, 8, 2),
    "立冬": (6, 9, 3),
    "小雪": (5, 8, 2),
    "大雪": (4, 7, 1),
}
YUAN_NAMES = ("upper", "middle", "lower")
UPPER_BRANCHES = frozenset("子午卯酉")
MIDDLE_BRANCHES = frozenset("寅申巳亥")
LOWER_BRANCHES = frozenset("辰戌丑未")
EARTH_STEMS = tuple("戊己庚辛壬癸丁丙乙")
PALACE_GUA = {1: "坎", 2: "坤", 3: "震", 4: "巽", 5: "中", 6: "乾", 7: "兑", 8: "艮", 9: "离"}
ORIGINAL_STAR = {
    1: "天蓬",
    2: "天芮",
    3: "天冲",
    4: "天辅",
    5: "天禽",
    6: "天心",
    7: "天柱",
    8: "天任",
    9: "天英",
}
ORIGINAL_DOOR = {
    1: "休门",
    2: "死门",
    3: "伤门",
    4: "杜门",
    5: "中门",
    6: "开门",
    7: "惊门",
    8: "生门",
    9: "景门",
}
HIDDEN_JIA = {0: "戊", 1: "己", 2: "庚", 3: "辛", 4: "壬", 5: "癸"}


class QimenError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def yuan_from_day_index(day_index: int) -> dict[str, Any]:
    offset = day_index % 5
    head_index = (day_index - offset) % 60
    stem = STEMS[head_index % 10]
    branch = BRANCHES[head_index % 12]
    if branch in UPPER_BRANCHES:
        yuan_index = 0
    elif branch in MIDDLE_BRANCHES:
        yuan_index = 1
    elif branch in LOWER_BRANCHES:
        yuan_index = 2
    else:
        raise AssertionError("Unreachable yuan branch group.")
    return {
        "index": yuan_index,
        "name": YUAN_NAMES[yuan_index],
        "fu_head": f"{stem}{branch}",
        "fu_head_day_index": head_index,
        "days_from_fu_head": offset,
    }


def earth_plate(dun: str, ju: int) -> list[dict[str, Any]]:
    direction = 1 if dun == "yang" else -1
    stem_by_palace = {}
    for offset, stem in enumerate(EARTH_STEMS):
        palace = ((ju - 1 + direction * offset) % 9) + 1
        stem_by_palace[palace] = stem
    return [
        {
            "fact_id": f"qimen.earth.palace.{palace:03d}",
            "palace": palace,
            "gua": PALACE_GUA[palace],
            "earth_stem": stem_by_palace[palace],
            "original_star": ORIGINAL_STAR[palace],
            "original_door": ORIGINAL_DOOR[palace],
            "source_ids": [SOURCE_ID],
        }
        for palace in range(1, 10)
    ]


def calculate(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {"local_datetime", "timezone", "day_boundary", "fold"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise QimenError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    if "local_datetime" not in payload or "timezone" not in payload:
        raise QimenError("missing_time", "local_datetime and timezone are required.")
    calendar_payload = dict(payload)
    calendar_payload.setdefault("day_boundary", "midnight")
    try:
        calendar = calculate_chart(calendar_payload)
    except CalculationError as exc:
        raise QimenError(exc.code, exc.message) from exc
    beijing = datetime.fromisoformat(calendar["normalized_input"]["beijing_datetime"])
    solar = Solar.fromYmdHms(
        beijing.year, beijing.month, beijing.day, beijing.hour, beijing.minute, beijing.second
    )
    previous_term = solar.getLunar().getPrevJieQi(True)
    term_name = previous_term.getName()
    term_solar = previous_term.getSolar()
    if term_name not in JU_TABLE:
        raise QimenError("unsupported_solar_term", f"Unsupported solar term: {term_name}")
    dun = "yang" if term_name in YANG_TERMS else "yin"
    day = calendar["computed_facts"]["pillars"]["day"]
    hour = calendar["computed_facts"]["pillars"]["hour"]
    yuan = yuan_from_day_index(day["index"])
    ju = JU_TABLE[term_name][yuan["index"]]
    palaces = earth_plate(dun, ju)
    hour_xun_index = hour["index"] // 10
    xun_start_index = hour_xun_index * 10
    xun_start = f"{STEMS[xun_start_index % 10]}{BRANCHES[xun_start_index % 12]}"
    hidden_stem = HIDDEN_JIA[hour_xun_index]
    duty_origin = next(item for item in palaces if item["earth_stem"] == hidden_stem)
    center_host = 2 if duty_origin["palace"] == 5 else None
    term_datetime = (
        f"{term_solar.getYear():04d}-{term_solar.getMonth():02d}-{term_solar.getDay():02d}T"
        f"{term_solar.getHour():02d}:{term_solar.getMinute():02d}:{term_solar.getSecond():02d}+08:00"
    )
    return {
        "schema_version": "0.1.0",
        "engine": {
            "name": "divination-skills-qimen-foundation",
            "version": "0.1.0",
            "dependencies": {"lunar_python": "1.4.8"},
            "source_ids": [SOURCE_ID, *calendar["engine"]["source_ids"]],
        },
        "normalized_input": {
            "local_datetime": calendar["normalized_input"]["local_datetime"],
            "utc_datetime": calendar["normalized_input"]["utc_datetime"],
            "beijing_datetime": calendar["normalized_input"]["beijing_datetime"],
            "timezone": calendar["normalized_input"]["timezone"],
            "day_boundary": calendar["normalized_input"]["day_boundary"],
            "lineage": "shijia-zhuanpan-chaibu-v0.1",
        },
        "computed_facts": {
            "solar_term": {"name": term_name, "beijing_datetime": term_datetime},
            "dun": dun,
            "yuan": yuan,
            "ju": ju,
            "ju_label": f"{dun}-{ju}",
            "day_pillar": day,
            "hour_pillar": hour,
            "earth_plate": palaces,
            "hour_xun": {
                "start": xun_start,
                "hidden_jia_stem": hidden_stem,
                "source_ids": [SOURCE_ID],
            },
            "duty_origin": {
                "palace": duty_origin["palace"],
                "gua": duty_origin["gua"],
                "star": duty_origin["original_star"],
                "door": duty_origin["original_door"],
                "center_host_palace": center_host,
                "source_ids": [SOURCE_ID],
            },
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {
            "status": "valid",
            "warnings": [
                *calendar["validation"]["warnings"],
                {
                    "code": "foundation_only",
                    "message": "Heaven, rotating star/door, and spirit plates are not implemented.",
                },
            ],
        },
    }


def explain(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Qimen foundation is required.")
    report = deepcopy(result)
    original = deepcopy(result["computed_facts"])
    facts = result["computed_facts"]
    earth_ids = [item["fact_id"] for item in facts["earth_plate"]]
    report["derived_findings"] = [
        {
            "finding_id": "qimen.finding.ju.001",
            "fact_ids": [facts["day_pillar"]["fact_id"], facts["hour_pillar"]["fact_id"]],
            "rule_ids": ["QIMEN-CHAIBU-JU-001"],
            "confidence": "medium",
            "value": facts["ju_label"],
            "source_ids": [SOURCE_ID],
        },
        {
            "finding_id": "qimen.finding.earth.001",
            "fact_ids": earth_ids,
            "rule_ids": ["QIMEN-EARTH-PLATE-001", "QIMEN-DUTY-ORIGIN-001"],
            "confidence": "medium",
            "source_ids": [SOURCE_ID],
        },
    ]
    report["narrative"] = {
        "foundation": {
            "fact_ids": earth_ids,
            "rule_ids": ["QIMEN-FOUNDATION-BOUNDARY-001"],
            "statement": (
                f"{facts['solar_term']['name']} uses {facts['yuan']['name']} yuan, "
                f"{facts['dun']} dun {facts['ju']} ju. This is an earth-plate foundation only."
            ),
        },
        "limitations": [
            "No heaven, rotating star/door, or spirit plate is present.",
            "No 用神, direction, event, outcome, or timing judgment is supported.",
        ],
    }
    if report["computed_facts"] != original:
        raise AssertionError("Qimen explanation must not mutate calculation facts.")
    return report
