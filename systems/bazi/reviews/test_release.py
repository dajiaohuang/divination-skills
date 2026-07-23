from __future__ import annotations

from systems.bazi.reviews.release import audit_release


def test_release_audit_reports_complete_technical_counts_and_real_human_blockers() -> None:
    report = audit_release()
    assert report["counts"] == {
        "standard": 100,
        "edge": 30,
        "dispute": 20,
        "invalid_input": 20,
        "expert_candidates": 50,
        "expert_accepted": 0,
    }
    assert report["count_checks"]["standard"]
    assert not report["count_checks"]["expert_accepted"]
    assert report["signoff_checks"] == {"domain": False, "rights": False, "privacy": False}
    assert report["evaluation_checks"] == {"report_current": True, "technical_pass": True}
    assert not report["ready"]
