---
source_id: "SRC-TIME-TZDATA-001"
title: "Python tzdata 2026.3"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/bazi/sources/SRC-TIME-TZDATA-001.json"
capture_mode: "full"
aggregate_payload_sha256: "cbb36147d3d35533588df590b0df12abd6c57d6fef07c627a3ecf50c517aa6df"
license: "Apache-2.0"
---

# Python tzdata 2026.3

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-TIME-TZDATA-001`
- Manifest: `systems/bazi/sources/SRC-TIME-TZDATA-001.json`
- Type: `dataset`
- Language: `en`
- Edition/version: `2026.3`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `bazi`, `vedic-astrology`, `western-astrology`
- Lineages: `time-normalization`, `true-citra-common-v0.1`, `tropical-geocentric-v0.1`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Verified PyPI metadata identifies Apache-2.0 and records a trusted-publishing source commit.

## Locator capture ledger

### Locator 1

- Registered: https://pypi.org/project/tzdata/2026.3/
- Resolved: https://pypi.org/pypi/tzdata/2026.3/json
- Status: `captured`
- Media type: `application/json`
- SHA-256: `803cc078e95743a65df3400feac314ee93a4c5bf9fbb1acf62938d50fe88660e`
- Note: Retrieved through the PyPI JSON API: https://pypi.org/pypi/tzdata/2026.3/json

#### Parsed material

# tzdata 2026.3

Provider of IANA time zone data

## Package metadata

- License: Apache-2.0
- Python requirement: >=2
- Project URL: https://pypi.org/project/tzdata/
- Package URL: https://pypi.org/project/tzdata/

## Declared dependencies


## Published description

tzdata: Python package providing IANA time zone data
====================================================

This is a Python package containing ``zic``-compiled binaries for the IANA time
zone database. It is intended to be a fallback for systems that do not have
system time zone data installed (or don't have it installed in a standard
location), as a part of `PEP 615 <https://www.python.org/dev/peps/pep-0615/>`_.

This repository generates a ``pip``-installable package, published on PyPI as
`tzdata <https://pypi.org/project/tzdata>`_.

For more information, see `the documentation <https://tzdata.python.org>`_.

### Locator 2

- Registered: https://github.com/python/tzdata/tree/2026.3
- Resolved: https://api.github.com/repos/python/tzdata
- Status: `captured`
- Media type: `application/json; charset=utf-8`
- SHA-256: `ff32db1888d5b73baa7324a3cb811295491ec0731a25728e36a8b52d9d877301`
- Note: Retrieved repository metadata through the GitHub API: https://api.github.com/repos/python/tzdata; README capture failed: HTTP Error 404: Not Found

#### Parsed material

# python/tzdata

Python package wrapping the IANA time zone database

## Repository metadata

- Default branch: `master`
- License: `NOASSERTION`
- Archived: `False`
- Created: `2020-02-21T14:32:53Z`
- Updated: `2026-07-16T10:55:30Z`
- Repository: https://github.com/python/tzdata

## Manifest quality note

Pinned cross-platform IANA time-zone data fallback.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `cbb36147d3d35533588df590b0df12abd6c57d6fef07c627a3ecf50c517aa6df`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
