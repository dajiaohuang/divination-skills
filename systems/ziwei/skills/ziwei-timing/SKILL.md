---
name: ziwei-timing
description: Calculate project-native Ziwei v0.5 major-limit, minor-limit, annual, monthly, daily, and hourly structural layers with a shared timeline contract and transformation provenance. Use for 紫微运限, 大限小限, 流年流月流日流时, time-window structure, or deterministic replay. Do not predict guaranteed events, mix timing schools, infer missing birth time, or invoke iztro.
---

# Ziwei timing

Return time structure and evidence, never guaranteed event predictions.

## Workflow

1. Require validated natal inputs and an explicit target local datetime and IANA timezone.
2. Run `scripts/run.py` with natal and target arguments.
3. Preserve the natal chart and return dynamic layers separately.
4. For each transformation, retain origin palace, origin stem, target star fact, target palace fact, rule IDs, and source IDs.
5. Use the shared timeline interval convention: start inclusive, end exclusive.
6. Cite `ZIWEI-TIMING-ROTATION-001`, `ZIWEI-CYCLE-DECADAL-001`, and `ZIWEI-TRANSFORMATION-DYNAMIC-001`.
7. State the nominal-age policy and apply [references/safety.md](references/safety.md).

Do not translate a period boundary into a promise that an event will occur.
