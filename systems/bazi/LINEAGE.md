# Bazi lineage and calculation decisions

## Baseline

The initial product baseline is a narrow Ziping-style calculation layer. It does not claim to represent every Ziping lineage. A separate, project-authored seasonal-support path exists only as an explicit engineering baseline; it is never mixed into the default calculation lineage.

## Frozen v0.1 decisions

| Topic | Decision |
|---|---|
| Calendar input | Proleptic Gregorian within 1900–2100 |
| Time zone | Required IANA identifier; use `zoneinfo` plus pinned `tzdata` |
| Year boundary | Exact instant of Spring Commences / 立春 |
| Month boundary | Exact instant of the 12 minor solar terms / 节 |
| Solar-term frame | The term is an absolute instant; `lunar_python` term timestamps are interpreted in their fixed UTC+08:00 reference frame and converted to UTC, avoiding accidental historical DST shifts |
| Day boundary | Default `midnight`; optional `zi_initial` advances the day pillar at 23:00 |
| Late-Zi hour stem | Derived from the next civil day's day stem for 23:00–23:59 under both day-boundary policies |
| True solar time | Not applied in v0.1; longitude is retained only as input metadata |
| Luck-cycle direction | Must be supplied explicitly as `forward` or `reverse`; never inferred from gender |
| Luck-cycle start | Interval to the adjacent month-boundary term divided by three days per year; output as a decimal age and marked method-specific |
| Strength path | Disabled by default; the only selectable path is the isolated `project-seasonal-support-v0.1` feature contract, marked low-confidence and pending independent expert approval |

## Explicit disputes

- Day changes at midnight versus the beginning of the Zi double-hour.
- Late-Zi day pillar and hour-stem handling.
- Civil time versus mean or apparent solar time.
- Gender/year-polarity direction rules for luck cycles.
- Exact conversion of the adjacent-term interval into start year, month, day, and hour.

Each is represented in `disputes/`; product output must disclose any non-default selection.

## Evidence boundary

Solar-term geometry is checked against the Hong Kong Observatory description that the 24 terms are spaced at 15-degree ecliptic-longitude intervals. Timestamp-aware behavior is compared against `lunar-python`; an independent `sxtwl-modern` implementation agrees on all four pillars for 17 non-boundary-date standard cases. Its day-level API cannot adjudicate the exact instant on a Jie date, so those three exclusions are recorded in `tests/COMPARATOR_REPORT.md`. Classical interpretive claims remain out of scope until accepted sources and expert review are available.

The opt-in seasonal-support path is defined only by `strength/SEASONAL_SUPPORT_SPEC.md`. Its labels must not be presented as canonical Ziping conclusions or used to select useful gods.

A user-supplied external Bazi Skill export additionally corroborates one 1999 chart's four pillars,
Ten Gods, five branch relations, and forward luck-cycle prefix. Its provider and version were not
reported, so it remains a non-authoritative regression reference rather than a production source.
