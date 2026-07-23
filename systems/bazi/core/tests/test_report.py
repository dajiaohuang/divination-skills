from __future__ import annotations

from copy import deepcopy

from systems.bazi.calculator.engine import calculate_chart
from systems.bazi.core.report import build_report


def sample_chart(**overrides):
    payload = {
        "local_datetime": "1986-05-29T19:30:00",
        "timezone": "Asia/Shanghai",
        **overrides,
    }
    return calculate_chart(payload)


def all_explanations(report):
    narrative = report["narrative"]
    return [
        *narrative["calculation_basis"],
        *narrative["verified_facts"],
        *narrative["symbolic_relationships"],
        *narrative["seasonal_support_path"],
        *narrative["method_specific_timing"],
    ]


def test_report_preserves_computed_facts_and_links_every_explanation() -> None:
    chart = sample_chart(luck_cycle_direction="forward")
    original = deepcopy(chart["computed_facts"])
    report = build_report(chart)

    assert chart["computed_facts"] == original
    assert report["computed_facts"] == original
    for explanation in all_explanations(report):
        assert explanation["fact_ids"]
        assert explanation["rule_ids"]
        assert explanation["statement"]


def test_selected_late_zi_rule_is_linked() -> None:
    report = build_report(
        sample_chart(local_datetime="2024-01-01T23:30:00", day_boundary="zi_initial")
    )
    day = next(
        item
        for item in report["narrative"]["verified_facts"]
        if item["fact_ids"] == ["bazi.pillar.day"]
    )
    assert day["rule_ids"] == ["BAZI-CAL-DAY-002"]


def test_missing_luck_direction_omits_timing_explanation() -> None:
    report = build_report(sample_chart())
    assert report["narrative"]["method_specific_timing"] == []


def test_apparent_solar_time_is_cited_and_disclosed() -> None:
    report = build_report(
        sample_chart(
            local_datetime="1999-09-15T19:05:00",
            longitude=119.917,
            time_basis="apparent_solar",
        )
    )
    basis = report["narrative"]["calculation_basis"][0]
    assert basis["rule_ids"] == ["BAZI-TIME-SOLAR-001"]
    assert "NOAA apparent-solar" in basis["statement"]


def test_strength_path_is_opt_in_and_has_exactly_one_low_confidence_finding() -> None:
    baseline = build_report(sample_chart())
    assert baseline["narrative"]["seasonal_support_path"] == []
    assert not any(
        finding["finding_type"] == "bazi.seasonal-support"
        for finding in baseline["derived_findings"]
    )

    selected = build_report(sample_chart(), "project-seasonal-support-v0.1")
    explanations = selected["narrative"]["seasonal_support_path"]
    findings = [
        finding
        for finding in selected["derived_findings"]
        if finding["finding_type"] == "bazi.seasonal-support"
    ]
    assert len(explanations) == 1
    assert len(findings) == 1
    assert findings[0]["confidence"] == "low"
    assert explanations[0]["rule_ids"] == [findings[0]["rule_id"]]


def test_unknown_strength_lineage_is_rejected() -> None:
    try:
        build_report(sample_chart(), "mixed-school-unlabeled")
    except ValueError as exc:
        assert "Unsupported strength lineage" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Unknown lineage was accepted")


def test_invalid_external_chart_is_rejected() -> None:
    chart = sample_chart()
    chart["validation"]["status"] = "invalid"
    try:
        build_report(chart)
    except ValueError as exc:
        assert "valid calculator chart" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Invalid chart was accepted")
