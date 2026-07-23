"""Generate deterministic Ziwei standard, boundary, and dispute cases."""

from __future__ import annotations

import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from divination_skills.contracts import canonical_json

from systems.ziwei.engine import LINEAGE, calculate

ROOT = Path(__file__).resolve().parent
GOLDEN_ROOT = ROOT / "golden"
EDGE_ROOT = ROOT / "edge_cases"
DISPUTE_ROOT = ROOT / "disputes"
RULES = [
    "ZIWEI-NATIVE-NATAL-001",
    "ZIWEI-TIME-INDEX-001",
    "ZIWEI-STAR-AUX-001",
    "ZIWEI-CYCLE-DECADAL-001",
    "ZIWEI-STRUCTURAL-BOUNDARY-001",
]
SOURCE_REFS = [
    {
        "source_id": "SRC-ZIWEI-PROJECT-SPEC-001",
        "locator": "project-native structural calculation v0.4",
    },
    {
        "source_id": "SRC-ZIWEI-QUANSHU-001",
        "locator": "formula sections for palaces, stars, cycles, and limits",
    },
]


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def placement_map(result: dict[str, Any]) -> dict[str, int]:
    positions = {}
    for palace in result["computed_facts"]["palaces"]:
        for group in ("majorStars", "minorStars", "auxiliaryStars"):
            for star in palace[group]:
                positions[f"{group}:{star['name']}"] = palace["index"]
    return dict(sorted(positions.items()))


def build_case(
    *,
    case_id: str,
    title: str,
    category: str,
    payload: dict[str, Any],
    rules: list[str] | None = None,
    allowed_disagreements: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    result = calculate(payload)
    return {
        "case_id": case_id,
        "title": title,
        "system": "ziwei",
        "lineage": LINEAGE,
        "category": category,
        "data_classification": "synthetic",
        "raw_input": payload,
        "normalized_input": result["normalized_input"],
        "expected_intermediate": {
            "time_index": result["normalized_input"]["time_index"],
            "five_elements_class": result["computed_facts"]["five_elements_class"],
            "star_placements": placement_map(result),
        },
        "expected_output": {
            "computed_facts_sha256": digest(result["computed_facts"]),
            "palace_count": len(result["computed_facts"]["palaces"]),
        },
        "must_match_rules": rules or RULES,
        "allowed_disagreements": allowed_disagreements or [],
        "forbidden_conclusions": [
            "A fixed life event is guaranteed.",
            "The calculation-gender parameter was inferred as identity.",
            "A brightness value was invented.",
        ],
        "sources": SOURCE_REFS,
        "reviewers": [
            {
                "reviewer_id": "project-native-regression-review",
                "role": "calculation",
                "reviewed_at": "2026-07-23",
                "decision": "accepted",
                "notes": (
                    "Synthetic deterministic regression review; independent Ziwei expert "
                    "acceptance remains pending."
                ),
            }
        ],
    }


def write_case(root: Path, case: dict[str, Any]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / f"{case['case_id']}.json").write_text(
        json.dumps(case, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def clear_generated(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for path in root.glob("CASE-ZIWEI-*.json"):
        path.unlink()


def standard_cases() -> list[dict[str, Any]]:
    cases = []
    start = date(1900, 2, 4)
    hours = (0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23)
    zones = ("Asia/Shanghai", "UTC", "Asia/Tokyo", "America/New_York")
    for index in range(100):
        day = start + timedelta(days=index * 731 + index % 29)
        if day.year > 2099:
            day = date(1900 + index, index % 12 + 1, index % 27 + 1)
        payload = {
            "local_datetime": f"{day.isoformat()}T{hours[index % len(hours)]:02d}:17:00",
            "timezone": zones[index % len(zones)],
            "calculation_gender": "male" if index % 2 == 0 else "female",
        }
        cases.append(
            build_case(
                case_id=f"CASE-ZIWEI-NATAL-{index + 1:03d}",
                title=f"Project-native Ziwei structural chart {index + 1:03d}",
                category="standard",
                payload=payload,
            )
        )
    return cases


def edge_cases() -> list[dict[str, Any]]:
    cases = []
    for index in range(30):
        year = 1900 + (index * 7) % 200
        day = date(year, 2, min(28, index % 27 + 1))
        payload: dict[str, Any] = {
            "local_datetime": (
                f"{day.isoformat()}T{23 if index % 2 else 0:02d}:"
                f"{59 if index % 3 else 0:02d}:00"
            ),
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male" if index % 2 == 0 else "female",
            "late_zi_policy": "next_day" if index % 2 else "current_day",
            "year_boundary": (
                "spring_commences" if index % 3 == 0 else "lunar_new_year"
            ),
            "leap_month_policy": (
                "split_after_15" if index % 5 == 0 else "preserve"
            ),
        }
        cases.append(
            build_case(
                case_id=f"CASE-ZIWEI-EDGE-BOUNDARY-{index + 1:03d}",
                title=f"Ziwei boundary policy case {index + 1:03d}",
                category="edge_case",
                payload=payload,
                rules=[
                    "ZIWEI-INPUT-POLICY-001",
                    "ZIWEI-TIME-INDEX-001",
                    "ZIWEI-STRUCTURAL-BOUNDARY-001",
                ],
            )
        )
    return cases


def dispute_cases() -> list[dict[str, Any]]:
    cases = []
    policy_fields = (
        (
            "late_zi_policy",
            ["current_day", "next_day"],
            "DSP-ZIWEI-BOUNDARY-POLICY-001",
        ),
        (
            "year_boundary",
            ["lunar_new_year", "spring_commences"],
            "DSP-ZIWEI-BOUNDARY-POLICY-001",
        ),
        (
            "leap_month_policy",
            ["preserve", "split_after_15"],
            "DSP-ZIWEI-BOUNDARY-POLICY-001",
        ),
        (
            "calculation.time_basis",
            ["local_civil", "true_solar_time"],
            "DSP-ZIWEI-TIME-BASIS-001",
        ),
    )
    for index in range(20):
        field, allowed, dispute_id = policy_fields[index % len(policy_fields)]
        payload = {
            "local_datetime": f"{2000 + index:04d}-02-03T23:30:00",
            "timezone": "Asia/Shanghai",
            "calculation_gender": "male" if index % 2 == 0 else "female",
        }
        cases.append(
            build_case(
                case_id=f"CASE-ZIWEI-DISPUTE-POLICY-{index + 1:03d}",
                title=f"Ziwei explicit policy dispute {index + 1:03d}",
                category="dispute",
                payload=payload,
                rules=[
                    "ZIWEI-INPUT-POLICY-001",
                    "ZIWEI-STRUCTURAL-BOUNDARY-001",
                ],
                allowed_disagreements=[
                    {
                        "dispute_id": dispute_id,
                        "field_path": field,
                        "allowed_values": allowed,
                    }
                ],
            )
        )
    return cases


def main() -> None:
    for root in (GOLDEN_ROOT, EDGE_ROOT, DISPUTE_ROOT):
        clear_generated(root)
    groups = (
        (GOLDEN_ROOT, standard_cases()),
        (EDGE_ROOT, edge_cases()),
        (DISPUTE_ROOT, dispute_cases()),
    )
    for root, cases in groups:
        for case in cases:
            write_case(root, case)
    print("Generated 100 standard, 30 boundary, and 20 dispute Ziwei cases.")


if __name__ == "__main__":
    main()
