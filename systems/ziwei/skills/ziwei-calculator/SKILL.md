---
name: ziwei-calculator
description: Calculate or validate a project-native Zi Wei Dou Shu structural foundation with explicit IANA local time, double-hour index, and calculation-gender parameter. Use for 紫微斗数基础排盘, twelve-palace and star facts, independent comparison, or chart validation. Do not invoke iztro, infer gender identity, apply true solar time, mix schools, interpret life events, or guarantee outcomes.
---

# Ziwei calculator

Return calculation facts, not an interpretive reading.

## Workflow

1. Require an offset-free `--local-datetime`, IANA `--timezone`, and explicit `--calculation-gender` of `male` or `female`.
2. Run `scripts/run.py`; preserve DST fold, UTC instant, local date, double-hour index, and lineage.
3. Cite `ZIWEI-TIME-INDEX-001` and `ZIWEI-NATIVE-NATAL-001` for every placement claim.
4. Preserve all twelve palace and star fact IDs exactly.
5. Enforce `ZIWEI-STRUCTURAL-BOUNDARY-001`: do not turn placements, 四化 labels, or decade ranges into life-event claims.
6. Say that `calculation_gender` is a required algorithm parameter and never infer or restate it as identity.
7. Apply [references/safety.md](references/safety.md) to high-impact or third-party requests.

Treat iztro only as an ignored comparison reference. Charts from other schools, engines,
leap-month policies, time conventions, or true-solar-time correction are not interchangeable with
this lineage.
