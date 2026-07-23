---
source_id: "SRC-NUMEROLOGY-PROJECT-SPEC-001"
title: "Project Pythagorean and Chaldean numerology contracts v0.3"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/numerology/sources/SRC-NUMEROLOGY-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "d5ca37732840d8cd46a527c3b44e70b37b2104cea493754c0476a460b9d9a115"
license: "Apache-2.0"
---

# Project Pythagorean and Chaldean numerology contracts v0.3

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-NUMEROLOGY-PROJECT-SPEC-001`
- Manifest: `systems/numerology/sources/SRC-NUMEROLOGY-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `0.3.0`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `numerology`
- Lineages: `pythagorean-project-v0.3`, `chaldean-name-cheiro-v0.3`, `numerology-audit-trace-v0.3`, `cross-lineage-input-policy-v0.2`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Original project-authored mapping contract and wording.

## Locator capture ledger

### Locator 1

- Registered: systems/numerology/LINEAGE.md
- Resolved: systems/numerology/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `e84dafe362e620a76d5cce2e73133ca0613d0064fcdeca243a38161ee983b735`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Numerology lineage

`pythagorean-project-v0.3` maps A=1 through I=9 and repeats through Z. Vowels are A, E, I, O, U; Y is a consonant. All digits of the Gregorian birth date are summed before reduction. Repeated digit sums stop at one digit or master number 11, 22, or 33. This choice is explicit because other practitioners reduce components separately or preserve different compounds.

`chaldean-name-cheiro-v0.3` is a separate name mapping sourced to Cheiro: 1=AIJQY, 2=BKR,
3=CGLS, 4=DMT, 5=EHNX, 6=UVW, 7=OZ, and 8=FP; no letter maps to 9. Name-derived and maturity
facts reduce to a single digit and do not preserve Pythagorean master numbers. The independent
project date policy still preserves 11, 22, and 33 for Life Path and Birthday. This transparent
project lineage is not silently blended with the Pythagorean baseline.

`numerology-audit-trace-v0.3` records every normalized character, its vowel/consonant category, assigned value, raw name total, birth-date digits, and raw date total.

Non-Latin alphabetic input requires `user_supplied_latin_transliteration-v0.2`. The software never
infers transliteration. The normalized letters and policy are retained in the output.

## Manifest quality note

Transparent symbolic convention pending practitioner review.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `d5ca37732840d8cd46a527c3b44e70b37b2104cea493754c0476a460b9d9a115`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
