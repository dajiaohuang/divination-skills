---
source_id: "SRC-BAZI-PROJECT-SPEC-001"
title: "Project-authored Bazi extension contracts v0.2"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/bazi/sources/SRC-BAZI-PROJECT-SPEC-001.json"
capture_mode: "full"
aggregate_payload_sha256: "49d5cefdd6a921fc9835ee30092bbd8aa101c6c59ee779b25638fee947e44f46"
license: "Apache-2.0"
---

# Project-authored Bazi extension contracts v0.2

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-BAZI-PROJECT-SPEC-001`
- Manifest: `systems/bazi/sources/SRC-BAZI-PROJECT-SPEC-001.json`
- Type: `standard`
- Language: `en`
- Edition/version: `0.2.0`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `bazi`
- Lineages: `ziping-calculation-baseline`

## Rights envelope

- License: `Apache-2.0`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Project-authored contracts are released under the repository Apache-2.0 license.

## Locator capture ledger

### Locator 1

- Registered: systems/bazi/DATA_CONTRACT.md
- Resolved: systems/bazi/DATA_CONTRACT.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `ee14addea4877014af5573ac694dafd18f7543bbaead7c9c8f10049b07eb50c5`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Bazi data contract v0.2

## Input

```json
{
  "local_datetime": "2024-02-04T16:27:08",
  "timezone": "Asia/Shanghai",
  "fold": 0,
  "day_boundary": "midnight",
  "time_basis": "apparent_solar",
  "longitude": 121.4737,
  "latitude": 31.2304,
  "luck_cycle_direction": "forward"
}
```

Required fields are `local_datetime` and `timezone`. The datetime must not include an offset because the named time zone is the auditable source of historical offset rules. `fold` is required only when the local time occurs twice during a backward clock transition.

`day_boundary` defaults to `midnight`; `time_basis` defaults to `civil`. `luck_cycle_direction`, coordinates, and `fold` are optional. `apparent_solar` requires longitude and uses the NOAA approximation to produce a separate calculation clock. The civil UTC instant is never replaced.

## Output layers

```text
raw_input
normalized_input
computed_facts
derived_findings
narrative
validation
```

The calculator emits the first three layers plus validation. Rule evaluation adds `derived_findings`; only a reporting Skill may add `narrative`.

Every pillar and relation includes a stable `fact_id`. Every rule-derived finding must record the fact IDs and rule ID it used. Narrative must not mutate calculator output.

## Failure behavior

- Unknown time zone: fail.
- Nonexistent local time during a forward clock transition: fail.
- Ambiguous local time without `fold`: fail.
- Date outside supported range: fail.
- Apparent solar time without longitude or with lunar input: fail.
- Conflicting `time_basis` and legacy `true_solar_time`: fail.
- Missing luck-cycle direction: return the chart without luck cycles and add a warning.

### Locator 2

- Registered: systems/bazi/LINEAGE.md
- Resolved: systems/bazi/LINEAGE.md
- Status: `captured`
- Media type: `text/markdown`
- SHA-256: `fd1f797b5407b215bce8a75bf4f33db161d4a90900a8fba8e85b0c3448104517`
- Note: Copied from the repository-local authoritative contract.

#### Parsed material

# Bazi lineage and calculation decisions

## Baseline

The initial product baseline is a narrow Ziping-style calculation layer. It does not claim to represent every Ziping lineage. A separate, project-authored seasonal-support path exists only as an explicit engineering baseline; it is never mixed into the default calculation lineage.

## Frozen v0.2 decisions

| Topic | Decision |
|---|---|
| Calendar input | Proleptic Gregorian within 1900–2100 |
| Time zone | Required IANA identifier; use `zoneinfo` plus pinned `tzdata` |
| Year boundary | Exact instant of Spring Commences / 立春 |
| Month boundary | Exact instant of the 12 minor solar terms / 节 |
| Solar-term frame | The term is an absolute instant; `lunar_python` term timestamps are interpreted in their fixed UTC+08:00 reference frame and converted to UTC, avoiding accidental historical DST shifts |
| Day boundary | Default `midnight`; optional `zi_initial` advances the day pillar at 23:00 |
| Late-Zi hour stem | Derived from the next civil day's day stem for 23:00–23:59 under both day-boundary policies |
| True solar time | Civil time is default; explicit `apparent_solar` plus longitude uses NOAA's published fractional-year approximation to select the calculation date/hour |
| Luck-cycle direction | Must be supplied explicitly as `forward` or `reverse`; never inferred from gender |
| Luck-cycle start | Interval to the adjacent month-boundary term divided by three days per year; output as a decimal age and marked method-specific |
| Strength path | Disabled by default; the only selectable path is the isolated `project-seasonal-support-v0.1` feature contract, marked low-confidence and pending independent expert approval |
| Classical table facts | 纳音, ten-stem 十二长生, and seasonal 旺相休囚死 follow the selected 《三命通会》 transcription; visible counts exclude hidden stems |

## Explicit disputes

- Day changes at midnight versus the beginning of the Zi double-hour.
- Late-Zi day pillar and hour-stem handling.
- Civil time versus mean or apparent solar time.
- Gender/year-polarity direction rules for luck cycles.
- Exact conversion of the adjacent-term interval into start year, month, day, and hour.

Each is represented in `disputes/`; product output must disclose any non-default selection.

## Evidence boundary

Solar-term geometry is checked against the Hong Kong Observatory description that the 24 terms are spaced at 15-degree ecliptic-longitude intervals. Timestamp-aware behavior is compared against `lunar-python`; an independent `sxtwl-modern` implementation agrees on all four pillars for 17 non-boundary-date standard cases. Its day-level API cannot adjudicate the exact instant on a Jie date, so those three exclusions are recorded in `tests/COMPARATOR_REPORT.md`. Classical interpretive claims remain out of scope until accepted sources and expert review are available.

The opt-in seasonal-support path is defined only by `strength/SEASONAL_SUPPORT_SPEC.md`. Its labels must not be presented as canonical Ziping conclusions or used to select useful gods.

A user-supplied external Bazi Skill export additionally corroborates one 1999 chart's four pillars,
Ten Gods, five branch relations, and forward luck-cycle prefix. Its provider and version were not
reported, so it remains a non-authoritative regression reference rather than a production source.

## Manifest quality note

Defines import, comparison, timing, synastry, and rectification data behavior. Domain interpretation acceptance remains pending.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `49d5cefdd6a921fc9835ee30092bbd8aa101c6c59ee779b25638fee947e44f46`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
