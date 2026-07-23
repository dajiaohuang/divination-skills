---
name: western-core
description: Explain a validated tropical Western natal chart as traceable symbolic structure using exact placement, house, angle, retrograde, and major-aspect facts. Use for 本命盘解读、行星落座说明、宫位主题、相位结构 after `$western-natal`. Do not add unsupported dignity, Placidus, transit, synastry, event prediction, identity diagnosis, or high-impact advice.
---

# Western core

Keep astronomical facts immutable and commentary explicitly symbolic.

## Workflow

1. Require a chart with `validation.status=valid`; calculate or validate first if needed.
2. State the tropical/geocentric frame and selected house system.
3. Explain each placement using its exact fact ID, sign, house, and apparent motion. Cite the calculation, house, and structural interpretation rules.
4. Explain each recorded major aspect with its exact orb; do not invent missing aspects.
5. Report Ascendant and Midheaven as calculated angles without adding unsupported personality verdicts.
6. Separate low-confidence reflective language from deterministic calculation facts.
7. End with the exact unsupported module needed for any deeper question.

Run `scripts/explain.py <chart.json>` for the canonical report. Read [references/safety.md](references/safety.md) before responding to identity, compatibility, health, money, law, danger, fertility, or mortality questions.
