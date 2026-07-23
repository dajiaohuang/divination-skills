# ADR-0001: Use Bazi as the first production vertical

- Status: accepted
- Date: 2026-07-23

## Context

The common contracts need a calculation-heavy system that exposes time-zone, calendar-boundary, lineage, deterministic-rule, and narrative-traceability requirements. The initial audience is assumed to be Chinese-speaking unless product evidence changes that assumption.

## Decision

Use Bazi with a documented Ziping baseline as the first end-to-end implementation. Freeze all year, month, day, hour, solar-time, luck-cycle, and lineage choices in `systems/bazi/LINEAGE.md` before interpreting charts.

Western astrology remains the fallback if the product priority changes to maximum reuse of astronomical infrastructure. Starting both calculation systems before the Bazi vertical passes its exit gate is prohibited.

## Consequences

- The shared schemas must represent historical time zones, calendar boundaries, disputes, and explainable rule chains.
- Bazi sources and expert review become the first domain bottleneck.
- Tarot may be implemented after the first vertical to test stochastic and non-calculation workflows.
