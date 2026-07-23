"""Development comparators kept outside the production calculation path."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from lunar_python import Solar

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"


def lunar_python_reference(payload: dict[str, Any]) -> dict[str, str]:
    """Return reference pillars for Asia/Shanghai local civil inputs."""

    if payload.get("timezone") != "Asia/Shanghai":
        raise ValueError("The development comparator only accepts Asia/Shanghai inputs.")
    local = datetime.fromisoformat(payload["local_datetime"])
    solar = Solar.fromYmdHms(
        local.year, local.month, local.day, local.hour, local.minute, local.second
    )
    eight_char = solar.getLunar().getEightChar()
    eight_char.setSect(1 if payload.get("day_boundary") == "zi_initial" else 2)
    return {
        "year": eight_char.getYear(),
        "month": eight_char.getMonth(),
        "day": eight_char.getDay(),
        "hour": eight_char.getTime(),
    }


def sxtwl_modern_reference(payload: dict[str, Any]) -> dict[str, str]:
    """Return the independent sxtwl day-level reference for Shanghai inputs.

    sxtwl-modern 1.1.2 exposes calendar-day pillars rather than a timestamp-aware
    year/month boundary API. Callers must exclude dates containing Li Chun or a
    Jie boundary when comparing the year and month pillars.
    """

    if payload.get("timezone") != "Asia/Shanghai":
        raise ValueError("The sxtwl comparator only accepts Asia/Shanghai inputs.")
    if payload.get("day_boundary", "midnight") != "midnight":
        raise ValueError("The sxtwl comparator only covers the midnight day boundary.")

    try:
        import sxtwl
    except ImportError as exc:  # pragma: no cover - dependency is in the dev extra
        raise RuntimeError("Install the dev extra to use the sxtwl comparator.") from exc

    local = datetime.fromisoformat(payload["local_datetime"])
    calendar = sxtwl.Lunar()
    day = calendar.getDayBySolar(local.year, local.month, local.day)
    hour = calendar.getShiGz(day.Lday2.tg, local.hour)

    def ganzhi(value: Any) -> str:
        return STEMS[value.tg] + BRANCHES[value.dz]

    return {
        "year": ganzhi(day.Lyear2),
        "month": ganzhi(day.Lmonth2),
        "day": ganzhi(day.Lday2),
        "hour": ganzhi(hour),
    }
