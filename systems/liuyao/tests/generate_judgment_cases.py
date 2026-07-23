from __future__ import annotations

import hashlib
import json
from pathlib import Path

from systems.liuyao.engine import calculate
from systems.liuyao.judgment import QUESTION_PACKS, analyze

ROOT = Path(__file__).resolve().parent
CASE_DIR = ROOT / "extension_cases" / "judgment"
QUEUE = Path(__file__).resolve().parents[1] / "evaluations" / "judgment_expert_candidates.json"


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def summary(result: dict) -> dict:
    return {
        "status": result["status"],
        "candidate_line_fact_ids": result["use_deity"]["candidate_line_fact_ids"],
        "line_strength": result["line_strength"],
        "moving_changes": result["moving_changes"],
        "timing_pack": result["timing_pack"],
    }


def main() -> None:
    CASE_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    categories = tuple(QUESTION_PACKS)
    candidates = []
    for number in range(1, 51):
        raw_input = {
            "seed_hex": f"{number:064x}",
            "local_datetime": (
                f"2026-{(number - 1) % 12 + 1:02d}-"
                f"{(number - 1) % 27 + 1:02d}T12:00:00"
            ),
            "timezone": "Asia/Shanghai",
        }
        arguments = {
            "question_category": categories[(number - 1) % len(categories)],
            "include_timing": number % 2 == 0,
        }
        expected = summary(analyze(calculate(raw_input), **arguments))
        case_id = f"CASE-LIUYAO-JUDGMENT-{number:03d}"
        case = {
            "case_id": case_id,
            "case_type": "standard",
            "raw_input": raw_input,
            "arguments": arguments,
            "expected_output": expected,
        }
        (CASE_DIR / f"{case_id}.json").write_text(
            json.dumps(case, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        candidates.append(
            {
                "candidate_id": f"LIUYAO-JUDGMENT-EXPERT-{number:03d}",
                "source_case_id": case_id,
                "expected_output_sha256": hashlib.sha256(
                    canonical(expected).encode("utf-8")
                ).hexdigest(),
                "review_focus": [
                    "explicit question-category routing",
                    "transparent strength components and moving/change relation",
                    "absence of guaranteed outcome or event-date claims",
                ],
                "accepted": False,
                "status": "pending_expert_review",
                "review": {
                    "decision": "pending",
                    "reviewer_id": None,
                    "reviewed_at": None,
                    "notes": "",
                },
            }
        )
    QUEUE.write_text(
        json.dumps(
            {
                "queue_id": "LIUYAO-JUDGMENT-EXPERT-QUEUE-001",
                "status": "pending_expert_review",
                "candidate_count": len(candidates),
                "candidates": candidates,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
