"""Classical source locators and explicit moving-line selection policies."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

SOURCE_EDITIONS = {
    "gutenberg-chinese-25501": {
        "source_id": "SRC-ICHING-GUTENBERG-25501",
        "title": "易經",
        "edition_type": "public-domain Chinese transcription",
        "document_url": "https://www.gutenberg.org/ebooks/25501",
        "passage_status": "semantic_locator_available",
    },
    "song-wangbi-kongyingda-loc-17845": {
        "source_id": "SRC-ICHING-LOC-17845",
        "title": "周易注疏 : 十三卷",
        "edition_type": "Southern Song print with Wang Bi and Kong Yingda commentary",
        "document_url": "https://www.loc.gov/item/2021666491/",
        "passage_status": "image_collation_pending",
    },
}
POLICIES = {
    "all-moving-lines-v0.2",
    "zhu-xi-count-routing-v0.3",
}


def _unit(kind: str, hexagram_number: int, line_position: int | None = None) -> dict[str, Any]:
    value = {
        "unit_type": kind,
        "hexagram_number": hexagram_number,
        "logical_locator": f"King Wen hexagram {hexagram_number}",
    }
    if line_position is not None:
        value["line_position_from_bottom"] = line_position
        value["logical_locator"] += f", line {line_position}"
    return value


def select_reading_units(cast: dict[str, Any], *, policy_id: str) -> dict[str, Any]:
    """Select text units without reproducing or inventing any classical passage."""

    if cast.get("validation", {}).get("status") != "valid":
        raise ValueError("A valid I Ching cast is required.")
    if policy_id not in POLICIES:
        raise ValueError("policy_id must be one of: " + ", ".join(sorted(POLICIES)))
    facts = cast["computed_facts"]
    primary = facts["primary_hexagram"]["number"]
    changed = facts["changed_hexagram"]["number"]
    moving = facts["moving_line_positions"]
    count = len(moving)
    selected: list[dict[str, Any]]

    if policy_id == "all-moving-lines-v0.2":
        selected = [_unit("primary_judgment", primary)]
        selected.extend(_unit("primary_line", primary, position) for position in moving)
        if moving:
            selected.append(_unit("changed_judgment", changed))
    elif count == 0:
        selected = [_unit("primary_judgment", primary)]
    elif count == 1:
        selected = [_unit("primary_line", primary, moving[0])]
    elif count == 2:
        selected = [
            {**_unit("primary_line", primary, moving[0]), "emphasis": "secondary"},
            {**_unit("primary_line", primary, moving[1]), "emphasis": "primary"},
        ]
    elif count == 3:
        selected = [
            {**_unit("primary_judgment", primary), "emphasis": "present"},
            {**_unit("changed_judgment", changed), "emphasis": "change"},
        ]
    elif count == 4:
        static = [position for position in range(1, 7) if position not in moving]
        selected = [
            {**_unit("changed_line", changed, static[1]), "emphasis": "secondary"},
            {**_unit("changed_line", changed, static[0]), "emphasis": "primary"},
        ]
    elif count == 5:
        static = next(position for position in range(1, 7) if position not in moving)
        selected = [_unit("changed_line", changed, static)]
    elif primary == 1:
        selected = [_unit("use_nine", primary)]
    elif primary == 2:
        selected = [_unit("use_six", primary)]
    else:
        selected = [_unit("changed_judgment", changed)]

    rule_id = (
        "ICHING-MOVING-POLICY-ALL-001"
        if policy_id == "all-moving-lines-v0.2"
        else "ICHING-MOVING-POLICY-COUNT-001"
    )
    source_ids = ["SRC-ICHING-PROJECT-SPEC-001"]
    if policy_id == "zhu-xi-count-routing-v0.3":
        source_ids.append("SRC-ICHING-QIMENG-TONGSHI-001")
    return {
        "policy_id": policy_id,
        "moving_line_count": count,
        "moving_line_positions": moving,
        "selected_units": selected,
        "rule_ids": [rule_id],
        "source_ids": source_ids,
        "limitations": [
            "Selection identifies passages; it does not supply an interpretation or outcome.",
            "The count-routing policy is lineage-specific and is never silently merged "
            "with alternatives.",
        ],
    }


def build_classical_layer(
    cast: dict[str, Any],
    *,
    policy_id: str = "all-moving-lines-v0.2",
    edition_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Attach edition-aware locators while retaining an explicit not-collated status."""

    original = deepcopy(cast["computed_facts"])
    reading = select_reading_units(cast, policy_id=policy_id)
    requested = edition_ids or list(SOURCE_EDITIONS)
    unknown = sorted(set(requested) - set(SOURCE_EDITIONS))
    if unknown:
        raise ValueError(f"Unknown edition_id(s): {', '.join(unknown)}")
    editions = []
    for edition_id in requested:
        edition = SOURCE_EDITIONS[edition_id]
        locators = []
        for unit in reading["selected_units"]:
            locators.append(
                {
                    **unit,
                    "source_id": edition["source_id"],
                    "document_url": edition["document_url"],
                    "passage_status": edition["passage_status"],
                    "text_included": False,
                }
            )
        editions.append(
            {
                "edition_id": edition_id,
                **edition,
                "selected_passage_locators": locators,
            }
        )
    if cast["computed_facts"] != original:
        raise AssertionError("Classical source layer must not mutate cast facts.")
    return {
        "schema_version": "0.3.0",
        "system": "iching",
        "lineage": "king-wen-classical-source-layer-v0.3",
        "rule_ids": [
            "ICHING-CLASSICAL-SOURCE-LAYER-001",
            *reading["rule_ids"],
        ],
        "selection": reading,
        "editions": editions,
        "version_comparison": {
            "status": "not_collated",
            "compared_edition_ids": requested,
            "differences": [],
            "message": (
                "Edition metadata is registered, but textual variants have not been collated. "
                "No difference is inferred from an absent comparison."
            ),
        },
        "validation": {
            "status": "valid",
            "warnings": [
                {
                    "code": "classical_text_not_bundled",
                    "message": "No classical or translated passage is bundled or quoted.",
                }
            ],
        },
    }
