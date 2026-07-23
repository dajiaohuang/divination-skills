---
name: numerology-core
description: Calculate and explain a traceable project Pythagorean or isolated Chaldean numerology profile from a name and Gregorian birth date, requiring explicit user-supplied Latin transliteration for non-Latin names. Use for 数字命理、生命灵数、姓名数、Chaldean mapping or reduction audits. Do not infer transliteration, mix mappings, claim measured personality, or guarantee events.
---

# Numerology core

Use only the frozen mapping and show every reduction.

## Workflow

1. Require a name, `YYYY-MM-DD` birth date, and explicit `mapping`.
2. If any non-Latin alphabetic character is present, require a complete user-supplied Latin
   `transliteration`; never infer it.
3. Run `scripts/calculate.py <input.json>`.
4. Show mapping lineage, transliteration policy, normalized letters, raw totals, reduction steps,
   final values, and master-number policy.
5. Cite `NUMEROLOGY-CAL-CHALDEAN-NAME-001` only for Chaldean name totals.
6. Present themes as optional reflection prompts, not facts about identity or destiny.
7. Reject silent mapping switches or inferred transliteration.

Read [references/lineage.md](references/lineage.md) for the exact mapping. For high-impact questions, prioritize real evidence and relevant professional guidance.
