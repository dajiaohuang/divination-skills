---
name: western-natal
description: Calculate a structured tropical Western natal chart with geocentric Sun-through-Pluto positions, Ascendant, Midheaven, whole-sign or equal houses, retrograde motion, and fixed-orb major aspects. Use for 西方占星排盘、本命盘、行星落座、宫位、相位 or reproducible chart JSON. Do not approximate Placidus, transits, synastry, progressions, or unsupported bodies.
---

# Western natal

Produce astronomical and structural facts before interpretation.

## Workflow

1. Require local Gregorian date/time without a numeric offset, IANA time zone, east-positive longitude, and latitude.
2. Require `fold=0` or `fold=1` for a repeated DST time; reject nonexistent times.
3. Default to `whole_sign`; use `equal` only when explicitly requested. Reject any other house system.
4. Run `scripts/calculate.py <input.json>` and return the structured chart.
5. State the tropical/geocentric frame, engine version, house system, coordinate/time policy, and unsupported modules.
6. Invoke `$western-core` only when the user requests symbolic explanation.

Read [references/calculation-policy.md](references/calculation-policy.md) for the frozen baseline. Never replace missing astronomical facts with model memory.
