---
name: tarot-draw
description: Produce an auditable, reproducible text-only Tarot draw from the project RWS-compatible 78-card deck. Use when a user asks to 抽塔罗牌、单牌、三牌阵、正逆位, wants a seed-replayable draw, or needs randomness audit data. Do not interpret life outcomes, use modern commercial card images, or silently redraw an unwanted result.
---

# Tarot draw

Create structured draw facts before any interpretation.

## Workflow

1. Reformulate the question as an open reflective prompt when needed; do not promise prediction.
2. Choose one supported spread: `single`, `situation-challenge-guidance`, or `option-a-option-b-focus`.
3. Ask for a seed only when the user wants to supply one. Otherwise allow the script to create and disclose a cryptographic seed.
4. Run `scripts/draw.py <input.json>`.
5. Return the spread positions, cards, orientations, draw ID, deck hash, algorithm, and disclosed seed. Do not hide or reroll a result.
6. Invoke `$tarot-core` only if an explanation is requested.

Read [references/randomness.md](references/randomness.md) when discussing fairness or replay. The draw is symbolic and software-auditable; it cannot prove a metaphysical source of randomness.
