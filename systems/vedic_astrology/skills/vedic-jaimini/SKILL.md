---
name: vedic-jaimini
description: Calculate only the bounded Jaimini structural layer of a validated Vedic chart, including selectable seven- or eight-chara-karaka ranking, rashi drishti, and a declared Arudha Lagna exception policy. Use for Jaimini, chara karaka, Atmakaraka, rashi aspect, or Arudha requests. Never combine seven- and eight-karaka results or invent Chara Dasha and predictive judgments.
---

# Vedic Jaimini

Keep Jaimini rules independent from Parāśarī and KP modules.

## Workflow

1. Ask whether the user wants the seven- or eight-kāraka policy. If no choice
   is given, use and disclose `seven`.
2. If no validated chart exists, run `scripts/calculate.py <input.json>` with
   `lineages: ["jaimini"]` and the selected
   `jaimini_karaka_policy`.
3. Report the ranked kārakas with effective within-sign degrees.
4. For the eight-kāraka policy, explicitly show that Rāhu uses the reversed
   within-sign arc.
5. Report rāśi dṛṣṭi as sign-to-sign relations.
6. For ārūḍha lagna, state whether the tenth-from-lord exception was applied.

Read [references/lineage-policy.md](references/lineage-policy.md) before
explaining a disputed policy.

## Guardrails

- Exact effective-degree ties must fail pending an explicit tie policy.
- Do not merge the seven- and eight-kāraka rank lists.
- Do not invent chara daśā, argalā, upapada, longevity, event, or remedial
  judgments.
- Do not present a project-selected exception as universal Jaimini doctrine.
