---
name: runes-core
description: Create or explain an auditable, text-only 24-symbol Elder Futhark draw using the project single or three-rune layouts. Use for rune draws, 卢恩符文抽取, symbolic reflection, or replaying a disclosed seed. Do not use reversals, invent symbols, claim historical reconstruction, reveal hidden facts, or guarantee future events.
---

# Runes core

Use the project's fixed Elder Futhark order and original project keywords; distinguish it from a claim of reconstructed historical divination practice.

## Workflow

1. Ask for or choose `single` or `three-rune`; never silently substitute another layout.
2. Run `scripts/run.py --spread <spread>` and optionally provide `--question` or `--seed-hex`.
3. Preserve the disclosed seed, deck hash, draw ID, positions, symbol IDs, and names.
4. Explain each symbol through `RUNES-SYMBOL-UPRIGHT-001` and `RUNES-POSITION-001`.
5. Compare symbols in position order only through `RUNES-SEQUENCE-001`; this lineage has no reversals.
6. State that the reading is a modern reflective prompt, not historical proof, evidence, or a fixed prediction.
7. Apply [references/safety.md](references/safety.md) to high-impact or third-party questions.

The script emits evidence-linked JSON. Supplying its `seed_hex` exactly replays the draw.
