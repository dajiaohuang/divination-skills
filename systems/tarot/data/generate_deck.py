"""Generate the project-authored text-only 78-card deck."""

from __future__ import annotations

import json
from pathlib import Path

MAJORS = [
    (
        "The Fool",
        ["openness", "first step", "curiosity"],
        ["hesitation", "heedlessness", "unfocused risk"],
    ),
    (
        "The Magician",
        ["initiative", "skillful action", "focused resources"],
        ["misapplied skill", "scattered intent", "appearance over substance"],
    ),
    (
        "The High Priestess",
        ["quiet knowing", "receptivity", "unspoken context"],
        ["ignored intuition", "withheld context", "inner noise"],
    ),
    (
        "The Empress",
        ["nurturing growth", "abundance", "embodied creativity"],
        ["overgiving", "stalled growth", "neglected needs"],
    ),
    (
        "The Emperor",
        ["structure", "responsibility", "clear authority"],
        ["rigidity", "control struggle", "weak boundaries"],
    ),
    (
        "The Hierophant",
        ["shared tradition", "teaching", "established method"],
        ["questioned convention", "empty conformity", "independent learning"],
    ),
    (
        "The Lovers",
        ["chosen alignment", "relationship", "values in action"],
        ["misalignment", "avoidance of choice", "conflicting values"],
    ),
    (
        "The Chariot",
        ["directed movement", "self-command", "commitment"],
        ["loss of direction", "forced progress", "divided will"],
    ),
    (
        "Strength",
        ["patient courage", "gentle influence", "self-trust"],
        ["self-doubt", "suppressed force", "fragile composure"],
    ),
    (
        "The Hermit",
        ["solitude", "careful inquiry", "inner guidance"],
        ["isolation", "avoidance", "refusal of counsel"],
    ),
    (
        "Wheel of Fortune",
        ["changing conditions", "cycle", "turning point"],
        ["resisted change", "repeating pattern", "poor timing"],
    ),
    (
        "Justice",
        ["accountability", "balanced judgment", "consequence"],
        ["bias", "avoided responsibility", "unequal terms"],
    ),
    (
        "The Hanged Man",
        ["pause", "changed perspective", "willing release"],
        ["stagnation", "needless sacrifice", "refusal to reframe"],
    ),
    (
        "Death",
        ["ending", "transition", "necessary clearing"],
        ["clinging", "unfinished ending", "delayed transition"],
    ),
    (
        "Temperance",
        ["integration", "measured adjustment", "sustainable rhythm"],
        ["excess", "poor mixture", "unstable pace"],
    ),
    (
        "The Devil",
        ["binding pattern", "compulsion", "material attachment"],
        ["recognizing a bind", "loosening attachment", "denied dependency"],
    ),
    (
        "The Tower",
        ["disruption", "revealed instability", "rapid restructuring"],
        ["avoided reckoning", "contained disruption", "fear of change"],
    ),
    (
        "The Star",
        ["renewal", "hopeful direction", "openness"],
        ["discouragement", "guarded hope", "lost orientation"],
    ),
    (
        "The Moon",
        ["ambiguity", "imagination", "uncertain signals"],
        ["clearing confusion", "denial of uncertainty", "distorted fear"],
    ),
    (
        "The Sun",
        ["clarity", "vitality", "shared confidence"],
        ["muted joy", "overexposure", "delayed clarity"],
    ),
    (
        "Judgement",
        ["reckoning", "renewed call", "integrated review"],
        ["self-condemnation", "ignored call", "unfinished review"],
    ),
    (
        "The World",
        ["completion", "integration", "wider context"],
        ["loose ends", "narrow horizon", "delayed completion"],
    ),
]

SUITS = {
    "wands": ("fire", "initiative", "energy", "purpose"),
    "cups": ("water", "feeling", "relationship", "receptivity"),
    "swords": ("air", "thought", "conflict", "communication"),
    "pentacles": ("earth", "resources", "craft", "material conditions"),
}

