---
name: ziwei-validator
description: Validate or compare a structured Zi Wei Dou Shu chart against the project-native v0.4 calculation without overwriting either source. Use for 紫微斗数排盘校验, external JSON comparison, palace or star-placement diffs, lineage mismatch review, or reproducible validation reports. Do not invoke iztro, accept screenshots or PDFs, silently normalize another school, or turn differences into life claims.
---

# Ziwei validator

Produce an auditable difference report between a native chart and an untrusted structured import.

## Workflow

1. Require two JSON objects with twelve palaces: the project-native chart and imported chart.
2. Run `scripts/run.py --native <file> --imported <file>`.
3. Preserve imported and native facts separately. Never repair one by copying fields from the other.
4. Report exact JSON paths and classify palace fields as `structural_difference` and star lists as `placement_difference`.
5. Attribute differences to a known lineage or boundary policy only when the input declares it. Otherwise use `unclassified`.
6. Cite `ZIWEI-INPUT-POLICY-001`, `ZIWEI-NATIVE-NATAL-001`, and the relevant placement rule.
7. Apply [references/safety.md](references/safety.md).

This validator accepts structured JSON only. OCR, PDF, screenshots, inferred birth data, and
automatic school conversion are outside scope.
