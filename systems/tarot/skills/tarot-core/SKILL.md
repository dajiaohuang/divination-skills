---
name: tarot-core
description: Explain a validated project Tarot draw using exact card facts, orientations, named positions, and optional adjacent arcana/element/suit/rank relations. Use for 塔罗解读、多牌阵、组合关系、正逆位说明 or reflective follow-up after `$tarot-draw`. Do not invent cards, redraw, claim third-party facts, or guarantee events.
---

# Tarot core

Explain the existing draw without changing it.

## Workflow

1. Require structured draw output with `validation.status=valid`; otherwise invoke `$tarot-draw` or reject mismatched external data.
2. For each card, retain its `fact_id`, position, card ID, arcana, rank, suit, element, identity
   lineage, source IDs, and orientation exactly.
3. Use the corresponding project-authored orientation keywords and constrain language by the named position.
4. Cite `TAROT-CARD-IDENTITY-001` for RWS identity and `TAROT-POSITION-001` plus the applicable
   orientation rule for every interpretive statement.
5. Read multiple cards in position order; when combinations are requested, expose only
   `TAROT-COMBINATION-RELATION-001` metadata facts.
6. Frame the output as reflection, questions, tradeoffs, or small reversible actions—not facts or fixed predictions.
7. End with limitations and professional-advice routing for high-impact decisions.

Run `scripts/explain.py <draw.json>` for the canonical evidence-linked JSON report. Read [references/safety.md](references/safety.md) before handling health, law, money, coercion, surveillance, death, or third-party questions.
