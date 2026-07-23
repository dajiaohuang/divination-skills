---
source_id: "SRC-VEDIC-PROJECT-SPEC-001"
title: "Project-authored Vedic multi-lineage calculation contract v0.1"
parser_version: "1.0.1"
retrieved_at: "2026-07-24"
manifest_path: "systems/vedic_astrology/sources/SRC-VEDIC-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "32c911ccb9845ca2f72934f77831000cb480288bddaa5792298e5737b4bdcce7"
license: "Apache-2.0"
---

# Project-authored Vedic multi-lineage calculation contract v0.1

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-VEDIC-PROJECT-SPEC-001`
- Manifest: `systems/vedic_astrology/sources/SRC-VEDIC-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `0.1.0`
- Retrieved: `2026-07-24`
- Usage status: `production`
- Systems: `vedic-astrology`
- Lineages: `true-citra-common-v0.1`, `parashari-structural-v0.1`, `jaimini-structural-v0.1`, `kp-stellar-v0.1`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Project-authored contracts are released under the repository Apache-2.0 license.

## Locator capture ledger

### Locator 1

- Registered: systems/vedic_astrology/DATA_CONTRACT.md
- Resolved: systems/vedic_astrology/DATA_CONTRACT.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `f67093e86dc67c6cbc787979abe9ba22b94e7fa09ce35ce4af542e17926a251f`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Vedic Astrology data contract

## Input

```json
{
  "local_datetime": "1999-09-15T19:05:00",
  "timezone": "Asia/Shanghai",
  "longitude": 119.917,
  "latitude": 31.30,
  "fold": 0,
  "lineages": ["parashari", "jaimini", "kp"],
  "jaimini_karaka_policy": "seven",
  "ayanamsha": "true_citra"
}
```

Required fields are `local_datetime`, `timezone`, `longitude`, and `latitude`.
`lineages` defaults to all three supported modules. `fold` is required only for
an ambiguous civil time. Unknown fields and nonexistent local times fail
closed.

The only accepted ayanāṃśa in v0.1 is `true_citra`. The only accepted Jaimini
kāraka policies are `seven` and `eight`.

## Output layers

The calculator returns:

1. `raw_input`;
2. `normalized_input`, including the selected policies and exact UTC instant;
3. `computed_facts.astronomy`, with tropical positions and the calculated
   ayanāṃśa;
4. `computed_facts.sidereal_chart`, with grahas, mean nodes, lagna, nakṣatra,
   pāda, and whole-sign house;
5. only the requested lineage modules under
   `computed_facts.lineages.parashari|jaimini|kp`;
6. `warnings`, `rule_ids`, `source_ids`, and `trace`.

Every substantive nested fact carries its own `rule_ids` and `source_ids`.
No natural-language prediction is emitted by the calculator.

## Numerical policies

- Supported civil years: 1900 through 2100.
- Longitudes are normalized to `[0, 360)`.
- Boundary selection uses half-open intervals.
- Stored display longitudes are rounded to eight decimal places; branch
  decisions use unrounded values.
- Vimśottarī schedule timestamps use a proleptic Gregorian duration of
  `365.2425` days per computational year.
- Exact Jaimini degree ties fail with `karaka_tie`.

## Failure codes

The public calculator may return:

- `unknown_fields`
- `missing_<field>`
- `invalid_longitude`
- `invalid_latitude`
- `invalid_lineages`
- `invalid_ayanamsha`
- `invalid_karaka_policy`
- `ambiguous_local_time`
- `nonexistent_local_time`
- `date_out_of_range`
- `karaka_tie`
- `angle_undefined`

### Locator 2

- Registered: systems/vedic_astrology/LINEAGE.md
- Resolved: systems/vedic_astrology/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `2b52fad47eca9fe8c3001ec70192f3d8e0ad66b7a79b185906b95af75ab0379b`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Vedic Astrology lineage policy

## Shared astronomical baseline

