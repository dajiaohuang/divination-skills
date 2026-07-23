"""Stable Ziwei term identifiers separated from display labels."""

from __future__ import annotations

PALACE_TERM_IDS = {
    "命宫": "ziwei.palace.life",
    "兄弟": "ziwei.palace.siblings",
    "夫妻": "ziwei.palace.spouse",
    "子女": "ziwei.palace.children",
    "财帛": "ziwei.palace.wealth",
    "疾厄": "ziwei.palace.health",
    "迁移": "ziwei.palace.travel",
    "仆役": "ziwei.palace.associates",
    "官禄": "ziwei.palace.career",
    "田宅": "ziwei.palace.property",
    "福德": "ziwei.palace.wellbeing",
    "父母": "ziwei.palace.parents",
}

DISPLAY_LABELS = {
    "zh-Hans": {term_id: label for label, term_id in PALACE_TERM_IDS.items()},
    "zh-Hant": {
        **{term_id: label for label, term_id in PALACE_TERM_IDS.items()},
        "ziwei.palace.life": "命宮",
        "ziwei.palace.siblings": "兄弟",
        "ziwei.palace.spouse": "夫妻",
        "ziwei.palace.children": "子女",
        "ziwei.palace.wealth": "財帛",
        "ziwei.palace.health": "疾厄",
        "ziwei.palace.travel": "遷移",
        "ziwei.palace.associates": "僕役",
        "ziwei.palace.career": "官祿",
        "ziwei.palace.property": "田宅",
        "ziwei.palace.wellbeing": "福德",
        "ziwei.palace.parents": "父母",
    },
    "en": {
        "ziwei.palace.life": "Life",
        "ziwei.palace.siblings": "Siblings",
        "ziwei.palace.spouse": "Spouse",
        "ziwei.palace.children": "Children",
        "ziwei.palace.wealth": "Wealth",
        "ziwei.palace.health": "Health",
        "ziwei.palace.travel": "Travel",
        "ziwei.palace.associates": "Associates",
        "ziwei.palace.career": "Career",
        "ziwei.palace.property": "Property",
        "ziwei.palace.wellbeing": "Wellbeing",
        "ziwei.palace.parents": "Parents",
    },
}


def display_label(term_id: str, locale: str = "zh-Hans") -> str:
    try:
        return DISPLAY_LABELS[locale][term_id]
    except KeyError as exc:
        raise ValueError(f"Unsupported Ziwei term or locale: {term_id!r}, {locale!r}") from exc
