---
source_id: "SRC-LIUYAO-PROJECT-SPEC-001"
title: "Project Wen Wang Najia structural and judgment specification v0.3"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/liuyao/sources/SRC-LIUYAO-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "f65c54601ed56e6af6dc17e5bf55f473447b11d5af2d403c63cd6c5e273efc93"
license: "Apache-2.0"
---

# Project Wen Wang Najia structural and judgment specification v0.3

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-LIUYAO-PROJECT-SPEC-001`
- Manifest: `systems/liuyao/sources/SRC-LIUYAO-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `zh-Hans`
- Edition/version: `0.3.0`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `liuyao`
- Lineages: `wen-wang-najia-structural-v0.3`, `wen-wang-najia-project-judgment-v0.2`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Project-authored table transcription and structural wording; no copied modern commentary.

## Locator capture ledger

### Locator 1

- Registered: systems/liuyao/LINEAGE.md
- Resolved: systems/liuyao/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `389dd2ba977739f529d477eebb5d15f9f82d21b77c84414a42ae427a79b9e609`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Liuyao lineage

`wen-wang-najia-structural-v0.3` uses the `three-coin-king-wen-structural-v0.3` casting contract, the eight-palace sequences, traditional inner/outer trigram 纳甲 tables, palace-element 六亲 derivation, and day-stem 六神 rotation.

The civil timestamp is normalized through the Bazi calculation layer. The caller must state an IANA time zone and may choose `midnight` or `zi_initial` as the day boundary; the selection is retained. This baseline is a transparent engineering transcription pending independent domain acceptance, not a claim that all Liuyao schools agree.

v0.3 cites 《增删卜易》 for the selected structural vocabulary and formulas. The project tables remain separately cited because a historical source does not by itself prove every transcription choice.

`wen-wang-najia-project-judgment-v0.2` is a physically separate and opt-in project
judgment lineage. It routes an explicit question category to 世、应 or one 六亲, exposes a
transparent month/day/void/moving structural score, calculates moving-line 纳甲 relations, and
optionally lists branch-level timing candidates. It never converts those candidates into an
outcome or event date. The rule pack remains pending independent practitioner review.

## Manifest quality note

Engineering baseline pending independent Liuyao practitioner acceptance.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `f65c54601ed56e6af6dc17e5bf55f473447b11d5af2d403c63cd6c5e273efc93`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
