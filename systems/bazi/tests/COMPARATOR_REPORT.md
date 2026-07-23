# Bazi development comparator report

Reviewed: 2026-07-23

The production engine is replayed against two separately implemented calendar sources:

- `lunar-python 1.4.8` supplies the timestamp-aware pinned comparator and solar-term instants.
- `sxtwl-modern 1.1.2` is an independent C++ astronomy/calendar implementation used only in development because its complete license text still needs review.

For the 100 standard fixtures, sxtwl agrees on all four pillars in 97 cases. Three inputs fall on a `Jie` calendar date (`CASE-BAZI-STANDARD-001`, `005`, and `018`). The sxtwl API exposed by version 1.1.2 returns date-level year/month pillars, while this project changes those pillars at the exact timestamp. Those three cases are excluded from strict sxtwl comparison and remain covered by timestamp-aware boundary tests.

The executable acceptance test is `test_independent_sxtwl_comparator_agrees_away_from_boundary_dates`; this document records why the exclusion is bounded rather than silently ignored.
