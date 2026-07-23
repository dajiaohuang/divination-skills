---
source_id: "SRC-ZIWEI-PROJECT-SPEC-001"
title: "Project-native Zi Wei Dou Shu structural foundation v0.5"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/ziwei/sources/SRC-ZIWEI-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "5ed7b3be0d6fe882c8eacadef7f289a52b2746bcdeb76c033a02e1523d841da9"
license: "Apache-2.0"
---

# Project-native Zi Wei Dou Shu structural foundation v0.5

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-ZIWEI-PROJECT-SPEC-001`
- Manifest: `systems/ziwei/sources/SRC-ZIWEI-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `0.5.0`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `ziwei`
- Lineages: `project-native-ziwei-structural-v0.5`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: The project owner selected Apache-2.0 for project-authored material.

## Locator capture ledger

### Locator 1

- Registered: systems/ziwei/LINEAGE.md
- Resolved: systems/ziwei/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `939dc3955e878bea12a5332e64cf740331c6ef5375178c4b0e3291c1e6027828`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Ziwei lineage

`project-native-ziwei-structural-v0.5` is an independently implemented structural baseline. It uses
lunar-python only for Gregorian/lunar calendrical facts, while project code owns all palace, star,
cycle, limit, query, and dynamic-layer algorithms. The primary formula reference is the
public-domain historical 《紫微斗數全書》; project-authored tables record formula facts, not copied
interpretive prose.

v0.5 also includes the catalogued daily, monthly, and yearly auxiliary placements needed to
reproduce the supplied 文墨天机 chart: 恩光、天贵、孤辰、寡宿、天才、天寿、天厨、蜚廉、
破碎、天官、天福、天空、截空、旬空、阴煞、天月、天巫 and the adjective 大耗. The
formulas are independently encoded; iztro remains a comparison reference only.

The selected calculation clock maps to 13 indices: early 子 at hour 0, eleven two-hour blocks, and
late 子 at hour 23. Civil time is the default; explicit `apparent_solar` plus longitude uses NOAA's
fractional-year equation-of-time approximation while retaining the civil UTC instant.
The caller explicitly selects lunar-new-year or spring-commences year boundary, current-day or
next-day late-Zi basis, and preserved or split-after-fifteenth leap-month policy. The caller supplies
`calculation_gender` only as an algorithm parameter affecting direction. It is not inferred or
described as identity.

Dynamic rotations and ↓ outward / ↑ inward self-transformation direction labels are named
project-native structural policies, not universal Ziwei standards. Birth and palace-stem
star-to-transformation mappings follow the selected 《紫微斗数全书》卷二 table, including
壬干天府化科. Brightness is bounded to the same volume's 21-star matrix; unlisted or structurally
impossible placements remain null. iztro 2.5.8 is reference-only and cannot define, execute, test,
or ship the production lineage.

A user-supplied 文墨天机 API 1.1.5 / App 2.5.20 export is retained as a non-authoritative regression
reference. It independently exposed the 天府 coordinate error and corroborates the repaired
fourteen-major-star layout, every reported brightness value, the reported civil-to-solar minute,
and nine self-transformations for one chart. Its missing 天府↑科 conflicts with the selected
classical 壬干 table and is retained as a declared lineage difference. One external chart is not
practitioner acceptance or broad cross-lineage validation.

### Locator 2

- Registered: systems/ziwei/DATA_CONTRACT.md
- Resolved: systems/ziwei/DATA_CONTRACT.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `42b75cd2d4120e7ae0f4a3a1880a654161367017e8818df9223bb908a4536083`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Ziwei data contract v0.5

Solar input requires offset-free `local_datetime`; lunar input requires `lunar_date`, boolean
`is_leap_month`, and a 0–12 `time_index`. Both require IANA `timezone` and explicit
`calculation_gender`; optional DST `fold` resolves ambiguous civil times. Supported years are
1900–2099. Input records `year_boundary`, `late_zi_policy`, and `leap_month_policy`.
`calculation_gender` is an algorithm parameter and is never inferred as identity.
Solar input may set `time_basis` to `apparent_solar` with longitude; civil time remains the default.
Lunar input cannot request apparent solar time.

Output records civil local/UTC time, calculation clock and correction, fold, policy values, time index, lunar and
sexagenary facts, 命宫/身宫, 命主/身主, 五行局, 来因宫, and twelve palaces. Every palace and star carries
a stable fact ID and production source IDs. Stars expose category, element, polarity, birth
transformation, bounded classical brightness or explicit null, and zero or more self-transformation
paths. Palaces include decade ranges and minor-limit ages.

Timing output keeps natal facts immutable and places major, minor, annual, monthly, daily, and hourly
layers in a separate object. Each transformation path records origin palace/stem and target
star/palace. The shared timeline uses inclusive starts and exclusive ends.

The calculator and timing outputs are structural only. `ziwei-core` is experimental and may explain
only cited structure; it must not assign fixed events, deterministic fortune, identity, diagnosis,
or invented brightness outside the selected matrix. iztro output may be inspected in a developer-only ignored reference but
must never enter runtime results or Golden Cases.

## Manifest quality note

Deterministic project-authored calculation contract; practitioner acceptance remains pending.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `5ed7b3be0d6fe882c8eacadef7f289a52b2746bcdeb76c033a02e1523d841da9`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
