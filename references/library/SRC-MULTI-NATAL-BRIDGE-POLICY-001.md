---
source_id: "SRC-MULTI-NATAL-BRIDGE-POLICY-001"
title: "Project-authored cross-system structural bridge policy v0.1"
parser_version: "1.0.1"
retrieved_at: "2026-07-24"
manifest_path: "systems/multi_natal/sources/SRC-MULTI-NATAL-BRIDGE-POLICY-001.json"
capture_mode: "full"
aggregate_payload_sha256: "f1678ba2307cb3027e866b905d9438898695ff13e98667415b9014370d7b3d64"
license: "Apache-2.0"
---

# Project-authored cross-system structural bridge policy v0.1

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-MULTI-NATAL-BRIDGE-POLICY-001`
- Manifest: `systems/multi_natal/sources/SRC-MULTI-NATAL-BRIDGE-POLICY-001.json`
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
- Evidence: Project-authored bridge policy is released under Apache-2.0.

## Locator capture ledger

### Locator 1

- Registered: systems/multi_natal/KNOWN_DISPUTES.md
- Resolved: systems/multi_natal/KNOWN_DISPUTES.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `f3c297b6e2cc47875e287f5ce53bc6a95eeec4101cf4d7bfa19dadf7fb0ac967`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Known multi-natal disputes

## Cross-system comparability

There is no consensus ontology that makes a Bazi Day Master, Western Sun,
Ziwei Life Palace, and Vedic Lagna equivalent. The project groups them only as
candidate navigation points and records `DSP-MULTI-NATAL-COMPARABILITY-001`.

## Time basis

Civil time and apparent solar time may place Bazi or Ziwei calculations on a
different double hour or date near boundaries. The bridge never silently chooses
apparent solar time merely because coordinates are present.

## Zodiac frames

Western tropical longitudes and Vedic sidereal longitudes are not compared as
sign agreement. Only the independently retained tropical astronomical positions
inside both engines are used for an objective implementation cross-check.

### Locator 2

- Registered: systems/multi_natal/rules/MULTI-NATAL-BRIDGE-001.json
- Resolved: systems/multi_natal/rules/MULTI-NATAL-BRIDGE-001.json
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `f1e0aad5e3800b4db198df1c0ee67673747297f0ba085b091f2f72409ff16b04`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

{
  "rule_id": "MULTI-NATAL-BRIDGE-001",
  "title": "Build non-equivalent structural navigation axes",
  "system": "multi-natal",
  "lineage": "cross-system-structural-bridge-v0.1",
  "version": "0.1.0",
  "status": "tested",
  "kind": "interpretation",
  "conditions": [
    {
      "fact_path": "computed_facts.system_summaries",
      "operator": "exists"
    }
  ],
  "conclusions": [
    {
      "finding_type": "synthesis.structural_crosswalk",
      "output_path": "computed_facts.synthesis_axes",
      "value": "navigation_only",
      "confidence": "low",
      "explanation_template": "Display cited structures together without equivalence, recurrence scoring, or predictive claims."
    }
  ],
  "exceptions": [
    {
      "when": [
        {
          "fact_path": "normalized_input.birthplace.resolution_source",
          "operator": "absent"
        }
      ],
      "effect": "skip",
      "rationale": "An unresolved birth place invalidates time-sensitive cross-system routing."
    }
  ],
  "priority": 70,
  "sources": [
    {
      "source_id": "SRC-MULTI-NATAL-PROJECT-SPEC-001",
      "locator": "LINEAGE.md required isolation",
      "support_type": "direct"
    }
  ],
  "disputes": [
    "DSP-MULTI-NATAL-COMPARABILITY-001"
  ],
  "tests": [
    "CASE-MULTI-NATAL-STANDARD-001",
    "CASE-MULTI-NATAL-DISPUTE-TIME-BASIS-001"
  ]
}

### Locator 3

- Registered: systems/multi_natal/KNOWN_LIMITATIONS.md
- Resolved: systems/multi_natal/KNOWN_LIMITATIONS.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `cbd940c5be0760fa64cd95828070460eb0687f5610cac0846761289b7bdde7ad`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Known multi-natal limitations

- Place-name geocoding is not bundled. A place must resolve to confirmed
  coordinates and an IANA time zone before calculation.
- Historical civil-time accuracy is limited by the installed time-zone database.
- The common supported birth-year interval is 1900 through 2099.
- Bazi luck cycles are omitted unless direction is explicitly supplied.
- KP remains the repository's bounded Stellar/Sub-lord layer, not complete KP.
- Numerology is optional and cannot infer a non-Latin transliteration.
- The synthesis is a source-linked structural index, not empirical validation,
  probability, diagnosis, compatibility verdict, or guaranteed prediction.

## Manifest quality note

Defines the product's non-equivalence policy; it does not establish empirical convergence among divination systems.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `f1678ba2307cb3027e866b905d9438898695ff13e98667415b9014370d7b3d64`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
