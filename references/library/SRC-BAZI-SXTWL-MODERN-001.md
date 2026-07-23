---
source_id: "SRC-BAZI-SXTWL-MODERN-001"
title: "sxtwl-modern 1.1.2"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/bazi/sources/SRC-BAZI-SXTWL-MODERN-001.json"
capture_mode: "metadata_only"
aggregate_payload_sha256: "b07fd466e445bd55df160c5016b4b25dda6c2869a1b377a773c74b2e4396c949"
license: "LicenseRef-PyPI-BSD-Metadata"
---

# sxtwl-modern 1.1.2

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-BAZI-SXTWL-MODERN-001`
- Manifest: `systems/bazi/sources/SRC-BAZI-SXTWL-MODERN-001.json`
- Type: `software`
- Language: `zh`
- Edition/version: `1.1.2`
- Retrieved: `2026-07-23`
- Usage status: `reference_only`
- Systems: `bazi`
- Lineages: `sxtwl-day-level-comparator`

## Rights envelope

- License: `LicenseRef-PyPI-BSD-Metadata`
- Rights review: `reference_only`
- Derivative use: `unknown`
- Dataset use: `unknown`
- Evidence: PyPI metadata identifies BSD; repository page and source distribution require a separate complete-license review.

## Locator capture ledger

### Locator 1

- Registered: https://github.com/SIC98/sxtwl
- Resolved: https://api.github.com/repos/SIC98/sxtwl
- Status: `metadata_only`
- Media type: `application/json; charset=utf-8`
- SHA-256: `74a417875e9767df805e7cbb7420a9cdbcab4fd59d23563b8ca0a72426c4e0c5`
- Note: Retrieved repository metadata through the GitHub API: https://api.github.com/repos/SIC98/sxtwl

#### Parsed material

# SIC98/sxtwl



## Repository metadata

- Default branch: `master`
- License: `None`
- Archived: `False`
- Created: `2025-11-15T05:54:16Z`
- Updated: `2025-11-15T10:46:20Z`
- Repository: https://github.com/SIC98/sxtwl

### Locator 2

- Registered: https://pypi.org/project/sxtwl-modern/1.1.2/
- Resolved: https://pypi.org/pypi/sxtwl-modern/1.1.2/json
- Status: `metadata_only`
- Media type: `application/json`
- SHA-256: `0a2fb0a5879b0a677995830ca479e74074a6bacb434abd09a00911b85334b9ae`
- Note: Retrieved through the PyPI JSON API: https://pypi.org/pypi/sxtwl-modern/1.1.2/json

#### Parsed material

# sxtwl-modern 1.1.2

Sxtwl_cpp wrapper for Python - Chinese Lunar Calendar Library

## Package metadata

- License: BSD
- Python requirement: >=3.8
- Project URL: https://pypi.org/project/sxtwl-modern/
- Package URL: https://pypi.org/project/sxtwl-modern/

## Declared dependencies

## Manifest quality note

Independent C++ astronomy/calendar implementation. Its exposed day API changes year/month pillars by calendar date, so exact solar-term instants are excluded from strict comparison.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `b07fd466e445bd55df160c5016b4b25dda6c2869a1b377a773c74b2e4396c949`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
