# Ziwei lineage

`project-native-ziwei-structural-v0.4` is an independently implemented structural baseline. It uses
lunar-python only for Gregorian/lunar calendrical facts, while project code owns all palace, star,
cycle, limit, query, and dynamic-layer algorithms. The primary formula reference is the
public-domain historical 《紫微斗數全書》; project-authored tables record formula facts, not copied
interpretive prose.

Local hours map to 13 indices: early 子 at hour 0, eleven two-hour blocks, and late 子 at hour 23.
The caller explicitly selects lunar-new-year or spring-commences year boundary, current-day or
next-day late-Zi basis, and preserved or split-after-fifteenth leap-month policy. The caller supplies
`calculation_gender` only as an algorithm parameter affecting direction. It is not inferred or
described as identity.

Dynamic rotations are a named project-native structural policy, not a universal Ziwei standard.
Brightness remains unavailable. iztro 2.5.8 is reference-only and cannot define, execute, test, or
ship the production lineage.

A user-supplied 文墨天机 API 1.1.5 / App 2.5.20 export is retained as a non-authoritative regression
reference. It independently exposed the 天府 coordinate error and corroborates the repaired
fourteen-major-star layout for one chart. One external chart is not practitioner acceptance or
broad cross-lineage validation.
