---
source_id: "SRC-WESTERN-PROJECT-SPEC-001"
title: "Project tropical Western astrology contracts v0.3"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/western_astrology/sources/SRC-WESTERN-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "deb34ed7490114d40e4c8bcd44d929b7913b7a0520d08c51e7d02a7f6bc575ca"
license: "Apache-2.0"
---

# Project tropical Western astrology contracts v0.3

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-WESTERN-PROJECT-SPEC-001`
- Manifest: `systems/western_astrology/sources/SRC-WESTERN-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `0.3.0`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `western-astrology`
- Lineages: `tropical-geocentric-v0.1`, `tropical-geocentric-major-aspects-v0.2`, `tropical-traditional-condition-v0.3`, `western-event-retained-rectification-v0.2`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: The project owner selected Apache-2.0 for project-authored repository material.

## Locator capture ledger

### Locator 1

- Registered: systems/western_astrology/LINEAGE.md
- Resolved: systems/western_astrology/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `21fefb6ad4f6a725719b1aca4b0dad79ee7ccb28c3c72483acd0b3adbf0560e8`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Western astrology lineage

The natal baseline is `tropical-geocentric-v0.1`; v0.2 extensions use
`tropical-geocentric-major-aspects-v0.2`, while retained-event rectification is isolated as
`western-event-retained-rectification-v0.2`.

v0.3 adds `tropical-traditional-condition-v0.3`, an unscored Ptolemaic table layer limited to Sun, Moon, Mercury, Venus, Mars, Jupiter, and Saturn. It never assigns modern outer-planet rulerships.

- Zodiac: tropical, true ecliptic and equinox of date.
- Planet frame: geocentric apparent positions from Astronomy Engine 2.1.19; no topocentric lunar parallax.
- Bodies: ten conventional planets/luminaries from Sun through Pluto.
- Angles: horizon/ecliptic and meridian/ecliptic intersections using observer latitude, east-positive longitude, and Greenwich apparent sidereal time from the pinned engine.
- Houses: whole-sign default; equal house optional. Both are explicit and never silently mixed.
- Aspects: conjunction/opposition 8°, trine/square 7°, sextile 5°; each pair receives at most the closest qualifying major aspect.
- Interpretation: project-authored symbolic labels only, no deterministic event prediction.
- Timing: transit-to-natal major aspects and solved geocentric tropical solar returns; no
  progressions or directions.
- Synastry: symmetric cross-chart aspects remain separate from directional house overlays.
- Rectification: dated training and holdout events are mandatory and unresolved evidence returns
  `underdetermined`.
- Horary astrology is not part of either production lineage. It requires a separate question-time
  contract, house system, dignity tables, significator rules, and expert-reviewed Golden Cases
  before a Skill can be exposed.

## Manifest quality note

Transparent product policy pending practitioner production review.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `deb34ed7490114d40e4c8bcd44d929b7913b7a0520d08c51e7d02a7f6bc575ca`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
