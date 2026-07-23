---
name: ziwei-core
description: Explain validated project-native Ziwei v0.5 palace, star, classical-brightness, empty-palace, three-directions-four-alignments, and transformation structures with fact, rule, and source citations. Use for 紫微本命结构解读 or cited core summaries after calculation. Experimental until expert acceptance; do not assign fixed events, deterministic fortune, diagnoses, identities, or unsupported brightness meanings.
---

# Ziwei core

Generate an experimental structural explanation whose citations can be mechanically audited.

## Workflow

1. Require a valid chart whose lineage is `project-native-ziwei-structural-v0.5`.
2. Run `scripts/run.py` using explicit natal inputs.
3. Keep stable term IDs separate from simplified Chinese, traditional Chinese, or English labels.
4. For every section, retain non-empty `fact_ids`, `rule_ids`, and `source_ids`.
5. Explain palace location, major-star occupancy, empty-palace status, 三方四正, and bounded brightness only as structural relationships.
6. Cite `ZIWEI-CORE-STRUCTURE-001`, `ZIWEI-PALACE-EMPTY-001`, and `ZIWEI-PALACE-SURROUNDED-001`.
7. Display `experimental` and `expert_acceptance_pending`; apply [references/safety.md](references/safety.md).

Do not hide the release gate. Practitioner acceptance and domain sign-off are external review
requirements and are not satisfied by passing software tests.
