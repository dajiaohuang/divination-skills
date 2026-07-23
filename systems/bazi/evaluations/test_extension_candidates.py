from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def test_synastry_expert_queue_has_fifty_unaccepted_candidates() -> None:
    queue = json.loads(
        (ROOT / "synastry_expert_candidates.json").read_text(encoding="utf-8")
    )
    assert queue["candidate_count"] == len(queue["candidates"]) == 50
    assert queue["status"] == "pending_expert_review"
    assert all(
        candidate["accepted"] is False
        and candidate["review"]["reviewer_id"] is None
        and candidate["review"]["decision"] == "pending"
        for candidate in queue["candidates"]
    )
