from __future__ import annotations

from divination_skills.evaluation import collect_fact_ids, collect_narrative_claims, ratio_metric


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
