---
name: bazi-core
description: Explain a validated Bazi chart using only traceable computed facts and reviewed structured rules. Use for 八字基础解读、四柱说明、日主/十神/藏干/地支关系解释, or questions about a chart already accepted by bazi-validator. Do not use for unsupported strength scoring, useful-god selection, fixed event prediction, or unvalidated external charts.
---

# Bazi core

Explain the validated chart without turning symbolic relationships into deterministic life claims.

## Preconditions

- Require structured calculator output with `validation.status=valid`.
- If only birth data exists, invoke `$bazi-calculator` first.
- If external chart data exists, invoke `$bazi-validator` first.
- Stop when a mismatch could alter the day or hour pillar.

## Workflow

1. State the calculation basis: time zone, day boundary, solar-time policy, and nearby term warning.
2. Summarize the four pillars and day master as facts.
3. Describe visible and hidden Ten Gods as relationship labels, not personality verdicts.
4. List branch relations with their participating pillar positions. Do not invent transformations or outcomes.
5. Describe optional luck cycles only as calculated sequences and method-specific ages.
6. For each explanation, cite the `fact_id`; cite a reviewed rule ID only when a machine rule actually supports the statement.
7. End with known limitations and the exact additional lineage module needed for deeper analysis.

For a reproducible JSON report, run `scripts/explain.py <validated-chart.json>` from this skill directory. The script evaluates reviewed rules into `derived_findings` while preserving `computed_facts` byte-for-byte at the data-model level.

Do not infer strength silently. Only when the user explicitly requests the isolated engineering baseline, pass `--strength-lineage project-seasonal-support-v0.1`, disclose that it is low-confidence and pending external expert approval, and show its complete feature vector.

Read [references/interpretation-policy.md](references/interpretation-policy.md) for allowed language and [references/safety.md](references/safety.md) for high-risk questions.

## Output shape

Use these compact sections: calculation basis, verified facts, symbolic relationships, method-specific timing data, limitations. Separate facts from commentary explicitly.
