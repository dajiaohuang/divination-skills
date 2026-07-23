from __future__ import annotations

from pathlib import Path

from divination_skills.evaluation import (
    collect_fact_ids,
    collect_narrative_claims,
    corpus_sha256,
    ratio_metric,
)


def test_ratio_metric_supports_minimum_and_maximum_thresholds() -> None:
    assert ratio_metric(9, 10, threshold=0.9, comparison="minimum", evidence=["fixture"])["passed"]
    assert ratio_metric(0, 10, threshold=0.0, comparison="maximum", evidence=["fixture"])["passed"]


def test_fact_and_claim_collectors_ignore_limitations() -> None:
    value = {"fact_id": "fact.a", "children": [{"fact_id": "fact.b"}]}
    narrative = {
        "section": {"statement": "bounded", "fact_ids": ["fact.a"], "rule_ids": ["R-1"]},
        "limitations": ["not a claim"],
    }
    assert collect_fact_ids(value) == {"fact.a", "fact.b"}
    assert collect_narrative_claims(narrative) == [narrative["section"]]


def test_corpus_hash_uses_canonical_json_across_line_endings(tmp_path: Path) -> None:
    windows = tmp_path / "windows"
    linux = tmp_path / "linux"
    windows.mkdir()
    linux.mkdir()
    (windows / "case.json").write_bytes(b'{\r\n  "b": 2,\r\n  "a": 1\r\n}\r\n')
    (linux / "case.json").write_bytes(b'{"a":1,"b":2}\n')

    assert corpus_sha256([windows / "case.json"]) == corpus_sha256([linux / "case.json"])
