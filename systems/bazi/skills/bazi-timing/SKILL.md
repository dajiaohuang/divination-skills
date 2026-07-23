---
name: bazi-timing
description: Calculate an explicitly directed Bazi luck cycle, target year and month pillars, cross-period branch activations, and shared timeline facts from a validated native chart. Use for 八字大运, 流年流月, structural timing windows, or deterministic replay. Do not infer luck direction, predict guaranteed events, mix timing schools, or turn activations into medical, legal, financial, employment, fertility, or mortality advice.
---

# Bazi timing

1. Require a valid native chart with explicit `luck_cycle_direction`.
2. Run `scripts/run.py --chart <json> --target-local-datetime ... --timezone ...`.
3. Return the active luck cycle, year/month pillars, structural relations, and inclusive-start/exclusive-end timeline.
4. Keep timing rules separate from natal interpretation.
5. Cite `BAZI-TIMING-LUCK-CYCLE-001` and `BAZI-TIMING-ACTIVATION-001`.
6. Apply [references/safety.md](references/safety.md).

An activation is evidence of a calculated relation, not evidence that an event will happen.
