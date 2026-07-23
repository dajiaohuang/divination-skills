---
name: iching-core
description: Cast or explain an auditable three-coin I Ching hexagram with bottom-to-top lines, moving lines, changed hexagram, trigrams, and King Wen identifiers. Use for 易经三钱起卦, reproducible casts, hexagram structure, or checking an existing structured cast. Do not quote absent classical texts, hide the seed, choose an unstated moving-line school, or guarantee outcomes.
---

# I Ching core

Keep calculation facts separate from project-authored reflection.

## Workflow

1. Run `scripts/run.py`, optionally with `--question` and a 64-character `--seed-hex`.
2. Preserve coin totals, six bottom-to-top lines, moving positions, trigram IDs, King Wen numbers, cast ID, and disclosed seed.
3. Use `ICHING-HEXAGRAM-MAP-001` for the primary structure and `ICHING-MOVING-LINES-001` for the changed structure.
4. Use `ICHING-STRUCTURAL-REFLECTION-001` only for bounded reflection.
5. When multiple lines move, report all of them; do not invent a line-priority method or classical quotation.
6. State that replayability does not establish predictive validity.
7. Apply [references/safety.md](references/safety.md) for high-impact or third-party questions.

The JSON report is the canonical result. If an external cast lacks its line order, coin convention, or source, treat it as unvalidated.
