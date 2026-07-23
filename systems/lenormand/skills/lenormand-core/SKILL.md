---
name: lenormand-core
description: Create or explain an auditable, text-only 36-card Lenormand draw using single, three-card, nine-card, or four-by-nine Grand Tableau layouts, including ordered pairs, grid lines, houses, and optional Man/Woman coordinates. Use for Lenormand draws, 雷诺曼抽牌, 九宫, Grand Tableau, or seed replay. Do not use reversals, claim hidden facts, or guarantee events.
---

# Lenormand core

Use the project's fixed 36-card text deck and preserve the draw as immutable evidence.

## Workflow

1. Ask for `single`, `three-card`, `nine-card`, or `grand-tableau`; do not silently
   substitute another layout.
2. Run `scripts/run.py --spread <spread>` and optionally provide `--question` or `--seed-hex`.
3. Report the disclosed seed, deck hash, draw ID, positions, symbol IDs, card numbers, French playing-card correspondences, and names exactly.
4. Use `LENORMAND-CARD-IDENTITY-001` for historical identity. Explain each symbol separately with `LENORMAND-CARD-UPRIGHT-001` and `LENORMAND-POSITION-001`.
5. Use `LENORMAND-PAIR-001`, `LENORMAND-NINE-GRID-001`, and
   `LENORMAND-GRAND-TABLEAU-001` only when their layouts apply.
6. Treat an optional Man/Woman significator as coordinates, not a real person's private state.
7. Treat the result as a reflective comparison, not evidence or a fixed prediction.
8. Apply [references/safety.md](references/safety.md) to health, legal, financial, crisis, surveillance, death, or third-party questions.

The script emits one evidence-linked JSON object. Reuse its `seed_hex` to reproduce a draw exactly.
Do not attribute project keywords to the historical Game of Hope pack.
