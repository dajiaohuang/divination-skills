from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from divination_skills.solar_time import (
    SolarTimeError,
    apparent_solar_time,
    equation_of_time_minutes,
)


def test_noaa_apparent_solar_time_matches_reported_wenmo_minute() -> None:
    civil = datetime(1999, 9, 15, 19, 5, tzinfo=ZoneInfo("Asia/Shanghai"))
    result = apparent_solar_time(civil, 119.917)

    assert result.longitude_correction_minutes == pytest.approx(-0.332, abs=0.000001)
    assert result.apparent_datetime.strftime("%Y-%m-%dT%H:%M") == "1999-09-15T19:09"
    assert 4 < result.total_correction_minutes < 5


def test_equation_of_time_accounts_for_leap_year() -> None:
    zone = ZoneInfo("UTC")
    regular = equation_of_time_minutes(datetime(2023, 3, 1, 12, tzinfo=zone))
    leap = equation_of_time_minutes(datetime(2024, 3, 1, 12, tzinfo=zone))
    assert regular != leap


@pytest.mark.parametrize("longitude", [-180.1, 180.1, True, "120"])
def test_apparent_solar_time_rejects_invalid_longitude(longitude: object) -> None:
    civil = datetime(2026, 1, 1, 12, tzinfo=ZoneInfo("UTC"))
    with pytest.raises(SolarTimeError) as captured:
        apparent_solar_time(civil, longitude)  # type: ignore[arg-type]
    assert captured.value.code == "invalid_longitude"


def test_apparent_solar_time_requires_aware_datetime() -> None:
    with pytest.raises(SolarTimeError) as captured:
        apparent_solar_time(datetime(2026, 1, 1, 12), 0)
    assert captured.value.code == "timezone_required"
