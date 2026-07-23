---
name: western-timing
description: Calculate tropical geocentric transit-to-natal major aspects, annual solar return, and shared timeline facts from a validated native chart. Use for Western astrology transits, solar return structure, target-date aspect review, or deterministic replay. Do not include progressions, directions, guaranteed event prediction, undeclared house systems, or high-impact decision advice.
---

# Western timing

1. Require a valid native tropical geocentric chart and explicit target local datetime/timezone.
2. Run `scripts/run.py --chart ... --target-local-datetime ... --timezone ...`.
3. Keep transit, natal, and return charts separate.
4. Preserve transit-to-natal direction and exact aspect/orb evidence.
5. Solve the solar return by recurring natal Sun longitude; do not substitute a birthday noon chart.
6. Cite `WESTERN-TIMING-TRANSIT-001` and `WESTERN-TIMING-SOLAR-RETURN-001`.
7. Apply [references/safety.md](references/safety.md).

Secondary progressions and directions are separate lineages and are excluded.
