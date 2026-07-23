# ADR-0003: License project-authored material under Apache-2.0

- Status: accepted
- Date: 2026-07-23
- Supersedes: ADR-0002

## Context

The owner chose to publish the project as open source and explicitly selected Apache License 2.0.
Reference repositories must remain ignored and outside the project license grant.

## Decision

License project-authored code, Skills, rules, schemas, synthetic fixtures, documentation, and
generated packages under Apache-2.0. Accept intentionally submitted contributions under section 5
unless a contributor explicitly states otherwise.

Keep every upstream reference under ignored `references/upstream/`. No reference repository may be
a Git submodule, runtime dependency, vendored component, or implicit source of missing facts.

## Consequences

- Public and commercial redistribution of project-authored material is allowed under Apache-2.0.
- External dependencies and source material retain their own licenses and review requirements.
- Open-source licensing does not satisfy domain, rights, privacy, or deployment approval gates.
