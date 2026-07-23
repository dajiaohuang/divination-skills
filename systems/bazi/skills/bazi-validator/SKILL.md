---
name: bazi-validator
description: Validate native Bazi JSON for schema, time boundary, provenance, and engine requirements, then optionally compare a structured import without overwriting either chart. Use for 校验八字, 核对四柱, external chart differences, or pre-interpretation gates. Accept structured JSON only; do not parse screenshots/PDFs, repair pillars silently, infer policies, or treat another engine as automatic truth.
---

# Bazi validator

Validate facts before interpretation.

## Workflow

1. Run `scripts/validate_chart.py <native.json>` for schema and provenance validation.
2. Add `--imported <chart.json>` for path-level pillar and day-boundary comparison.
3. Confirm local date-time, IANA zone, UTC instant, `fold`, day-boundary policy, exact term boundary, engine version, and source IDs.
4. Keep imported and native facts separate; never copy values between them.
5. Classify differences as pillar or boundary-policy differences without deciding a universal winner.
6. Return validation and comparison states separately.

Read [references/validation-policy.md](references/validation-policy.md) before accepting external chart material.

## Guardrails

- Never repair a pillar silently.
- Do not choose between disputed policies without naming the selected policy.
- Block downstream interpretation when a difference could change the day or hour pillar.
- Treat unsupported true-solar-time claims as unverified, not as a small rounding difference.
- Reject screenshots, PDFs, OCR, and prose in this structured validation workflow.
