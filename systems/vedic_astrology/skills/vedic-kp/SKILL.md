---
name: vedic-kp
description: "Calculate the bounded KP stellar identity layer for lagna and grahas: sidereal sign lord, nakshatra or star lord, and one of nine unequal Vimshottari-proportional sub-lords. Use for KP sub-lord lookup and boundary auditing. Clearly state that Placidus cusps, cusp sub-lords, ruling planets, significators, horary numbers, and event prediction are not implemented."
---

# Vedic KP stellar layer

Use the exact name `kp-stellar-v0.1`; do not call it a complete KP chart.

## Workflow

1. If no validated chart exists, run `scripts/calculate.py <input.json>`. The
   script forces `lineages: ["kp"]`.
2. Confirm the result declares `true_citra` and mean nodes. Do not relabel the
   ayanāṃśa as KP ayanāṃśa.
3. Return sign lord, star lord, sub-lord, and the half-open sub interval for
   each requested object.
4. Preserve the `unsupported` list and the `kp_stellar_only` warning.
5. Cite `VEDIC-KP-SUBLORD-001` and the source IDs attached to each fact.

Read [references/scope.md](references/scope.md) before answering a KP request.

## Guardrails

- Never use Parāśarī whole-sign houses as KP cusps.
- Never infer cusp sub-lords, ruling planets, significators, promises, timing,
  horary answers, or event outcomes.
- Do not copy modern KP teaching text; report only calculated identities and
  the project's explicit mathematical policy.
