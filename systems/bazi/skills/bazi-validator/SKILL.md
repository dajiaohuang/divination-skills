---
name: bazi-validator
description: Validate Bazi inputs and structured chart JSON for schema conformance, IANA time-zone handling, solar-term and day-boundary policy, required provenance, calculator version, and unsupported assumptions. Use when a user supplies an existing Bazi chart, asks to 校验八字/核对四柱/检查排盘, or before bazi-core interprets data from any external source.
---

# Bazi validator

Validate facts before interpretation.

## Workflow

1. If the input is repository calculator JSON, run `scripts/validate_chart.py <chart.json>`.
2. If the input is a screenshot, PDF, or prose chart, extract birth data and four pillars separately. Do not treat visual extraction as verified calculation.
3. Confirm local date-time, IANA zone, UTC instant, `fold`, day-boundary policy, exact term boundary, engine version, and source IDs.
4. Recalculate with `$bazi-calculator` when birth data is available. Compare every pillar.
5. Classify differences as input mismatch, time-zone mismatch, boundary-policy dispute, extraction error, or calculator disagreement.
6. Return `valid`, `valid_with_warnings`, or `invalid`. List each issue and the minimum corrective action.

Read [references/validation-policy.md](references/validation-policy.md) before accepting external chart material.

## Guardrails

- Never repair a pillar silently.
- Do not choose between disputed policies without naming the selected policy.
- Block downstream interpretation when a difference could change the day or hour pillar.
- Treat unsupported true-solar-time claims as unverified, not as a small rounding difference.
