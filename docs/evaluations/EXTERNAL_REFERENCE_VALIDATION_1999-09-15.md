# External reference validation: 1999-09-15

Date: 2026-07-23

## Status and evidence boundary

This comparison uses two user-supplied exports:

- 文墨天机紫微斗数命盘, API 1.1.5, App 2.5.20, placement code `C5VUC`;
- a Bazi Skill output whose provider and version were not reported.

The exports are non-authoritative regression references. They do not become production sources,
prove predictive validity, or create a runtime dependency on either provider. Only calculation
facts represented by the project contract are compared.

## Ziwei result

The reference agrees with the project on:

- lunar date, 戌 time block, 火六局, 命宫亥, 身宫未, 命主巨门, 身主天同, and 迁移来因宫;
- all twelve palace names and stems, allowing the display alias `交友` → `仆役`;
- all fourteen major-star placements and all four minor-star placements;
- the selected bounded auxiliary stars present in both outputs;
- all twelve decadal ranges and the first five listed minor-limit ages in every palace;
- the 己-year birth transformations 武曲禄、贪狼权、天梁科、文曲忌.
- every reported 庙旺得利平不陷 value covered by the selected classical matrix;
- all nine reported ↓离心/↑向心 self-transformations;
- the reported civil `19:05` to apparent-solar `19:09` minute using longitude `119.917`.

The comparison exposed and corrected three project defects:

1. 天府 used a 子-based offset in an 寅-based palace index, shifting the entire 天府 group.
2. 月德 incorrectly started from 子 instead of 巳.
3. The year-based 年解 placement was labeled 解神, while the month-based 解神 was absent.

The project additionally emits 天府↑科 because the selected 《紫微斗数全书》卷二 table gives 壬干
天府化科. The reference application does not mark it, so this is retained as an explicit
four-transformation lineage difference. Annual limits and uncatalogued small stars remain outside
the comparison.

## Bazi result

The reference agrees with the project on:

- the four pillars 己卯、癸酉、庚午、丙戌;
- 庚 day master, visible Ten Gods, and each branch's primary hidden-stem Ten God;
- all four 纳音, day-master and pillar-self 十二长生, 旺相休囚死, and visible five-element counts;
- 卯酉冲、卯午破、卯戌合、酉戌害、午戌半合;
- the forward luck-cycle sequence. The project emits the first eight cycles and they match the
  first eight of the ten displayed by the reference.

The comparison added the previously omitted `break` and `half_harmony` structural relation types.
The project records 卯戌 as a combination but does not infer “transformation to fire” from the pair
alone.

The project reports a precise method-specific start age of `7.758646` years. This falls in calendar
year 2007 and is compatible with the reference's rounded “2007, nominal age 9” display. It is not
treated as an identical age-format convention.

The Bazi export labels its input as true solar time. The project now independently converts the
reported civil `19:05` clock at longitude `119.917` to `19:09:25` with the NOAA fractional-year
approximation. It also replays the reported corrected `19:11` input directly. Both remain in the
same 戌 block and produce the same four pillars.

## Regression artifacts

- `systems/ziwei/tests/external_references/CASE-ZIWEI-WENMO-001.json`
- `systems/ziwei/tests/test_external_reference.py`
- `systems/bazi/tests/external_references/CASE-BAZI-USER-001.json`
- `systems/bazi/tests/test_external_reference.py`

The project-native Ziwei Golden Cases were deterministically regenerated after the formula repair.
They remain synthetic project regressions, separate from this external comparison.

The implementation-source review is recorded in
`docs/research/AUTHORITATIVE_SOURCES_ZIWEI_BAZI.md`.
