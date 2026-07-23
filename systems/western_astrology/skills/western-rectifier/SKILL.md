---
name: western-rectifier
description: Scan Western birth-time intervals against at least five dated historical events split into training and holdout sets, using transit contacts to candidate angles. Use for birth-time candidate ranking, retained-event rectification, or underdetermination checks. Do not promise a unique minute, use personality descriptions as tie-breakers, skip holdout validation, infer missing event details, or hide insufficient evidence.
---

# Western rectifier

1. Require birth date, IANA timezone, coordinates, at least five dated event ranges, evidence quality, and training/holdout labels.
2. Run `scripts/run.py --birth-date ... --events ... --interval-minutes 30`.
3. Rank declared time intervals with training events and check the holdout set.
4. Return `underdetermined` when evidence does not separate candidates.
5. Cite `WESTERN-RECTIFIER-EVENT-SCAN-001`.
6. Apply [references/safety.md](references/safety.md).

Never use personality descriptions to break ties or claim that event contacts prove causation.
