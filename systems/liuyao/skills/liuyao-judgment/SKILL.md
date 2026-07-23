---
name: liuyao-judgment
description: Analyze a valid Wen Wang Najia Liuyao chart with an explicit project question-category rule pack, transparent structural strength components, moving/change relations, and optional branch-only timing candidates. Use after $liuyao-core when the user explicitly requests 用神、旺衰、动变 or 应期 structure. Do not claim a universal school, a guaranteed outcome, or an event date.
---

# Liuyao judgment

Apply only reviewed repository rules to an existing chart.

## Workflow

1. Require a valid JSON chart produced by `$liuyao-core`.
2. Require one explicit category: `self`, `counterpart`, `career`, `finances`,
   `documents`, `children_relief`, or `peers_competition`.
3. Run `scripts/analyze.py --chart ... --question-category ...`.
4. Add `--include-timing` only when branch-level timing candidates were requested.
5. Preserve all source chart facts. Cite the returned fact, rule, and source IDs.
6. Report support, counterevidence, and limitations; keep status `underdetermined` when no
   candidate line exists.
7. State that the project score is pending practitioner review and is not an empirical
   probability.

Do not convert branch candidates into calendar dates, infer a promised event, or silently
substitute another Liuyao lineage.
