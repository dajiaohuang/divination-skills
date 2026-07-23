"""Shared strict IANA local-time normalization."""

from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class TimeNormalizationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def localize_strict(
    local_datetime: str, timezone: str, fold: int | None = None
) -> tuple[datetime, int]:
    """Parse an offset-free local ISO time and reject DST ambiguity or gaps."""

    try:
        naive = datetime.fromisoformat(local_datetime)
    except (TypeError, ValueError) as exc:
        raise TimeNormalizationError(
            "invalid_local_datetime", "local_datetime must be an ISO 8601 local date and time."
        ) from exc
    if naive.tzinfo is not None:
        raise TimeNormalizationError(
            "offset_not_allowed",
            "local_datetime must not contain an offset; provide an IANA timezone separately.",
        )
    try:
        zone = ZoneInfo(timezone)
    except (TypeError, ZoneInfoNotFoundError) as exc:
        raise TimeNormalizationError(
            "unknown_timezone", f"Unknown IANA time zone: {timezone}"
        ) from exc

    candidates = []
    for candidate_fold in (0, 1):
        aware = naive.replace(tzinfo=zone, fold=candidate_fold)
        if aware.astimezone(UTC).astimezone(zone).replace(tzinfo=None) == naive:
            candidates.append((candidate_fold, aware))
    offsets = {candidate.utcoffset() for _, candidate in candidates}
    if not candidates:
        raise TimeNormalizationError(
            "nonexistent_local_time",
            "The local time does not exist because the clock moved forward.",
        )
    if len(offsets) > 1 and fold is None:
        raise TimeNormalizationError(
            "ambiguous_local_time",
            "The local time occurs twice; explicitly provide fold=0 or fold=1.",
        )
    if fold not in (None, 0, 1) or isinstance(fold, bool):
        raise TimeNormalizationError("invalid_fold", "fold must be 0 or 1.")
    selected = 0 if fold is None else fold
    for candidate_fold, aware in candidates:
        if candidate_fold == selected:
            return aware, selected
    return candidates[0][1], candidates[0][0]
