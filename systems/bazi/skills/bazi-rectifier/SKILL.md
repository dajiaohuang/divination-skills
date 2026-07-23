---
name: bazi-rectifier
description: Scan Bazi double-hour birth-time candidates using at least five dated historical events split into training and holdout sets. Use for 八字时辰候选, hour-range rectification, retained-event ranking, or underdetermination checks. Do not promise a unique minute, use personality descriptions as tie-breakers, skip holdout validation, infer event details, or conceal insufficient evidence.
---

# Bazi rectifier

1. Require birth date, IANA timezone, at least five event date ranges, and explicit training/holdout labels. The current baseline calculates each event at local noon on `start_date`; `end_date` is retained only as uncertainty metadata.
2. Run `scripts/run.py --birth-date ... --timezone ... --events <json>`.
3. Scan the 13 declared double-hour ranges; do not fabricate minute precision.
4. Rank with training evidence, check holdout evidence, and return `underdetermined` on unresolved ties.
5. Cite `BAZI-RECTIFIER-HOUR-SCAN-001`.
6. Apply [references/safety.md](references/safety.md).

Soft personality descriptions are forbidden as tie-breakers. A ranking is not proof of causation or
a unique birth time.
