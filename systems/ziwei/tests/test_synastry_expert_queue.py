from __future__ import annotations

import json
from pathlib import Path

QUEUE = Path(__file__).resolve().parents[1] / "cases" / "synastry_expert_candidates.json"


def test_synastry_queue_has_fifty_unaccepted_candidates() -> None:
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    assert queue["candidate_count"] == len(queue["candidates"]) == 50
    assert all(
        candidate["accepted"] is False
        and candidate["review"]["reviewer_id"] is None
        and candidate["review"]["decision"] == "pending"
        for candidate in queue["candidates"]
    )
