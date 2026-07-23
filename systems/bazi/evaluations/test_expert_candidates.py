from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent


def test_fifty_traceable_candidates_are_ready_for_real_expert_review() -> None:
    schema = json.loads((ROOT / "expert-analysis.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    candidates = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "expert_candidates").glob("*.json"))
    ]
    assert len(candidates) == 50
    for candidate in candidates:
        validator.validate(candidate)
        assert candidate["review"]["status"] in {"pending_expert", "reviewed"}
        for claim in candidate["reasoning_chain"]:
            assert claim["fact_ids"] and claim["rule_ids"]


def test_no_candidate_claims_an_expert_review_that_did_not_happen() -> None:
    candidates = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "expert_candidates").glob("*.json"))
    ]
    for candidate in candidates:
        review = candidate["review"]
        if review["status"] == "pending_expert":
            assert review["reviewer_id"] is None
            assert review["reviewed_at"] is None
            assert review["decision"] is None
