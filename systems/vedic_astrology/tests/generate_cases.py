"""Regenerate Vedic astrology Golden, edge, and dispute fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from systems.vedic_astrology.calculator.engine import calculate_chart

ROOT = Path(__file__).resolve().parent
PROJECT_SOURCE = "SRC-VEDIC-PROJECT-SPEC-001"
ASTRONOMY_SOURCE = "SRC-WESTERN-ASTRONOMY-ENGINE-001"


def case(
    *,
    case_id: str,
    title: str,
    directory: str,
    category: str,
    lineage: str,
    raw_input: dict[str, Any],
    rules: list[str],
    sources: list[dict[str, str]],
    disagreements: list[dict[str, Any]] | None = None,
) -> tuple[Path, dict[str, Any]]:
    result = calculate_chart(raw_input)
    document = {
        "case_id": case_id,
        "title": title,
        "system": "vedic-astrology",
        "lineage": lineage,
        "category": category,
        "data_classification": "synthetic",
        "raw_input": raw_input,
        "normalized_input": result["normalized_input"],
        "expected_intermediate": {
            "astronomy": result["computed_facts"]["astronomy"],
        },
        "expected_output": result,
        "must_match_rules": rules,
        "allowed_disagreements": disagreements or [],
        "forbidden_conclusions": [
            "A future event is guaranteed.",
            "Rules from an unselected lineage were silently applied.",
            "The bounded KP stellar layer is described as a complete KP chart.",
        ],
        "sources": sources,
        "reviewers": [
            {
                "reviewer_id": "pinned-engineering-regression",
                "role": "calculation",
                "reviewed_at": "2026-07-24",
                "decision": "accepted",
                "notes": (
                    "Deterministic engineering fixture; independent Jyotisha "
                    "domain sign-off remains pending."
                ),
            }
        ],
    }
    return ROOT / directory / f"{case_id}.json", document


def main() -> None:
    common_sources = [
        {"source_id": ASTRONOMY_SOURCE, "locator": "Pinned Astronomy Engine 2.1.19"},
        {"source_id": PROJECT_SOURCE, "locator": "Vedic v0.1 calculation contract"},
    ]
    all_rules = [
        "VEDIC-CAL-TIME-001",
        "VEDIC-CAL-SIDEREAL-001",
        "VEDIC-CAL-GRAHA-001",
        "VEDIC-CAL-MEAN-NODE-001",
        "VEDIC-CAL-LAGNA-001",
        "VEDIC-CAL-NAKSHATRA-001",
        "VEDIC-LINEAGE-ISOLATION-001",
        "VEDIC-PARASHARI-WHOLE-SIGN-001",
        "VEDIC-PARASHARI-NAVAMSHA-001",
        "VEDIC-PARASHARI-VIMSHOTTARI-001",
        "VEDIC-JAIMINI-KARAKA-SEVEN-001",
        "VEDIC-JAIMINI-RASHI-DRISHTI-001",
        "VEDIC-JAIMINI-ARUDHA-001",
        "VEDIC-KP-SUBLORD-001",
        "VEDIC-BOUNDARY-001",
    ]
    base = {
        "local_datetime": "1999-09-15T19:05:00",
        "timezone": "Asia/Shanghai",
        "longitude": 119.917,
        "latitude": 31.3,
    }
    definitions = [
        case(
            case_id="CASE-VEDIC-NATAL-001",
            title="Multi-lineage chart for Shanghai 1999",
            directory="golden",
            category="standard",
            lineage="true-citra-multi-lineage-v0.1",
            raw_input=base,
            rules=all_rules,
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-NATAL-002",
            title="Multi-lineage chart at Greenwich J2000",
            directory="golden",
            category="standard",
            lineage="true-citra-multi-lineage-v0.1",
            raw_input={
                "local_datetime": "2000-01-01T12:00:00",
                "timezone": "UTC",
                "longitude": 0.0,
                "latitude": 51.4779,
            },
            rules=all_rules,
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-NATAL-003",
            title="Multi-lineage chart for Delhi 1980",
            directory="golden",
            category="standard",
            lineage="true-citra-multi-lineage-v0.1",
            raw_input={
                "local_datetime": "1980-06-21T06:30:00",
                "timezone": "Asia/Kolkata",
                "longitude": 77.209,
                "latitude": 28.6139,
            },
            rules=all_rules,
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-NATAL-004",
            title="Multi-lineage chart for New York 2024",
            directory="golden",
            category="standard",
            lineage="true-citra-multi-lineage-v0.1",
            raw_input={
                "local_datetime": "2024-03-20T12:00:00",
                "timezone": "America/New_York",
                "longitude": -74.006,
                "latitude": 40.7128,
            },
            rules=all_rules,
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-NATAL-005",
            title="Multi-lineage chart for Honolulu 1969",
            directory="golden",
            category="standard",
            lineage="true-citra-multi-lineage-v0.1",
            raw_input={
                "local_datetime": "1969-07-20T10:00:00",
                "timezone": "Pacific/Honolulu",
                "longitude": -157.8583,
                "latitude": 21.3069,
            },
            rules=all_rules,
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-JAIMINI-EIGHT-001",
            title="Jaimini eight-karaka variant",
            directory="golden",
            category="standard",
            lineage="jaimini-eight-karaka-v0.1",
            raw_input={
                **base,
                "lineages": ["jaimini"],
                "jaimini_karaka_policy": "eight",
            },
            rules=[
                "VEDIC-CAL-TIME-001",
                "VEDIC-CAL-SIDEREAL-001",
                "VEDIC-CAL-GRAHA-001",
                "VEDIC-CAL-MEAN-NODE-001",
                "VEDIC-CAL-LAGNA-001",
                "VEDIC-JAIMINI-KARAKA-EIGHT-001",
                "VEDIC-JAIMINI-RASHI-DRISHTI-001",
                "VEDIC-JAIMINI-ARUDHA-001",
                "VEDIC-LINEAGE-ISOLATION-001",
            ],
            sources=common_sources
            + [
                {
                    "source_id": "SRC-VEDIC-JAIMINI-READER-001",
                    "locator": "Seven/eight-karaka variant overview",
                }
            ],
        ),
        case(
            case_id="CASE-VEDIC-LINEAGE-PARASHARI-ONLY-001",
            title="Parashari-only routing",
            directory="golden",
            category="regression",
            lineage="parashari-structural-v0.1",
            raw_input={**base, "lineages": ["parashari"]},
            rules=[
                "VEDIC-LINEAGE-ISOLATION-001",
                "VEDIC-PARASHARI-WHOLE-SIGN-001",
                "VEDIC-PARASHARI-NAVAMSHA-001",
                "VEDIC-PARASHARI-VIMSHOTTARI-001",
            ],
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-LINEAGE-KP-ONLY-001",
            title="KP-stellar-only routing",
            directory="golden",
            category="regression",
            lineage="kp-stellar-v0.1",
            raw_input={**base, "lineages": ["kp"]},
            rules=["VEDIC-LINEAGE-ISOLATION-001", "VEDIC-KP-SUBLORD-001"],
            sources=common_sources
            + [
                {
                    "source_id": "SRC-VEDIC-KP-INTRO-001",
                    "locator": "KP sub-lord overview",
                }
            ],
        ),
        case(
            case_id="CASE-VEDIC-EDGE-DST-001",
            title="Ambiguous New York civil time with explicit fold",
            directory="edge_cases",
            category="edge_case",
            lineage="true-citra-common-v0.1",
            raw_input={
                "local_datetime": "2021-11-07T01:30:00",
                "timezone": "America/New_York",
                "fold": 0,
                "longitude": -74.006,
                "latitude": 40.7128,
                "lineages": ["parashari"],
            },
            rules=["VEDIC-CAL-TIME-001", "VEDIC-LINEAGE-ISOLATION-001"],
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-KP-BOUNDARY-001",
            title="KP half-open subdivision boundary policy",
            directory="edge_cases",
            category="edge_case",
            lineage="kp-stellar-v0.1",
            raw_input={**base, "lineages": ["kp"]},
            rules=[
                "VEDIC-CAL-NAKSHATRA-001",
                "VEDIC-KP-SUBLORD-001",
                "VEDIC-BOUNDARY-001",
            ],
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-EDGE-NAVAMSHA-001",
            title="Navamsha unrounded boundary policy",
            directory="edge_cases",
            category="edge_case",
            lineage="parashari-structural-v0.1",
            raw_input={**base, "lineages": ["parashari"]},
            rules=["VEDIC-PARASHARI-NAVAMSHA-001", "VEDIC-BOUNDARY-001"],
            sources=common_sources,
        ),
        case(
            case_id="CASE-VEDIC-EDGE-ARUDHA-001",
            title="Arudha exception policy regression",
            directory="edge_cases",
            category="edge_case",
            lineage="jaimini-structural-v0.1",
            raw_input={**base, "lineages": ["jaimini"]},
            rules=["VEDIC-JAIMINI-ARUDHA-001"],
            sources=common_sources,
        ),
    ]
    dispute_specs = [
        (
            "CASE-VEDIC-DISPUTE-AYANAMSHA-001",
            "Ayanamsha selection disclosure",
            "DSP-VEDIC-AYANAMSHA-001",
            "normalized_input.ayanamsha",
            ["true_citra", "other_named_policy"],
            ["VEDIC-CAL-SIDEREAL-001"],
        ),
        (
            "CASE-VEDIC-DISPUTE-NODE-001",
            "Mean versus true node disclosure",
            "DSP-VEDIC-NODE-POLICY-001",
            "normalized_input.node_policy",
            ["mean", "true"],
            ["VEDIC-CAL-MEAN-NODE-001"],
        ),
        (
            "CASE-VEDIC-DISPUTE-KARAKA-001",
            "Seven versus eight Jaimini karakas",
            "DSP-VEDIC-JAIMINI-KARAKA-001",
            "normalized_input.jaimini_karaka_policy",
            ["seven", "eight"],
            [
                "VEDIC-JAIMINI-KARAKA-SEVEN-001",
                "VEDIC-JAIMINI-KARAKA-EIGHT-001",
            ],
        ),
        (
            "CASE-VEDIC-DISPUTE-HOUSE-001",
            "Whole-sign bhavas are not KP cusps",
            "DSP-VEDIC-HOUSE-SYSTEM-001",
            "computed_facts.lineages.kp.completeness",
            ["stellar_identity_only", "full_kp_cusps"],
            ["VEDIC-PARASHARI-WHOLE-SIGN-001", "VEDIC-KP-SUBLORD-001"],
        ),
        (
            "CASE-VEDIC-DISPUTE-DASHA-YEAR-001",
            "Vimshottari year-length disclosure",
            "DSP-VEDIC-DASHA-YEAR-001",
            "computed_facts.lineages.parashari.vimshottari.year_length_days",
            [365.2425, 360],
            ["VEDIC-PARASHARI-VIMSHOTTARI-001"],
        ),
    ]
    for case_id, title, dispute_id, path, values, rules in dispute_specs:
        definitions.append(
            case(
                case_id=case_id,
                title=title,
                directory="disputes",
                category="dispute",
                lineage="multi-lineage-dispute-v0.1",
                raw_input=base,
                rules=rules,
                sources=common_sources,
                disagreements=[
                    {
                        "dispute_id": dispute_id,
                        "field_path": path,
                        "allowed_values": values,
                    }
                ],
            )
        )

    for path, document in definitions:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(f"Generated {len(definitions)} Vedic cases.")


if __name__ == "__main__":
    main()
