---
name: vedic-calculator
description: Calculate a traceable multi-lineage Vedic astrology chart using a fixed-Spica true-Citra sidereal origin, mean lunar nodes, strict IANA time handling, seven classical planets, lagna, nakshatra and whole-sign houses. Use for Jyotisha or Indian astrology chart requests, before any Parashari, Jaimini, or KP structural analysis, and when reproducible chart JSON is required.
---

# Vedic calculator

Produce astronomical and structural facts before any lineage-specific
explanation.

## Workflow

1. Require a local Gregorian date-time without a numeric offset, an IANA time
   zone, east-positive longitude, and latitude.
2. Require `fold=0` or `fold=1` for a repeated DST time; reject nonexistent
   local times.
3. Use `ayanamsha: true_citra`. Do not relabel it Lahiri, Raman, KP, or another
   named policy.
4. Select one or more explicit `lineages`: `parashari`, `jaimini`, and `kp`.
5. For Jaimini, preserve `jaimini_karaka_policy: seven|eight`; never merge the
   two rankings.
6. Run `scripts/calculate.py <input.json>` and return the structured result.
7. State the true-Citra, mean-node, whole-sign, and lineage-module policies and
   preserve all warnings.

Read [references/data-contract.md](references/data-contract.md) before accepting
input. Never replace a calculator error with a remembered or approximate chart.

## Guardrails

- Keep `computed_facts`, `derived_findings`, and `narrative` separate.
- Do not invent yogas, strengths, dignities, remedies, predictions, or event
  guarantees.
- Treat the KP result as stellar identity only, not a complete KP chart.
- Never import an external astrology repository at runtime.
