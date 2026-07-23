"""Wen Wang Liuyao structural calculation over an auditable I Ching cast."""

from __future__ import annotations

import hashlib
from copy import deepcopy
from typing import Any

from systems.bazi.calculator.engine import CalculationError, calculate_chart
from systems.iching.engine import CastError, cast

SOURCE_ID = "SRC-LIUYAO-PROJECT-SPEC-001"
STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
BRANCH_ELEMENT = {
    "子": "water",
    "亥": "water",
    "寅": "wood",
    "卯": "wood",
    "巳": "fire",
    "午": "fire",
    "辰": "earth",
    "戌": "earth",
    "丑": "earth",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
}
ELEMENT_GENERATES = {
    "wood": "fire",
    "fire": "earth",
    "earth": "metal",
    "metal": "water",
    "water": "wood",
}
ELEMENT_CONTROLS = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood",
}
PALACE_SEQUENCES = {
    "qian": [1, 44, 33, 12, 20, 23, 35, 14],
    "kun": [2, 24, 19, 11, 34, 43, 5, 8],
    "zhen": [51, 16, 40, 32, 46, 48, 28, 17],
    "xun": [57, 9, 37, 42, 25, 21, 27, 18],
    "kan": [29, 60, 3, 63, 49, 55, 36, 7],
    "li": [30, 56, 50, 64, 4, 59, 6, 13],
    "gen": [52, 22, 26, 41, 38, 10, 61, 53],
    "dui": [58, 47, 45, 31, 39, 15, 62, 54],
}
PALACE_ELEMENT = {
    "qian": "metal",
    "dui": "metal",
    "zhen": "wood",
    "xun": "wood",
    "kan": "water",
    "li": "fire",
    "gen": "earth",
    "kun": "earth",
}
PALACE_STAGE = (
    "pure",
    "first-change",
    "second-change",
    "third-change",
    "fourth-change",
    "fifth-change",
    "wandering-soul",
    "returning-soul",
)
SHI_YING = ((6, 3), (1, 4), (2, 5), (3, 6), (4, 1), (5, 2), (4, 1), (3, 6))
NAJIA = {
    "qian": {"inner": ("甲子", "甲寅", "甲辰"), "outer": ("壬午", "壬申", "壬戌")},
    "kun": {"inner": ("乙未", "乙巳", "乙卯"), "outer": ("癸丑", "癸亥", "癸酉")},
    "zhen": {"inner": ("庚子", "庚寅", "庚辰"), "outer": ("庚午", "庚申", "庚戌")},
    "xun": {"inner": ("辛丑", "辛亥", "辛酉"), "outer": ("辛未", "辛巳", "辛卯")},
    "kan": {"inner": ("戊寅", "戊辰", "戊午"), "outer": ("戊申", "戊戌", "戊子")},
    "li": {"inner": ("己卯", "己丑", "己亥"), "outer": ("己酉", "己未", "己巳")},
    "gen": {"inner": ("丙辰", "丙午", "丙申"), "outer": ("丙戌", "丙子", "丙寅")},
    "dui": {"inner": ("丁巳", "丁卯", "丁丑"), "outer": ("丁亥", "丁酉", "丁未")},
}
SIX_SPIRITS = ("青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武")
SPIRIT_START = {
    "甲": 0,
    "乙": 0,
    "丙": 1,
    "丁": 1,
    "戊": 2,
    "己": 3,
    "庚": 4,
    "辛": 4,
    "壬": 5,
    "癸": 5,
}


class LiuyaoError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def palace_for(number: int) -> tuple[str, int]:
    for palace, sequence in PALACE_SEQUENCES.items():
        if number in sequence:
            return palace, sequence.index(number)
    raise LiuyaoError("unknown_hexagram", f"Hexagram {number} is absent from eight palaces.")


def six_relative(palace_element: str, line_element: str) -> str:
    if line_element == palace_element:
        return "兄弟"
    if ELEMENT_GENERATES[line_element] == palace_element:
        return "父母"
    if ELEMENT_GENERATES[palace_element] == line_element:
        return "子孙"
    if ELEMENT_CONTROLS[palace_element] == line_element:
        return "妻财"
    if ELEMENT_CONTROLS[line_element] == palace_element:
        return "官鬼"
    raise AssertionError("Unreachable five-element relation.")


