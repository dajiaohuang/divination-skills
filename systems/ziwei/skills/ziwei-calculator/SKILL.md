---
name: ziwei-calculator
description: Calculate project-native Zi Wei Dou Shu v0.5 natal structure from explicit solar or lunar input, IANA time, calendar-boundary policies, calculation-gender parameter, and optional NOAA apparent solar time. Use for 紫微斗数排盘, twelve palaces, major/minor/auxiliary stars, classical brightness, cycles, birth and palace-stem transformations, or replayable natal facts. Do not invoke iztro, infer identity, apply undeclared time correction, mix schools, interpret fixed events, or invent unlisted brightness.
---

# Ziwei calculator

Return calculation facts, not an interpretive reading.

## Workflow

1. Require either offset-free solar `--local-datetime` or explicit lunar date, leap-month flag, and time index; also require IANA `--timezone` and `--calculation-gender`.
2. Default to `--time-basis civil`. Permit `--time-basis apparent_solar` only for solar input with explicit `--longitude`; disclose that it uses the NOAA approximation.
3. Record `year_boundary`, `late_zi_policy`, and `leap_month_policy`; never infer them from another engine.
4. Run `scripts/run.py`; preserve DST fold, civil UTC instant, calculation clock, double-hour index, and lineage.
5. Cite `ZIWEI-INPUT-POLICY-001`, `ZIWEI-TIME-INDEX-001`, `ZIWEI-NATIVE-NATAL-001`, `ZIWEI-STAR-BRIGHTNESS-001`, and the applicable transformation/cycle rules.
6. Preserve all twelve palace, star, brightness, and transformation-path fact IDs exactly.
7. Enforce `ZIWEI-STRUCTURAL-BOUNDARY-001`: do not turn placements, brightness, 四化, cycles, or limits into life-event claims.
8. Say that `calculation_gender` is a required algorithm parameter and never infer or restate it as identity.
9. Apply [references/safety.md](references/safety.md) to high-impact or third-party requests.

Treat iztro only as an ignored comparison reference. Brightness is emitted only for the selected
《紫微斗数全书》卷二 matrix. The ↓ outward / ↑ inward labels are a declared project policy.
Charts from other schools, engines, calendar policies, or solar-time policies are not interchangeable.
