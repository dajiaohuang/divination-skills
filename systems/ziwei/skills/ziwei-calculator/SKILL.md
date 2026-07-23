---
name: ziwei-calculator
description: Calculate project-native Zi Wei Dou Shu v0.4 natal structure from explicit solar or lunar input, IANA time, calendar-boundary policies, and calculation-gender parameter. Use for 紫微斗数排盘, twelve palaces, major/minor/auxiliary stars, cycles, four transformations, or replayable natal facts. Do not invoke iztro, infer identity, apply undeclared true solar time, mix schools, interpret fixed events, or invent brightness.
---

# Ziwei calculator

Return calculation facts, not an interpretive reading.

## Workflow

1. Require either offset-free solar `--local-datetime` or explicit lunar date, leap-month flag, and time index; also require IANA `--timezone` and `--calculation-gender`.
2. Record `year_boundary`, `late_zi_policy`, and `leap_month_policy`; never infer them from another engine.
3. Run `scripts/run.py`; preserve DST fold, UTC instant, calculation date, double-hour index, and lineage.
4. Cite `ZIWEI-INPUT-POLICY-001`, `ZIWEI-TIME-INDEX-001`, `ZIWEI-NATIVE-NATAL-001`, and the applicable star/cycle rules.
5. Preserve all twelve palace and star fact IDs exactly.
6. Enforce `ZIWEI-STRUCTURAL-BOUNDARY-001`: do not turn placements, 四化, cycles, or limits into life-event claims.
7. Say that `calculation_gender` is a required algorithm parameter and never infer or restate it as identity.
8. Apply [references/safety.md](references/safety.md) to high-impact or third-party requests.

Treat iztro only as an ignored comparison reference. Brightness is explicitly unavailable in v0.4.
Charts from other schools, engines, calendar policies, or true-solar-time correction are not
interchangeable with this lineage.
