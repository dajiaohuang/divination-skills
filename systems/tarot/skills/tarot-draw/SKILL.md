---
name: tarot-draw
description: Produce an auditable, reproducible text-only Tarot draw from the project RWS-compatible 78-card deck across one-, three-, five-, six-, seven-, and ten-card spreads. Use for 抽塔罗牌、三牌阵、凯尔特十字、正逆位, seed replay, or randomness audit. Do not interpret outcomes, use commercial card images, or silently redraw.
---

# Tarot draw

Create structured draw facts before any interpretation.

## Workflow

1. Reformulate the question as an open reflective prompt when needed; do not promise prediction.
2. Choose one registered spread from the draw engine, including `elemental-five`,
   `relationship-six`, `horseshoe-seven`, or `celtic-cross`.
3. Ask for a seed only when the user wants to supply one. Otherwise allow the script to create and disclose a cryptographic seed.
4. Run `scripts/draw.py <input.json>`.
5. Return the spread positions, cards, arcana, rank, suit, element, RWS identity lineage,
   orientations, draw ID, deck hash, algorithm, source IDs, and disclosed seed. Do not hide or
   reroll a result.
6. Cite `TAROT-CARD-IDENTITY-001` for identity fields. Do not present RWS as universal Tarot or
   attribute project-authored keywords to Waite.
7. Invoke `$tarot-core` only if an explanation is requested.

Read [references/randomness.md](references/randomness.md) when discussing fairness or replay. The draw is symbolic and software-auditable; it cannot prove a metaphysical source of randomness.
