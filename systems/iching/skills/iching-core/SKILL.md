---
name: iching-core
description: Cast or explain an auditable three-coin I Ching hexagram with bottom-to-top lines, explicit moving-line selection policy, changed hexagram, King Wen identifiers, and edition-aware classical source locators. Use for 易经三钱起卦, reproducible casts, moving-line routing, or checking a structured cast. Do not quote absent texts, hide the seed, merge selection policies, or guarantee outcomes.
---

# I Ching core

Keep calculation facts separate from project-authored reflection.

## Workflow

1. Run `scripts/run.py`, optionally with `--question` and a 64-character `--seed-hex`.
2. Preserve coin totals, six bottom-to-top lines, moving positions, trigram IDs, King Wen numbers, cast ID, and disclosed seed.
3. Use `ICHING-HEXAGRAM-MAP-001` for the primary structure and `ICHING-MOVING-LINES-001` for the changed structure.
4. Use `ICHING-STRUCTURAL-REFLECTION-001` only for bounded reflection.
5. Require either `all-moving-lines-v0.2` or `zhu-xi-count-routing-v0.2`; never merge them.
6. Return classical source locators with `text_included: false` and preserve
   `version_comparison.status: not_collated`.
7. State that replayability does not establish predictive validity.
8. Apply [references/safety.md](references/safety.md) for high-impact or third-party questions.

The JSON report is the canonical result. If an external cast lacks its line order, coin convention, or source, treat it as unvalidated.