RANKS = [
    (
        "ace",
        "opening",
        "seed",
        "unused potential",
        "blocked start",
        "diffuse potential",
        "missed opening",
    ),
    ("two", "choice", "pairing", "balance", "indecision", "imbalance", "split attention"),
    (
        "three",
        "development",
        "collaboration",
        "first results",
        "poor coordination",
        "delayed growth",
        "third-factor tension",
    ),
    (
        "four",
        "stability",
        "boundary",
        "consolidation",
        "stagnation",
        "weak foundation",
        "overprotection",
    ),
    (
        "five",
        "friction",
        "adjustment",
        "challenge",
        "avoided conflict",
        "lingering strain",
        "unproductive contest",
    ),
    (
        "six",
        "exchange",
        "transition",
        "restored movement",
        "unequal exchange",
        "unfinished transition",
        "conditional support",
    ),
    (
        "seven",
        "assessment",
        "strategy",
        "testing resolve",
        "poor strategy",
        "defensiveness",
        "scattered effort",
    ),
    (
        "eight",
        "motion",
        "practice",
        "growing momentum",
        "delay",
        "repetition without learning",
        "misdirected speed",
    ),
    (
        "nine",
        "culmination",
        "resilience",
        "near completion",
        "fatigue",
        "guardedness",
        "fragile gains",
    ),
    (
        "ten",
        "completion",
        "full consequence",
        "handoff",
        "overload",
        "incomplete closure",
        "burdened outcome",
    ),
    (
        "page",
        "learning",
        "message",
        "fresh approach",
        "immaturity",
        "unclear message",
        "shallow curiosity",
    ),
    (
        "knight",
        "pursuit",
        "movement",
        "committed approach",
        "rash pursuit",
        "stalled action",
        "one-track focus",
    ),
    (
        "queen",
        "mature receptivity",
        "stewardship",
        "inner command",
        "overidentification",
        "withheld care",
        "insecure command",
    ),
    (
        "king",
        "mature direction",
        "responsibility",
        "outer command",
        "domination",
        "misused authority",
        "rigid direction",
    ),
]


def slug(value: str) -> str:
    return value.lower().replace(" ", "-")


def build_deck() -> dict:
    cards = []
    for index, (name, upright, reversed_) in enumerate(MAJORS):
        cards.append(
            {
                "card_id": f"tarot.rws.major-{index:02d}-{slug(name.removeprefix('The '))}",
                "index": index,
                "name": name,
                "arcana": "major",
                "suit": None,
                "rank": str(index),
                "element": None,
                "upright": upright,
                "reversed": reversed_,
            }
        )
    index = len(cards)
    for suit, (element, domain, process, context) in SUITS.items():
        for rank, up1, up2, up3, rev1, rev2, rev3 in RANKS:
            cards.append(
                {
                    "card_id": f"tarot.rws.{suit}-{rank}",
                    "index": index,
                    "name": f"{rank.title()} of {suit.title()}",
                    "arcana": "minor",
                    "suit": suit,
                    "rank": rank,
                    "element": element,
                    "upright": [
                        f"{up1} in {domain}",
                        f"{up2} through {process}",
                        f"{up3} around {context}",
                    ],
                    "reversed": [
                        f"{rev1} in {domain}",
                        f"{rev2} around {process}",
                        f"{rev3} in {context}",
                    ],
                }
            )
            index += 1
    return {
        "deck_id": "rws-text-78",
        "version": "0.1.0",
        "lineage": "rws-text-baseline-v0.1",
        "source_ids": ["SRC-TAROT-DECK-SPEC-001"],
        "cards": cards,
    }


def main() -> None:
    output = Path(__file__).resolve().parent / "rws-78.json"
    output.write_text(
        json.dumps(build_deck(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {len(build_deck()['cards'])} text-only cards.")


if __name__ == "__main__":
    main()
