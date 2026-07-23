---
name: bazi-calculator
description: Calculate a traceable Bazi (Four Pillars/八字/四柱) chart from a Gregorian local birth date-time and IANA time zone. Use when a user asks to 排八字、排四柱、算生辰八字, calculate year/month/day/hour pillars, inspect Ten Gods or hidden stems from birth data, or obtain structured Bazi JSON. Also use before any Bazi interpretation when no validated chart exists.
---

# Bazi calculator

Produce deterministic chart facts. Do not interpret strength, structure, useful gods, or life events.

## Workflow

1. Collect `local_datetime` and an IANA `timezone`. Never infer a time zone from a city name without resolving it explicitly.
2. Treat `day_boundary` as `midnight` unless the user explicitly selects `zi_initial` for a 23:00 change.
3. Reject ambiguous DST times without `fold`; reject nonexistent DST times.
4. Do not apply true solar time. Coordinates are metadata only in v0.1.
5. Include luck cycles only when the user explicitly supplies `forward` or `reverse` direction.
6. Write an input JSON object and run `scripts/calculate.py <input.json>` from the skill directory.
7. Return the structured JSON or preserve it as the primary artifact. Any prose summary must quote facts from that output.

Read [references/data-contract.md](references/data-contract.md) for fields and failure behavior. Read [references/lineage.md](references/lineage.md) when a boundary, solar-time, or luck-cycle policy matters.

## Guardrails

- Never calculate critical boundaries from memory.
- Never replace a calculator error with an approximate pillar.
- Keep `computed_facts`, `derived_findings`, and `narrative` separate.
- State that the output follows the documented v0.1 policy when the user expects a different lineage.
