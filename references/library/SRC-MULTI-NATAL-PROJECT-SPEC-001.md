---
source_id: "SRC-MULTI-NATAL-PROJECT-SPEC-001"
title: "Project-authored multi-natal orchestration and synthesis contract v0.1"
parser_version: "1.0.1"
retrieved_at: "2026-07-24"
manifest_path: "systems/multi_natal/sources/SRC-MULTI-NATAL-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "df7a40968ac2ad5c63ec9dd8b8853bbe5611aafc27240c123c4d41a593b6ef1e"
license: "Apache-2.0"
---

# Project-authored multi-natal orchestration and synthesis contract v0.1

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-MULTI-NATAL-PROJECT-SPEC-001`
- Manifest: `systems/multi_natal/sources/SRC-MULTI-NATAL-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `0.1.0`
- Retrieved: `2026-07-24`
- Usage status: `production`
- Systems: `multi-natal`
- Lineages: `cross-system-structural-bridge-v0.1`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Project-authored orchestration contracts are released under Apache-2.0.

## Locator capture ledger

### Locator 1

- Registered: systems/multi_natal/DATA_CONTRACT.md
- Resolved: systems/multi_natal/DATA_CONTRACT.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `f906046b18df707f0a4cee17b4e5e866c2ebc093519941db929f1ce642c7aa79`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Multi-natal data contract v0.1

## Required input

```json
{
  "birth_date": "1999-09-15",
  "birth_time": "19:05",
  "birthplace": {
    "name": "Nanjing, Jiangsu, China",
    "timezone": "Asia/Shanghai",
    "longitude": 118.7969,
    "latitude": 32.0603,
    "resolution_source": "user_confirmed"
  },
  "calculation_gender": "female"
}
```

`birthplace.name` is display metadata. The IANA time zone and coordinates are
the calculation inputs. An unresolved or ambiguous place name must not be guessed.
`calculation_gender` is passed only to Ziwei and must be explicitly supplied; it
is not inferred from a name or profile.

## Optional policies

```json
{
  "fold": 0,
  "policies": {
    "east_asian_time_basis": "civil",
    "bazi_day_boundary": "midnight",
    "bazi_luck_cycle_direction": null,
    "western_house_system": "whole_sign",
    "ziwei_year_boundary": "lunar_new_year",
    "ziwei_late_zi_policy": "current_day",
    "ziwei_leap_month_policy": "preserve",
    "vedic_lineages": ["parashari", "jaimini", "kp"],
    "jaimini_karaka_policy": "seven"
  }
}
```

An optional `numerology` object contains `name`, optional `transliteration`, and
one or both mappings from `pythagorean` and `chaldean`.

## Output

The result follows the repository four-layer report contract:

1. `normalized_input`;
2. immutable native charts and cross-checks under `computed_facts`;
3. evidence-linked `derived_findings`;
4. a bounded `narrative`.

The output never persists the birth profile by itself. Callers must apply the
shared consent and privacy contracts before storage.

### Locator 2

- Registered: systems/multi_natal/LINEAGE.md
- Resolved: systems/multi_natal/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `3e4dcb0b8fb740b5fd25d4d7851f48e25a14d87afeb1b14b83139f95548f87af`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Multi-natal lineage policy

Lineage: `cross-system-structural-bridge-v0.1`.

The bridge owns routing and presentation only. Every calculation remains under
the versioned lineage and policies recorded by its native engine.

## Required isolation

- Bazi day-boundary, time-basis, and luck-direction choices stay in the Bazi chart.
- Western output remains tropical and retains its selected house system.
- Ziwei retains its own calendar, late-Zi, time-basis, and calculation-gender policies.
- Vedic output remains sidereal; Parāśarī, Jaimini, and KP Stellar modules remain separate.
- Numerology mappings remain separate and require explicit transliteration when applicable.

The synthesis axes are navigation aids. Selecting two facts under the same axis
does not assert that the facts, symbols, schools, or evidential status are equivalent.

### Locator 3

- Registered: systems/multi_natal/SCOPE.md
- Resolved: systems/multi_natal/SCOPE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `cdae3cdf947295b7da732e8c2b3df0e194f00a0621ff22013797b7bc25c75488`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Multi-natal synthesis scope

This is an orchestration system, not a new divination lineage. It normalizes one
consented birth profile and independently runs:

- Bazi;
- Western natal astrology;
- project-native Ziwei Dou Shu;
- Vedic astrology with explicitly selected Parāśarī, Jaimini, and/or KP Stellar modules;
- optional Pythagorean and/or Chaldean numerology when a usable name is supplied.

The output contains every native chart unchanged, objective time/astronomy
cross-checks, per-system summaries, and a bounded structural crosswalk.

It does not score agreement, merge zodiac systems, invent a universal element
model, or convert symbolic recurrence into a factual or predictive claim.

### Locator 4

- Registered: common/report-spec/AUDITABLE_REPORT.md
- Resolved: common/report-spec/AUDITABLE_REPORT.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `9be7bf146441943c105065d8c4a49be2d25a10fd8c0de19c87f3193c2297494c`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Auditable report contract v0.1

Every runtime result separates four layers:

1. `normalized_input`: validated calculation or draw parameters, including explicit lineage and time/randomness policy.
2. `computed_facts`: immutable, reproducible facts. Each addressable fact should carry a stable `fact_id` and source IDs where practical.
3. `derived_findings`: rule results that cite rule IDs, evidence, confidence, and sources. Findings never overwrite computed facts.
4. `narrative`: user-facing statements. Every factual or symbolic statement must cite at least one fact ID and one rule ID. Limitations may be plain strings.

The result also includes:

- `schema_version`;
- engine name, version, dependencies, and source IDs;
- validation status and warnings;
- audit data required to replay randomized results.

Writers must deep-copy or otherwise protect `computed_facts` before rule evaluation. A report is invalid if narrative references an unknown fact or rule, if a cross-system rule appears without an explicit bridge contract, or if missing calculation facts are reconstructed from model memory.

Composition uses the common contracts in `common/schemas/`:

- `reading-session` links one or more validated charts to an explicit question and consent scope;
- `confidence-profile` records which modules are allowed, degraded, or blocked;
- `timeline` carries calculated periods without narrative claims;
- `comparison` records directional two-chart facts;
- `report-profile` selects report sections but does not define new rules;
- `chart-import` records external-field mappings and preserves native calculations as canonical.

Raw question text, chart IDs, consent records, and birth inputs must be removed before operational
logging. Existing v0.1 chart documents can be wrapped without rewriting them, as recorded in
ADR-0004.

## Manifest quality note

Defines routing, audit, and non-equivalence policy; it does not validate any divination system empirically.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `df7a40968ac2ad5c63ec9dd8b8853bbe5611aafc27240c123c4d41a593b6ef1e`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
