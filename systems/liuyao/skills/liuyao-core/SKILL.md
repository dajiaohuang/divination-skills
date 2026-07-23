---
name: liuyao-core
description: Cast and calculate an auditable Wen Wang Liuyao structure with timestamped month/day context, eight-palace stage, 世应, 纳甲, 六亲, 六神, and 旬空. Use for 六爻排盘, 文王纳甲 structure, replaying a seed, or validating a structured Liuyao chart. Do not select 用神, score 旺衰, predict outcomes or timing, or blend this silently with general I Ching text reading.
---

# Liuyao core

Calculate the v0.1 structure while keeping every unresolved judgment outside the result.

## Workflow

1. Require `--local-datetime` and an IANA `--timezone`; state the `--day-boundary` if it is not `midnight`.
2. Run `scripts/run.py` with optional question and 64-character seed.
3. Preserve coin facts, primary/change hexagrams, calendar normalization, palace and stage, 世应, six 纳甲 lines, 六亲, 六神, and 旬空.
4. Cite `LIUYAO-NAJIA-001`, `LIUYAO-PALACE-SHIYING-001`, and `LIUYAO-CALENDAR-CONTEXT-001` for calculation claims.
5. Enforce `LIUYAO-STRUCTURAL-BOUNDARY-001`: do not select 用神 or infer 旺衰, outcome, or timing.
6. Keep Liuyao separate from `$iching-core`; one is a timestamped 纳甲 calculation, the other is a structural three-coin I Ching reading.
7. Apply [references/safety.md](references/safety.md) to high-impact and third-party questions.

Treat external charts without time-zone, day-boundary, line-order, or school metadata as unvalidated.
