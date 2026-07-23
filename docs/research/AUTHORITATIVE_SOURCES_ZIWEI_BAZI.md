# Authoritative implementation sources: Ziwei and Bazi

Date reviewed: 2026-07-23

## Selection standard

Production calculation rules must be supported by an official technical publication, a
public-domain primary historical text, or a project specification that clearly labels a modern
product convention. User exports and reference repositories are regression evidence only.

## Apparent solar time

Selected source:

- NOAA Global Monitoring Laboratory, [General Solar Position Calculations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF).
- NOAA, [Solar Calculation Details](https://gml.noaa.gov/grad/solcalc/calcdetails.html).
- NOAA, [Copyright and Usage](https://sos.noaa.gov/copyright/).

Implemented equations:

```text
fractional_year = 2π / days_in_year × (day_of_year - 1 + (hour - 12) / 24)
equation_of_time = NOAA fractional-year series
time_offset = equation_of_time + 4 × longitude_east - 60 × UTC_offset_hours
apparent_solar_clock = civil_clock + time_offset
```

The conversion produces a calculation clock. It does not change the recorded physical UTC instant
or the absolute solar-term boundaries. Civil time remains the default; apparent solar time must be
explicitly selected and requires longitude.

The NREL Solar Position Algorithm was reviewed as a higher-precision alternative but is not used in
this release. The compact NOAA method is sufficient for a disclosed approximate calculation clock
and is directly reproducible without a new runtime dependency.

## Bazi calculation facts

Selected primary text:

- 《三命通会》卷一, [六十甲子纳音](https://zh.wikisource.org/zh-hans/%E4%B8%89%E5%91%BD%E9%80%9A%E6%9C%83/%E5%8D%B7%E4%B8%80).
- 《三命通会》卷二, [论天干阴阳生死](https://zh.wikisource.org/zh-hans/%E4%B8%89%E5%91%BD%E9%80%9A%E6%9C%83/%E5%8D%B7%E4%BA%8C).

Implemented facts:

- all 30 纳音 labels across the sixty Jiazi pairs;
- ten-stem 十二长生 direction and starting branch;
- seasonal 五行旺相休囚死;
- visible five-element counts across the eight visible stem/branch characters, explicitly excluding
  hidden stems.

These facts do not decide canonical strength, 格局, 从格, 调候, or useful gods. Those judgments remain
outside the default calculation layer because major lineages differ on precedence and exceptions.

## Ziwei calculation facts

Selected primary text:

- 《紫微斗数全书》卷二, [Wikisource transcription](https://zh.wikisource.org/zh-hant/%E7%B4%AB%E5%BE%AE%E6%96%97%E6%95%B8%E5%85%A8%E6%9B%B8/%E5%8D%B7%E4%BA%8C).

Implemented facts:

- the complete twelve-branch 庙旺得利平不陷 matrix for the 21 tabulated stars;
- the ten-stem four-transformation table;
- bounded null output for stars or placements not present in that matrix.

The selected table gives 壬干 as 天梁化禄、紫微化权、天府化科、武曲化忌. This differs from the supplied
文墨天机 chart, which does not mark the resulting 天府向心化科. The project retains the classical
mapping and records the mismatch as a lineage difference.

## Modern self-transformation direction policy

The historical source supports the stem-to-star four-transformation table but does not define the
modern ↓/↑ symbols. The project therefore labels:

- target palace's own stem → `outward`, `↓`, 离心自化;
- opposite palace's stem → `inward`, `↑`, 向心自化.

Every result retains origin palace, origin stem, target palace, target star, and transformation.
Consumers can ignore the modern labels without losing the underlying path facts. The convention is
registered in `DSP-ZIWEI-SELF-TRANSFORMATION-001`.

## Evidence and rights boundary

The historical originals are public domain. Wikisource transcriptions are used to verify formulas
and uncopyrightable tables; the project does not redistribute the transcription prose. NOAA
government material is used under its stated public-domain policy with attribution and no implied
endorsement.

The 文墨天机 export and the ignored iztro clone are not production sources, runtime dependencies, or
definitions of the project lineage.
