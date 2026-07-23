"""Project-native rotating-plate Qimen chart completion."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from systems.qimen.engine import (
    ORIGINAL_DOOR,
    ORIGINAL_STAR,
    PALACE_GUA,
    SOURCE_ID,
    calculate,
)

LINEAGE = "shijia-zhuanpan-chaibu-full-v0.2"
RING = (1, 8, 3, 4, 9, 2, 7, 6)
PALACE_BRANCHES = {
    1: ("子",),
    2: ("未", "申"),
    3: ("卯",),
    4: ("辰", "巳"),
    5: (),
    6: ("戌", "亥"),
    7: ("酉",),
    8: ("丑", "寅"),
    9: ("午",),
}
PALACE_ELEMENT = {
    1: "water",
    2: "earth",
    3: "wood",
    4: "wood",
    5: "earth",
    6: "metal",
    7: "metal",
    8: "earth",
    9: "fire",
}
STEM_ELEMENT = {
    "甲": "wood",
    "乙": "wood",
    "丙": "fire",
    "丁": "fire",
    "戊": "earth",
    "己": "earth",
    "庚": "metal",
    "辛": "metal",
    "壬": "water",
    "癸": "water",
}
DOOR_ELEMENT = {
    "休门": "water",
    "生门": "earth",
    "伤门": "wood",
    "杜门": "wood",
    "景门": "fire",
    "死门": "earth",
    "惊门": "metal",
    "开门": "metal",
}
ELEMENT_CONTROLS = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood",
}
TOMB_PALACE_BY_ELEMENT = {
    "wood": 2,
    "fire": 6,
    "earth": 6,
    "metal": 8,
    "water": 4,
}
INSTRUMENT_PUNISHMENT_PALACE = {
    "戊": 3,
    "己": 2,
    "庚": 8,
    "辛": 9,
    "壬": 4,
    "癸": 4,
}
SPIRITS = ("值符", "螣蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天")


def _effective_palace(palace: int) -> int:
    return 2 if palace == 5 else palace


def _ring_shift(palace: int, steps: int) -> int:
    effective = _effective_palace(palace)
    return RING[(RING.index(effective) + steps) % len(RING)]


def _void_branches(hour_index: int) -> list[str]:
    branches = tuple("子丑寅卯辰巳午未申酉戌亥")
    start_branch = ((hour_index // 10) * 10) % 12
    return [branches[(start_branch + 10) % 12], branches[(start_branch + 11) % 12]]


def calculate_full(payload: dict[str, Any]) -> dict[str, Any]:
    """Calculate all nine project plate facts without interpreting an outcome."""

    foundation = calculate(payload)
    original = deepcopy(foundation["computed_facts"])
    facts = foundation["computed_facts"]
    earth_by_palace = {item["palace"]: item for item in facts["earth_plate"]}
    hour = facts["hour_pillar"]
    hidden = facts["hour_xun"]["hidden_jia_stem"]
    hour_stem = hour["stem"]["name"]
    instrument = hidden if hour_stem == "甲" else hour_stem
    instrument_origin = next(
        item["palace"] for item in facts["earth_plate"] if item["earth_stem"] == instrument
    )
    duty_origin = facts["duty_origin"]["palace"]
    star_shift = (
        RING.index(_effective_palace(instrument_origin))
        - RING.index(_effective_palace(duty_origin))
    )
    star_targets = {
        source: _ring_shift(source, star_shift)
        for source in RING
    }
    center_star_target = star_targets[2]

    xun_start_index = (hour["index"] // 10) * 10
    hour_step = hour["index"] - xun_start_index
    rotation_direction = 1 if facts["dun"] == "yang" else -1
    duty_door_target = _ring_shift(duty_origin, rotation_direction * hour_step)
    door_shift = (
        RING.index(duty_door_target) - RING.index(_effective_palace(duty_origin))
    )
    door_targets = {source: _ring_shift(source, door_shift) for source in RING}

    void = _void_branches(hour["index"])
    plate = {
        palace: {
            "fact_id": f"qimen.full.palace.{palace:03d}",
            "palace": palace,
            "gua": PALACE_GUA[palace],
            "branches": list(PALACE_BRANCHES[palace]),
            "earth_stem": earth_by_palace[palace]["earth_stem"],
            "heaven_stems": [],
            "stars": [],
            "doors": [],
            "spirits": [],
            "is_void": bool(set(PALACE_BRANCHES[palace]) & set(void)),
            "tomb_entries": [],
            "instrument_punishments": [],
            "door_oppressions": [],
            "rule_ids": [
                "QIMEN-HEAVEN-STAR-PLATE-001",
                "QIMEN-DOOR-SPIRIT-PLATE-001",
                "QIMEN-STATE-MARKERS-001",
            ],
            "source_ids": [SOURCE_ID],
        }
        for palace in range(1, 10)
    }

    for source in RING:
        target = star_targets[source]
        plate[target]["heaven_stems"].append(
            {
                "stem": earth_by_palace[source]["earth_stem"],
                "source_palace": source,
                "center_hosted": False,
            }
        )
        plate[target]["stars"].append(
            {
                "name": ORIGINAL_STAR[source],
                "source_palace": source,
                "duty": source == _effective_palace(duty_origin),
                "center_hosted": False,
            }
        )
    plate[center_star_target]["heaven_stems"].append(
        {
            "stem": earth_by_palace[5]["earth_stem"],
            "source_palace": 5,
            "center_hosted": True,
        }
    )
    plate[center_star_target]["stars"].append(
        {
            "name": ORIGINAL_STAR[5],
            "source_palace": 5,
            "duty": duty_origin == 5,
            "center_hosted": True,
        }
    )
    for source in RING:
        target = door_targets[source]
        plate[target]["doors"].append(
            {
                "name": ORIGINAL_DOOR[source],
                "source_palace": source,
                "duty": source == _effective_palace(duty_origin),
            }
        )
    duty_star_target = star_targets[_effective_palace(duty_origin)]
    for offset, spirit in enumerate(SPIRITS):
        target = _ring_shift(duty_star_target, rotation_direction * offset)
        plate[target]["spirits"].append({"name": spirit, "duty": offset == 0})

    for palace, item in plate.items():
        for stem in item["heaven_stems"]:
            if TOMB_PALACE_BY_ELEMENT[STEM_ELEMENT[stem["stem"]]] == palace:
                item["tomb_entries"].append(
                    {
                        "stem": stem["stem"],
                        "layer": "heaven",
                        "rule_id": "QIMEN-STATE-MARKERS-001",
                    }
                )
            if INSTRUMENT_PUNISHMENT_PALACE.get(stem["stem"]) == palace:
                item["instrument_punishments"].append(
                    {
                        "stem": stem["stem"],
                        "layer": "heaven",
                        "rule_id": "QIMEN-STATE-MARKERS-001",
                    }
                )
        earth_stem = item["earth_stem"]
        if TOMB_PALACE_BY_ELEMENT[STEM_ELEMENT[earth_stem]] == palace:
            item["tomb_entries"].append(
                {
                    "stem": earth_stem,
                    "layer": "earth",
                    "rule_id": "QIMEN-STATE-MARKERS-001",
                }
            )
        for door in item["doors"]:
            if ELEMENT_CONTROLS[DOOR_ELEMENT[door["name"]]] == PALACE_ELEMENT[palace]:
                item["door_oppressions"].append(
                    {
                        "door": door["name"],
                        "palace": palace,
                        "rule_id": "QIMEN-STATE-MARKERS-001",
                    }
                )

    if foundation["computed_facts"] != original:
        raise AssertionError("Full-chart extension must not mutate foundation facts.")
    return {
        "schema_version": "0.2.0",
        "system": "qimen",
        "lineage": LINEAGE,
        "foundation": foundation,
        "rotation": {
            "hour_instrument": instrument,
            "hour_instrument_earth_palace": instrument_origin,
            "duty_star_origin_palace": duty_origin,
            "duty_star_target_palace": duty_star_target,
            "duty_door_origin_palace": duty_origin,
            "duty_door_target_palace": duty_door_target,
            "rotation_direction": facts["dun"],
            "hour_steps_from_xun_start": hour_step,
        },
        "void_branches": void,
        "palaces": [plate[palace] for palace in range(1, 10)],
        "conclusions": [
            {
                "conclusion_id": "qimen.full.structure.001",
                "statement": (
                    "The result records rotating plates and named state markers only; "
                    "it does not select 用神 or infer direction, event, outcome, or timing."
                ),
                "fact_ids": [plate[palace]["fact_id"] for palace in range(1, 10)],
                "rule_ids": [
                    "QIMEN-HEAVEN-STAR-PLATE-001",
                    "QIMEN-DOOR-SPIRIT-PLATE-001",
                    "QIMEN-STATE-MARKERS-001",
                ],
                "source_ids": [SOURCE_ID],
                "support": ["All nine palaces are produced by one declared rotation policy."],
                "counterevidence": [
                    "Other Qimen schools use different ju, hosting, rotation, or marker policies."
                ],
                "limitations": [
                    "The v0.2 rotation policy awaits independent practitioner acceptance.",
                    "No symbolic marker is converted into a factual or predictive claim.",
                ],
            }
        ],
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "full_plate_pending_domain_review",
                    "message": "The full project rotation policy awaits practitioner review.",
                }
            ],
        },
    }
