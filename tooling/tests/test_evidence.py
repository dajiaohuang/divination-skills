from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from divination_skills.evidence import evidence_record


def test_evidence_record_uses_repository_relative_path_and_hash(tmp_path: Path) -> None:
    path = tmp_path / "reviews" / "signed.txt"
    path.parent.mkdir()
    path.write_text("signed review\n", encoding="utf-8")
    record = evidence_record(tmp_path, path)
    assert record == {
        "locator": "reviews/signed.txt",
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "retained_in_repository": True,
    }


def test_evidence_record_rejects_external_file(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-review.txt"
    outside.write_text("external\n", encoding="utf-8")
    with pytest.raises(ValueError, match="inside the repository"):
        evidence_record(tmp_path, outside)
