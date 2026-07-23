# Bazi v0.1 traceability example

This is a calculation and evidence-chain example, not an expert life reading.

## Calculation basis

- Local input: `1986-05-29T19:30:00 Asia/Shanghai`.
- Historical UTC offset: `+09:00` because the IANA record includes the 1986 DST period.
- Solar-term provider frame: fixed `UTC+08:00`; it is not shifted by historical Shanghai DST.
- Day boundary: `midnight`.
- True solar time: not applied; coordinates are retained as metadata.
- Luck-cycle direction: explicitly `forward`.

## Verified facts

| Fact ID | Value | Governing rule | Explanation |
|---|---|---|---|
| `bazi.pillar.year` | 丙寅 | `BAZI-CAL-YEAR-001` | The instant is after 1986 立春. |
| `bazi.pillar.month` | 癸巳 | `BAZI-CAL-MONTH-001` | The instant lies between 立夏 and 芒种. |
| `bazi.pillar.day` | 癸酉 | `BAZI-CAL-DAY-001` | The default policy changes the day at midnight. |
| `bazi.pillar.hour` | 壬戌 | `BAZI-CAL-HOUR-001` | 19:30 local civil time is in the 戌 double-hour. |
| `bazi.day_master` | 癸, yin water | `BAZI-FACT-DAYMASTER-001` | This is the visible stem of the day pillar. |
| `bazi.ten_gods` | year 正财; month 比肩; day 比肩; hour 劫财 | `BAZI-FACT-TENGOD-001` | These are relational labels computed against 癸; no personality or event claim is added. |
| `bazi.branch_relation.001` | 寅–巳 harm | `BAZI-FACT-BRANCH-REL-001` | The relation connects the year and month branches. |
| `bazi.branch_relation.002` | 酉–戌 harm | `BAZI-FACT-BRANCH-REL-001` | The relation connects the day and hour branches. |

## Method-specific timing data

Under `BAZI-LUCK-START-001`, the adjacent 芒种 interval produces a decimal start age of approximately `2.517218` years. The first three forward sequence pillars are 甲午, 乙未, and 丙申. This is calculated sequence data, not a prediction that an event will occur at those ages.

## Limits

The default report does not infer strength. If the caller explicitly selects `project-seasonal-support-v0.1`, this example receives score `2` and rule `BAZI-STRENGTH-DRAIN-001` labels only the disclosed feature vector as `drain_control_dominant` with low confidence. It is not an expert-approved canonical strength judgment and cannot support structure, transformation, climate adjustment, useful-god, career, health, relationship, or event conclusions.
