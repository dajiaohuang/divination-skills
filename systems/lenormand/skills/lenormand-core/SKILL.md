---
name: lenormand-core
description: Create or explain an auditable, text-only 36-card Lenormand draw using the project single, three-card, or nine-card layouts. Use for Lenormand draws, 雷诺曼抽牌, card-sequence reflection, or replaying a disclosed seed. Do not use reversals, invent cards, claim hidden facts, or guarantee future events.
---

# Lenormand core

Use the project's fixed 36-card text deck and preserve the draw as immutable evidence.

## Workflow

1. Ask for or choose `single`, `three-card`, or `nine-card`; do not silently substitute another layout.
2. Run `scripts/run.py --spread <spread>` and optionally provide `--question` or `--seed-hex`.
3. Report the disclosed seed, deck hash, draw ID, positions, symbol IDs, and names exactly.
4. Explain each symbol with `LENORMAND-CARD-UPRIGHT-001` and `LENORMAND-POSITION-001`.
5. Read the ordered sequence only through `LENORMAND-SEQUENCE-001`; do not use reversals in this lineage.
6. Treat the result as a reflective comparison, not evidence or a fixed prediction.
7. Apply [references/safety.md](references/safety.md) to health, legal, financial, crisis, surveillance, death, or third-party questions.

The script emits one evidence-linked JSON object. Reuse its `seed_hex` to reproduce a draw exactly.
