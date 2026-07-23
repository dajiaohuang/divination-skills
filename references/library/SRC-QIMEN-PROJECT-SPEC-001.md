---
source_id: "SRC-QIMEN-PROJECT-SPEC-001"
title: "Project Shijia Zhuanpan Chaibu full-chart specification v0.3"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/qimen/sources/SRC-QIMEN-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "8e9553eeb167d29ab493e47a3a618d92ed98182d4eadf05c7538f80dd371aaaf"
license: "Apache-2.0"
---

# Project Shijia Zhuanpan Chaibu full-chart specification v0.3

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-QIMEN-PROJECT-SPEC-001`
- Manifest: `systems/qimen/sources/SRC-QIMEN-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `zh-Hans`
- Edition/version: `0.3.0`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `qimen`
- Lineages: `shijia-zhuanpan-chaibu-v0.3`, `shijia-zhuanpan-chaibu-full-v0.3`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Project-authored calculation transcription and safety wording; no copied commentary.

## Locator capture ledger

### Locator 1

- Registered: systems/qimen/LINEAGE.md
- Resolved: systems/qimen/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `3b621caa93492e286d729b3db48c2263b86af7c3661286822ad368f407a52d3b`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Qimen lineage

`shijia-zhuanpan-chaibu-v0.3` fixes the method to time-based Shijia Qimen, rotating-plate terminology, and the Chaibu three-yuan ju table. Solar terms are evaluated as instants using the project's pinned calendar dependency and compared in China Standard Time. The caller's selected civil or apparent-solar calculation time is normalized from an IANA zone.

Yang dun runs the nine earth-plate stems forward from the ju palace; yin dun runs them backward. The order is 戊己庚辛壬癸丁丙乙. The hour's sexagenary xun identifies the hidden Jia instrument and its original duty-star and duty-door palace. This engineering transcription remains pending independent practitioner acceptance.

`shijia-zhuanpan-chaibu-full-v0.3` extends that immutable foundation with an eight-palace rotation
ring for stars, doors, and spirits plus a nine-palace Lo Shu walk for locating the duty door.
A logical duty-door landing in palace 5 is disclosed and hosted in Kun 2 for the rotating
eight-door plate. The layer includes heaven stems, nine stars, eight doors, eight spirits, hour
void, the selected classical three-Qi tomb markers (乙 in 2; 丙/丁 in 6), six-instrument
punishments, and palace-controls-door oppression facts. These are calculation facts only. No
用神、方位、吉凶、事件 or 应期 judgment is part of the lineage.

## Manifest quality note

Foundation tables pending independent practitioner acceptance.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `8e9553eeb167d29ab493e47a3a618d92ed98182d4eadf05c7538f80dd371aaaf`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
