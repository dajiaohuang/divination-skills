from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from divination_skills.auditable_draw import build_symbol_report, draw_symbols

SPREADS = {"single": ("focus",), "three-rune": ("context", "tension", "practice")}
SOURCE = "SRC-RUNES-PROJECT-SPEC-001"
UNICODE_SOURCE = "SRC-RUNES-UNICODE-001"
HISTORICAL_SOURCE = "SRC-RUNES-SHM-KYLVER-001"
RUNE_GRAPHEMES = {
    "Fehu": ("ᚠ", "U+16A0", "RUNIC LETTER FEHU FEOH FE F", "f"),
    "Uruz": ("ᚢ", "U+16A2", "RUNIC LETTER URUZ UR U", "u"),
    "Thurisaz": ("ᚦ", "U+16A6", "RUNIC LETTER THURISAZ THURS THORN", "th"),
    "Ansuz": ("ᚨ", "U+16A8", "RUNIC LETTER ANSUZ A", "a"),
    "Raidho": ("ᚱ", "U+16B1", "RUNIC LETTER RAIDO RAD REID R", "r"),
    "Kenaz": ("ᚲ", "U+16B2", "RUNIC LETTER KAUNA", "k"),
    "Gebo": ("ᚷ", "U+16B7", "RUNIC LETTER GEBO GYFU G", "g"),
    "Wunjo": ("ᚹ", "U+16B9", "RUNIC LETTER WUNJO WYNN W", "w"),
    "Hagalaz": ("ᚺ", "U+16BA", "RUNIC LETTER HAGLAZ H", "h"),
    "Nauthiz": ("ᚾ", "U+16BE", "RUNIC LETTER NAUDIZ NYD NAUD N", "n"),
    "Isa": ("ᛁ", "U+16C1", "RUNIC LETTER ISAZ IS ISS I", "i"),
    "Jera": ("ᛃ", "U+16C3", "RUNIC LETTER JERAN J", "j"),
    "Eihwaz": ("ᛇ", "U+16C7", "RUNIC LETTER IWAZ EOH", "ï"),
    "Perthro": ("ᛈ", "U+16C8", "RUNIC LETTER PERTHO PEORTH P", "p"),
    "Algiz": ("ᛉ", "U+16C9", "RUNIC LETTER ALGIZ EOLHX", "z"),
    "Sowilo": ("ᛊ", "U+16CA", "RUNIC LETTER SOWILO S", "s"),
    "Tiwaz": ("ᛏ", "U+16CF", "RUNIC LETTER TIWAZ TIR TYR T", "t"),
    "Berkano": ("ᛒ", "U+16D2", "RUNIC LETTER BERKANAN BEORC BJARKAN B", "b"),
    "Ehwaz": ("ᛖ", "U+16D6", "RUNIC LETTER EHWAZ EH E", "e"),
    "Mannaz": ("ᛗ", "U+16D7", "RUNIC LETTER MANNAZ MAN M", "m"),
    "Laguz": ("ᛚ", "U+16DA", "RUNIC LETTER LAUKAZ LAGU LOGR L", "l"),
    "Ingwaz": ("ᛜ", "U+16DC", "RUNIC LETTER INGWAZ", "ng"),
    "Dagaz": ("ᛞ", "U+16DE", "RUNIC LETTER DAGAZ DAEG D", "d"),
    "Othala": ("ᛟ", "U+16DF", "RUNIC LETTER OTHALAN ETHEL O", "o"),
}


@lru_cache(maxsize=1)
def items() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parent / "data" / "deck.json"
    return json.loads(path.read_text(encoding="utf-8"))


def draw(payload: dict[str, Any]) -> dict[str, Any]:
    result = draw_symbols(
        payload,
        system="runes",
        lineage="elder-futhark-project-v0.3",
        items=items(),
        spreads=SPREADS,
        source_id=SOURCE,
        draw_rule_id="RUNES-DRAW-UNIQUE-001",
        identity_rule_id="RUNES-GRAPHEME-IDENTITY-001",
    )
    result["schema_version"] = "0.3.0"
    result["engine"]["version"] = "0.3.0"
    result["engine"]["source_ids"] = [SOURCE, UNICODE_SOURCE, HISTORICAL_SOURCE]
    for fact in result["computed_facts"]["symbols"]:
        character, codepoint, unicode_name, transliteration = RUNE_GRAPHEMES[fact["name"]]
        fact["character"] = character
        fact["codepoint"] = codepoint
        fact["unicode_name"] = unicode_name
        fact["transliteration"] = transliteration
        fact["identity_lineage"] = "elder-futhark-grapheme-v0.3"
        fact["grapheme_policy"] = "project_canonical_unicode_scalar"
        fact["source_ids"] = [SOURCE, UNICODE_SOURCE, HISTORICAL_SOURCE]
    return result


def explain(value: dict[str, Any]) -> dict[str, Any]:
    return build_symbol_report(
        value,
        items=items(),
        system="runes",
        source_id=SOURCE,
        orientation_rule="RUNES-SYMBOL-UPRIGHT-001",
        position_rule="RUNES-POSITION-001",
        sequence_rule="RUNES-SEQUENCE-001",
    )
