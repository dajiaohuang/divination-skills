# ADR-0002: Preserve licensing options until the owner chooses a distribution model

- Status: superseded by ADR-0003
- Date: 2026-07-23

## Context

The roadmap allows closed-source, open-core, and dual-license products. Choosing an open-source license now would grant irreversible permissions without a confirmed business model or copyright-holder attribution.

## Decision

Do not add a repository-wide license yet. The default legal state remains no license granted. Each external dependency and source still requires an explicit manifest and compatibility review.

Before the first external distribution, the owner must choose and document one of:

- a permissive open-source license;
- an open-core split with separately licensed directories;
- a reciprocal license;
- proprietary distribution terms;
- a dual-license model.

## Consequences

- The repository must not be represented as open source while this ADR remains active.
- Outside contributions should not be accepted until contribution licensing is defined.
- Reference code licenses do not determine the license of independently authored project files.