def void_branches(day_index: int) -> list[str]:
    xun_start_branch = ((day_index // 10) * 10) % 12
    return [BRANCHES[(xun_start_branch + 10) % 12], BRANCHES[(xun_start_branch + 11) % 12]]


def calculate(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {"question", "seed_hex", "local_datetime", "timezone", "day_boundary", "fold"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise LiuyaoError("unknown_fields", f"Unknown field(s): {', '.join(unknown)}")
    if "local_datetime" not in payload or "timezone" not in payload:
        raise LiuyaoError("missing_time", "local_datetime and timezone are required.")
    cast_payload = {key: payload[key] for key in ("question", "seed_hex") if key in payload}
    calendar_payload = {
        key: payload[key]
        for key in ("local_datetime", "timezone", "day_boundary", "fold")
        if key in payload
    }
    calendar_payload.setdefault("day_boundary", "midnight")
    try:
        cast_result = cast(cast_payload)
        calendar = calculate_chart(calendar_payload)
    except (CastError, CalculationError) as exc:
        raise LiuyaoError(exc.code, exc.message) from exc

    primary = cast_result["computed_facts"]["primary_hexagram"]
    palace, stage_index = palace_for(primary["number"])
    palace_element = PALACE_ELEMENT[palace]
    shi, ying = SHI_YING[stage_index]
    lower = primary["lower_trigram"]["id"]
    upper = primary["upper_trigram"]["id"]
    assignments = [*NAJIA[lower]["inner"], *NAJIA[upper]["outer"]]
    day = calendar["computed_facts"]["pillars"]["day"]
    month = calendar["computed_facts"]["pillars"]["month"]
    spirit_start = SPIRIT_START[day["stem"]["name"]]
    lines = []
    for index, (cast_line, ganzhi) in enumerate(
        zip(cast_result["computed_facts"]["lines"], assignments, strict=True), start=1
    ):
        stem, branch = ganzhi
        line_element = BRANCH_ELEMENT[branch]
        lines.append(
            {
                **cast_line,
                "najia": {
                    "stem": stem,
                    "branch": branch,
                    "ganzhi": ganzhi,
                    "element": line_element,
                },
                "six_relative": six_relative(palace_element, line_element),
                "six_spirit": SIX_SPIRITS[(spirit_start + index - 1) % 6],
                "role": "shi" if index == shi else "ying" if index == ying else None,
                "is_void": branch in void_branches(day["index"]),
                "source_ids": [SOURCE_ID],
            }
        )
    question = payload.get("question", "")
    return {
        "schema_version": "0.1.0",
        "engine": {
            "name": "divination-skills-liuyao",
            "version": "0.1.0",
            "source_ids": [SOURCE_ID, *calendar["engine"]["source_ids"]],
        },
        "normalized_input": {
            "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
            "local_datetime": calendar["normalized_input"]["local_datetime"],
            "utc_datetime": calendar["normalized_input"]["utc_datetime"],
            "timezone": calendar["normalized_input"]["timezone"],
            "day_boundary": calendar["normalized_input"]["day_boundary"],
            "lineage": "wen-wang-najia-structural-v0.1",
        },
        "audit": cast_result["audit"],
        "computed_facts": {
            "primary_hexagram": primary,
            "changed_hexagram": cast_result["computed_facts"]["changed_hexagram"],
            "moving_line_positions": cast_result["computed_facts"]["moving_line_positions"],
            "palace": {
                "id": palace,
                "element": palace_element,
                "stage": PALACE_STAGE[stage_index],
                "stage_index": stage_index,
                "shi_position": shi,
                "ying_position": ying,
                "source_ids": [SOURCE_ID],
            },
            "calendar_context": {
                "month_commander": month["branch"],
                "day_pillar": day,
                "void_branches": void_branches(day["index"]),
            },
            "lines": lines,
        },
        "derived_findings": [],
        "narrative": None,
        "validation": {
            "status": "valid",
            "warnings": [
                *cast_result["validation"]["warnings"],
                *calendar["validation"]["warnings"],
                {
                    "code": "structural_only",
                    "message": "No 用神, 旺衰, outcome, or timing judgment is produced in v0.1.",
                },
            ],
        },
    }


def explain(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid Liuyao calculation is required.")
    report = deepcopy(result)
    original = deepcopy(result["computed_facts"])
    facts = result["computed_facts"]
    fact_ids = [line["fact_id"] for line in facts["lines"]]
    report["derived_findings"] = [
        {
            "finding_id": "liuyao.finding.structure.001",
            "fact_ids": fact_ids,
            "rule_ids": ["LIUYAO-NAJIA-001", "LIUYAO-PALACE-SHIYING-001"],
            "confidence": "high",
            "source_ids": [SOURCE_ID],
        },
        {
            "finding_id": "liuyao.finding.context.001",
            "fact_ids": [facts["calendar_context"]["day_pillar"]["fact_id"]],
            "rule_ids": ["LIUYAO-CALENDAR-CONTEXT-001"],
            "confidence": "high",
            "source_ids": [SOURCE_ID],
        },
    ]
    report["narrative"] = {
        "structure": {
            "fact_ids": fact_ids,
            "rule_ids": ["LIUYAO-STRUCTURAL-BOUNDARY-001"],
            "statement": (
                f"Hexagram {facts['primary_hexagram']['number']} belongs to the "
                f"{facts['palace']['id']} palace ({facts['palace']['stage']}); 世 is line "
                f"{facts['palace']['shi_position']} and 应 is line "
                f"{facts['palace']['ying_position']}."
            ),
        },
        "limitations": [
            "This report calculates structure only and does not select 用神.",
            "No 旺衰, event outcome, or response-time claim is made.",
        ],
    }
    if report["computed_facts"] != original:
        raise AssertionError("Liuyao explanation must not mutate calculation facts.")
    return report
