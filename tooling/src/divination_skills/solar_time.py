"""Approximate apparent solar time using NOAA's published equations."""

from __future__ import annotations

from calendar import isleap
from dataclasses import dataclass
from datetime import datetime, timedelta
from math import cos, pi, sin

SOURCE_ID = "SRC-ASTRONOMY-NOAA-SOLAR-001"
METHOD = "noaa-fractional-year-equation-of-time"


class SolarTimeError(ValueError):
    """A user-correctable apparent-solar-time input error."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class ApparentSolarTime:
    """One auditable civil-to-apparent-solar-time conversion."""

    civil_datetime: datetime
    apparent_datetime: datetime
    longitude_degrees_east: float
    utc_offset_hours: float
    equation_of_time_minutes: float
    longitude_correction_minutes: float
    total_correction_minutes: float

    def to_dict(self) -> dict[str, object]:
        return {
            "method": METHOD,
            "civil_datetime": self.civil_datetime.isoformat(),
            "apparent_datetime": self.apparent_datetime.isoformat(),
            "longitude_degrees_east": self.longitude_degrees_east,
            "utc_offset_hours": round(self.utc_offset_hours, 6),
            "equation_of_time_minutes": round(self.equation_of_time_minutes, 6),
            "longitude_correction_minutes": round(self.longitude_correction_minutes, 6),
            "total_correction_minutes": round(self.total_correction_minutes, 6),
            "source_ids": [SOURCE_ID],
        }


def equation_of_time_minutes(local_datetime: datetime) -> float:
    """Return NOAA's fractional-year equation-of-time approximation in minutes."""

    if local_datetime.tzinfo is None or local_datetime.utcoffset() is None:
        raise SolarTimeError(
            "timezone_required",
            "equation_of_time_minutes requires a timezone-aware local datetime.",
        )
    days_in_year = 366 if isleap(local_datetime.year) else 365
    fractional_hour = (
        local_datetime.hour
        + local_datetime.minute / 60
        + local_datetime.second / 3600
        + local_datetime.microsecond / 3_600_000_000
    )
    gamma = (
        2
        * pi
        / days_in_year
        * (local_datetime.timetuple().tm_yday - 1 + (fractional_hour - 12) / 24)
    )
    return 229.18 * (
        0.000075
        + 0.001868 * cos(gamma)
        - 0.032077 * sin(gamma)
        - 0.014615 * cos(2 * gamma)
        - 0.040849 * sin(2 * gamma)
    )


def apparent_solar_time(
    civil_datetime: datetime,
    longitude_degrees_east: float,
) -> ApparentSolarTime:
    """Convert civil time to approximate apparent solar time.

    NOAA publishes ``time_offset = equation_of_time + 4*longitude -
    60*timezone`` where longitude is positive east and timezone is the
    hours added to UTC.  The returned datetime is a calculation clock, not
    a second physical instant.
    """

    if civil_datetime.tzinfo is None or civil_datetime.utcoffset() is None:
        raise SolarTimeError(
            "timezone_required",
            "Apparent solar time requires a timezone-aware civil datetime.",
        )
    if isinstance(longitude_degrees_east, bool) or not isinstance(
        longitude_degrees_east, (int, float)
    ):
        raise SolarTimeError(
            "invalid_longitude",
            "longitude must be a number between -180 and 180 degrees east.",
        )
    longitude = float(longitude_degrees_east)
    if not -180 <= longitude <= 180:
        raise SolarTimeError(
            "invalid_longitude",
            "longitude must be between -180 and 180 degrees east.",
        )

    utc_offset_hours = civil_datetime.utcoffset().total_seconds() / 3600
    equation = equation_of_time_minutes(civil_datetime)
    longitude_correction = 4 * longitude - 60 * utc_offset_hours
    total_correction = equation + longitude_correction
    return ApparentSolarTime(
        civil_datetime=civil_datetime,
        apparent_datetime=civil_datetime + timedelta(minutes=total_correction),
        longitude_degrees_east=longitude,
        utc_offset_hours=utc_offset_hours,
        equation_of_time_minutes=equation,
        longitude_correction_minutes=longitude_correction,
        total_correction_minutes=total_correction,
    )
