"""Generate original text-only Lenormand and Elder Futhark data files."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LENORMAND = [
    ("Rider", "news", "arrival", "movement"),
    ("Clover", "small chance", "brief ease", "lightness"),
    ("Ship", "distance", "journey", "expansion"),
    ("House", "home", "stability", "private structure"),
    ("Tree", "slow growth", "roots", "wellbeing context"),
    ("Clouds", "confusion", "mixed visibility", "temporary uncertainty"),
    ("Snake", "complexity", "indirect route", "careful strategy"),
    ("Coffin", "closure", "pause", "ending"),
    ("Bouquet", "appreciation", "gift", "pleasant invitation"),
    ("Scythe", "quick cut", "sudden choice", "sharp boundary"),
    ("Whip", "repetition", "debate", "friction"),
    ("Birds", "conversation", "nervous activity", "paired exchange"),
    ("Child", "small beginning", "novelty", "simplicity"),
    ("Fox", "self-interest", "work tactic", "verification"),
    ("Bear", "power", "protection", "resource control"),
    ("Stars", "orientation", "pattern", "hopeful direction"),
    ("Stork", "change", "relocation", "improvement effort"),
    ("Dog", "loyalty", "support", "trusted connection"),
    ("Tower", "institution", "distance", "formal boundary"),
    ("Garden", "public space", "network", "gathering"),
    ("Mountain", "obstacle", "delay", "large constraint"),
    ("Crossroads", "options", "choice", "diverging path"),
    ("Mice", "erosion", "worry", "small losses"),
    ("Heart", "affection", "desire", "valued connection"),
    ("Ring", "agreement", "cycle", "commitment"),
    ("Book", "unknown information", "study", "privacy"),
    ("Letter", "message", "document", "record"),
    ("Man", "person marker", "social role", "human agency"),
    ("Woman", "person marker", "social role", "human agency"),
    ("Lily", "maturity", "peace", "long practice"),
    ("Sun", "clarity", "energy", "visible success"),
    ("Moon", "recognition", "sensitivity", "rhythm"),
    ("Key", "solution", "access", "importance"),
    ("Fish", "flow", "trade", "resources"),
    ("Anchor", "stability", "work", "long duration"),
    ("Cross", "burden", "meaningful difficulty", "duty"),
]

RUNES = [
    ("Fehu", "movable resources", "exchange", "stewardship"),
    ("Uruz", "vital force", "endurance", "shaping effort"),
    ("Thurisaz", "threshold", "defense", "disruptive force"),
    ("Ansuz", "speech", "signal", "learning"),
    ("Raidho", "journey", "orderly movement", "right timing"),
    ("Kenaz", "illumination", "craft", "revealed pattern"),
    ("Gebo", "gift", "reciprocity", "balanced exchange"),
    ("Wunjo", "belonging", "satisfaction", "shared harmony"),
    ("Hagalaz", "disruption", "uncontrolled condition", "restructuring"),
    ("Nauthiz", "need", "constraint", "disciplined response"),
    ("Isa", "stillness", "concentration", "delay"),
    ("Jera", "cycle", "harvest", "earned timing"),
    ("Eihwaz", "endurance", "axis", "transition"),
    ("Perthro", "uncertainty", "lot", "hidden process"),
    ("Algiz", "protection", "alertness", "boundary"),
    ("Sowilo", "clarity", "direction", "integrity"),
    ("Tiwaz", "principle", "courage", "fair sacrifice"),
    ("Berkano", "growth", "care", "renewal"),
    ("Ehwaz", "coordinated movement", "trust", "partnership"),
    ("Mannaz", "human context", "self-knowledge", "community"),
    ("Laguz", "flow", "feeling", "adaptation"),
    ("Ingwaz", "stored potential", "gestation", "completion within"),
    ("Dagaz", "breakthrough", "daylight", "changed perspective"),
    ("Othala", "inheritance", "home ground", "responsible legacy"),
]


def write(system: str, values: list[tuple[str, str, str, str]]) -> None:
    cards = [
        {
            "symbol_id": f"{system}.{number:02d}.{name.lower()}",
            "number": number,
            "name": name,
            "upright": [first, second, third],
            "reversed": [first, second, third],
        }
        for number, (name, first, second, third) in enumerate(values, start=1)
    ]
    path = ROOT / "systems" / system / "data" / "deck.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(cards, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    write("lenormand", LENORMAND)
    write("runes", RUNES)
    print("Generated Lenormand 36 and Elder Futhark 24 text symbols.")


if __name__ == "__main__":
    main()
