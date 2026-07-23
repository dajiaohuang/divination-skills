---
name: runes-core
description: Create or explain an auditable, text-only 24-symbol Elder Futhark draw while strictly separating Old English historical name evidence from project-authored modern reflection. Use for rune draws, 卢恩符文抽取, historical-source questions, symbolic reflection, or seed replay. Do not use reversals, claim historical continuity, reveal hidden facts, or guarantee events.
---

# Runes core

Use the project's fixed Elder Futhark order and original project keywords; distinguish it from a claim of reconstructed historical divination practice.

## Workflow

1. Ask for or choose `single` or `three-rune`; never silently substitute another layout.
2. Run `scripts/run.py --spread <spread>` and optionally provide `--question` or `--seed-hex`.
3. Preserve the disclosed seed, deck hash, draw ID, positions, symbol IDs, and names.
4. Return `RUNES-HISTORICAL-LAYER-001` name evidence separately from
   `RUNES-MODERN-REFLECTION-LAYER-001` prompts.
5. Compare symbols in position order only through `RUNES-SEQUENCE-001`; this lineage has no reversals.
6. State that the historical source does not support the modern divinatory keywords.
7. Apply [references/safety.md](references/safety.md) to high-impact or third-party questions.

The script emits evidence-linked JSON. Supplying its `seed_hex` exactly replays the draw.