All enabled lineages receive the same normalized instant and geocentric
ecliptic facts. Tropical longitudes are converted to sidereal longitudes by
subtracting a dynamically calculated true-Citrā offset: the tropical
ecliptic-of-date longitude of Spica is anchored to 180° sidereal. The fixed
stellar coordinates are the J2000 catalogue values declared in the project
contract; annual aberration and stellar proper motion are not applied to the
anchor. This is not labelled Lahiri, Raman, KP, Yukteśvara, or any other
ayanāṃśa.

Rāhu is the mean ascending lunar node calculated from a documented polynomial;
Ketu is exactly opposite. Users must not compare these node positions to a
true-node chart without changing the policy in a future version.

## Parāśarī structural profile

`parashari-structural-v0.1` uses:

- sidereal rāśis and whole-sign bhāvas from sidereal lagna;
- 27 equal nakṣatras of 13°20′, each divided into four pādas;
- the Ketu–Venus–Sun–Moon–Mars–Rahu–Jupiter–Saturn–Mercury Vimśottarī order;
- navāṃśa signs derived from the movable/fixed/dual starting-sign rule;
- a 365.2425-day computational year for ISO schedule boundaries.

The last item is a software time-scale policy, not a claim that every
Parāśarī school uses the same daśā year length.

## Jaimini structural profile

`jaimini-structural-v0.1` supports two non-mergeable chara-kāraka policies:

- `seven`: Sun through Saturn, excluding the nodes;
- `eight`: Sun through Saturn plus Rāhu, whose within-sign arc is reversed.

Ranks are determined by descending effective degree within a sign. Exact ties
are rejected because silently breaking them would manufacture a lineage rule.

Rāśi dṛṣṭi follows the movable/fixed/dual sign-class relation. Ārūḍha lagna
uses the counted distance from lagna to its lord and repeats that distance from
the lord. When the ordinary result is the source sign or its seventh, this
profile places the ārūḍha tenth from the lord and reports the exception.

## KP stellar profile

`kp-stellar-v0.1` implements only a reproducible stellar identity:

- sidereal sign lord;
- nakṣatra/star lord;
- one of nine unequal sub-lords in Vimśottarī order and proportion.

It intentionally does not reuse whole-sign bhāvas as KP cusps. Complete KP
practice requires a separately sourced and tested cusp, significator, ruling
planet, and judgment layer.

## Source hierarchy

Classical texts establish historical terminology and structural concepts.
Official astronomical material establishes the modern nirayana/panchang
context. Modern Jaimini and KP pages are corroborating, rights-restricted
references only. Project-authored contracts resolve software boundaries and
never present a disputed convention as universal doctrine.

### Locator 3

- Registered: systems/vedic_astrology/KNOWN_DISPUTES.md
- Resolved: systems/vedic_astrology/KNOWN_DISPUTES.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `21f9d3cf53db0ffe7030a03a4d22e6cf69a4f5641d17270baceee4add2238c74`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Known Vedic Astrology disputes

- Ayanāṃśa: Lahiri/Chitrapaksha, Raman, KP, Yukteśvara, true-Citrā and other
  definitions are not numerically interchangeable.
- Lunar nodes: mean and true node policies can change sign, nakṣatra, and
  sub-lord near boundaries.
- Bhāva method: whole-sign rāśi houses, equal houses, quadrant bhāva cusps and
  KP Placidus cusps must not be merged.
- Vimśottarī year: civil, tropical, savana and other year-length conventions
  produce different calendar boundaries.
- Jaimini chara kārakas: seven- and eight-kāraka traditions differ on Rāhu and
  the handling of degree ties.
- Jaimini ārūḍha exceptions and sign-daśā direction/duration rules differ among
  commentators.
- Divisional-chart boundary behavior differs when an upstream calculator
  rounds display degrees before classification.

Each disagreement is exposed as a policy, a dispute record, a limitation, or
an explicit unsupported feature.

## Manifest quality note

Defines software policies and limitations; independent domain acceptance remains pending.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `32c911ccb9845ca2f72934f77831000cb480288bddaa5792298e5737b4bdcce7`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
