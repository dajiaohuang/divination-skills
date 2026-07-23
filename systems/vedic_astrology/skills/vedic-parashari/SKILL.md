---
name: vedic-parashari
description: "Calculate and explain only the bounded Parashari structural layer of a validated Vedic chart: sidereal rashi positions, whole-sign bhavas, nakshatra and pada, D9 navamsha signs, and a declared-year Vimshottari mahadasha schedule. Use for Parashari, BPHS, navamsha, nakshatra, or Vimshottari calculation requests. Do not infer yogas, strength, events, or remedies."
---

# Vedic Parashari

Use only the declared `parashari-structural-v0.1` module.

## Workflow

1. If no validated Vedic result exists, collect the required birth data and
   run `scripts/calculate.py <input.json>` with
   `lineages: ["parashari"]`.
2. Confirm the result declares `ayanamsha: true_citra`, `node_policy: mean`,
   and `house_policy: whole_sign_from_sidereal_lagna`.
3. Report rāśi positions, bhāva numbers, nakṣatra/pāda, D9 sign, or
   Vimśottarī mahādaśā timing only when asked.
4. For daśā timestamps, disclose the `365.2425`-day computational-year policy.
5. Cite the fact's `rule_ids` and `source_ids`; keep explanation subordinate
   to the structured output.

Read [references/lineage-policy.md](references/lineage-policy.md) before
describing D9 or Vimśottarī.

## Guardrails

- Do not add unimplemented vargas, yogas, avasthās, ṣaḍbala, aṣṭakavarga,
  gochara judgments, compatibility scores, remedies, or predictions.
- Do not import Jaimini kārakas or KP sub-lords into a Parāśarī conclusion.
- Do not hide the ayanāṃśa, node, house, or daśā-year policies.
