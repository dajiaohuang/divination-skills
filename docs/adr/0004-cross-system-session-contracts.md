# ADR-0004: Add cross-system session and composition contracts

- Status: accepted
- Date: 2026-07-23

## Context

The v0.1 system contracts describe one chart or draw at a time. Timing, external chart imports,
two-chart comparison, specialist reports, and birth-time uncertainty require shared envelopes
without weakening each system's own chart schema.

## Decision

Add six versioned common contracts:

- reading session;
- chart import;
- confidence profile;
- timeline;
- comparison;
- report profile.

The contracts compose chart references but never replace system chart schemas. Session IDs are
content addressed. Operational logs receive only redacted session metadata. Input precision
controls module access through an explicit requirement table.

External imports remain comparison evidence. The native calculator is always the canonical
authority unless a future, separately reviewed lineage contract says otherwise.

## Compatibility and migration

Existing v0.1 calculators and Skills may continue returning their current chart documents. A
caller that needs composition wraps the existing chart with
`divination_skills.contracts.legacy_chart_reference` and creates a reading session. The wrapper
derives its ID from computed facts and does not copy raw or normalized birth input.

Contract changes follow semantic versioning:

- patch: documentation or validation clarification that accepts the same documents;
- minor: optional fields or enum values with backward-compatible readers;
- major: required-field or semantic changes.

Readers must reject an unsupported major version. Migrations create a new document and preserve
the original; they never edit a signed chart or report in place.

## Consequences

- Systems can add timing and comparison modules without sharing domain rules.
- Question text, chart IDs, consent records, and birth inputs stay out of operational logs.
- Specialist reports are selected by profiles and cannot silently invent missing evidence.
- All six schemas and their canonical examples are checked by repository validation.
