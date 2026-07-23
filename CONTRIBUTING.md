# Contributing

## Required workflow

1. Open or reference an issue describing the source, rule, case, calculation, or Skill change.
2. For external material, add or update its source manifest before adding derived project data.
3. Keep computed facts, rule-derived findings, and narrative output separate.
4. Add tests for every deterministic change and at least one counterexample for every new rule.
5. Run `python -m divination_skills.validation .` and `pytest` before requesting review.
6. Do not commit files under `references/upstream/`, secrets, personal birth data, or generated `dist/` artifacts.

## Review requirements

- Calculation changes require a reproducible fixture and independent comparison source.
- Rule changes require a precise source locator and lineage.
- Disputed rules require a dispute record; reviewers must not silently select a school.
- Production knowledge requires accepted rights review and domain review.
- Skill changes must pass the Skill validator and use the single source under `systems/<system>/skills/`.

## Commit scope

Keep governance, schemas, calculators, rules, cases, and generated artifacts in separate commits when practical. Generated artifacts must never be edited by hand.

## Inbound licensing

Unless explicitly stated otherwise by the contributor, contributions intentionally submitted for
inclusion are accepted under Apache-2.0 section 5, without additional terms. Contributors must have
the authority to submit their work and must not copy material from ignored reference repositories.
Opening an issue without submitting a contribution does not transfer rights.
