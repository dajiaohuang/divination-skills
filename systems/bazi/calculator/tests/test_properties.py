"""Deterministic property checks across the supported Bazi date window."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from systems.bazi.calculator.engine import calculate_chart

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"


def chart_at(value: datetime) -> dict:
    return calculate_chart(
        {"local_datetime": value.isoformat(timespec="seconds"), "timezone": "UTC"}
    )


def sampled_datetimes(count: int = 120) -> list[datetime]:
    randomizer = random.Random(20260723)
    start = datetime(1901, 1, 1, 12)
    span_days = (datetime(2099, 10, 1) - start).days
    return [start + timedelta(days=randomizer.randrange(span_days)) for _ in range(count)]


def test_every_pillar_index_matches_its_stem_and_branch() -> None:
    for instant in sampled_datetimes():
        chart = chart_at(instant)
        for pillar in chart["computed_facts"]["pillars"].values():
            assert pillar["stem"]["name"] == STEMS[pillar["index"] % 10]
            assert pillar["branch"]["name"] == BRANCHES[pillar["index"] % 12]
            assert pillar["ganzhi"] == STEMS[pillar["index"] % 10] + BRANCHES[pillar["index"] % 12]


def test_day_pillar_advances_one_step_per_civil_day() -> None:
    for instant in sampled_datetimes():
        today = chart_at(instant)["computed_facts"]["pillars"]["day"]["index"]
        tomorrow = chart_at(instant + timedelta(days=1))["computed_facts"]["pillars"]["day"][
            "index"
        ]
        assert tomorrow == (today + 1) % 60


def test_day_pillar_repeats_after_sixty_civil_days() -> None:
    for instant in sampled_datetimes():
        today = chart_at(instant)["computed_facts"]["pillars"]["day"]["ganzhi"]
        later = chart_at(instant + timedelta(days=60))["computed_facts"]["pillars"]["day"]["ganzhi"]
        assert later == today


def test_hour_branch_covers_double_hours_with_late_zi_at_23() -> None:
    for hour in range(24):
        chart = chart_at(datetime(2024, 7, 15, hour, 30))
        expected_branch = BRANCHES[((hour + 1) // 2) % 12]
        assert chart["computed_facts"]["pillars"]["hour"]["branch"]["name"] == expected_branch


def test_randomized_calculation_is_exactly_reproducible() -> None:
    for instant in sampled_datetimes(40):
        assert chart_at(instant) == chart_at(instant)
