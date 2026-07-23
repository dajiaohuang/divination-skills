from __future__ import annotations

from systems.ziwei.engine import calculate
from systems.ziwei.synastry import compare_charts


def _chart(value: str, gender: str) -> dict:
    return calculate(
        {
            "local_datetime": value,
            "timezone": "Asia/Shanghai",
            "calculation_gender": gender,
        }
    )


def test_ziwei_synastry_separates_directional_and_symmetric_facts() -> None:
    chart_a = _chart("2000-01-01T12:00:00", "male")
    chart_b = _chart("2001-02-03T14:00:00", "female")
    report = compare_charts(chart_a, chart_b)
    assert report["chart_refs"]["A"] != report["chart_refs"]["B"]
    assert all(
        fact["direction"] == "A_to_B"
        for fact in report["directional"]["A_to_B"]
    )
    assert all(
        fact["direction"] == "B_to_A"
        for fact in report["directional"]["B_to_A"]
    )
    assert all(
        fact["a_star_fact_id"] and fact["b_star_fact_id"]
        for fact in report["symmetric"]
    )
    assert report["validation"]["status"] == "valid"


def test_same_chart_comparison_is_replayable_but_not_a_compatibility_score() -> None:
    chart = _chart("2000-01-01T12:00:00", "male")
    report = compare_charts(chart, chart)
    assert len(report["symmetric"]) == 14
    assert "score" not in report
    assert "compatibility" not in report
