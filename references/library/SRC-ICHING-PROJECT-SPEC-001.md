---
source_id: "SRC-ICHING-PROJECT-SPEC-001"
title: "Project three-coin, King Wen, and moving-policy specification v0.3"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/iching/sources/SRC-ICHING-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "134ec792c23bf3d6acdb27c2f2963639a326fa0953919e8ff3ebc32923241e44"
license: "Apache-2.0"
---

# Project three-coin, King Wen, and moving-policy specification v0.3

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-ICHING-PROJECT-SPEC-001`
- Manifest: `systems/iching/sources/SRC-ICHING-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `0.3.0`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `iching`
- Lineages: `three-coin-king-wen-structural-v0.3`, `king-wen-classical-source-layer-v0.2`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Conventional identifiers and calculation structure only; project-authored prompts; no copied translation or commentary.

## Locator capture ledger

### Locator 1

- Registered: systems/iching/LINEAGE.md
- Resolved: systems/iching/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `f9428b5f1bbb63147a592780350bd88ae3277c4c4f2ee89b2b90fe84dfe4ec64`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# I Ching lineage

`three-coin-king-wen-structural-v0.3` uses six fair three-coin lines, numbered from the bottom. Coin values are 2 or 3, so totals are 6 through 9. Six and nine move; the changed line flips polarity. Primary and changed line patterns are mapped to the conventional eight trigrams and King Wen sequence.

The production layer contains conventional identifiers plus project-authored structural prompts. It intentionally excludes copied translations of the judgments, images, and line texts. Interpretation beyond the computed structure remains pending domain review.
`king-wen-classical-source-layer-v0.3` registers edition-level provenance and semantic passage
locators without copying classical text. `all-moving-lines-v0.2` exposes every moving line.
`zhu-xi-count-routing-v0.3` is the isolated count-based selection policy documented in
Hu Fangping's public-domain *Yixue Qimeng Tongshi*, including separate routing for zero through
six changing lines. A caller must always state the policy ID; the two outputs are never silently
merged.

`ICHING-CANONICAL-IDENTITY-001` keeps structural identifiers independent from edition wording. The engine returns source locators but never silently chooses or reconstructs a translation.

## Manifest quality note

Calculation baseline pending independent practitioner acceptance.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `134ec792c23bf3d6acdb27c2f2963639a326fa0953919e8ff3ebc32923241e44`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
