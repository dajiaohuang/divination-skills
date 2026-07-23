# Ziwei lineage

`project-native-ziwei-structural-v0.5` is an independently implemented structural baseline. It uses
lunar-python only for Gregorian/lunar calendrical facts, while project code owns all palace, star,
cycle, limit, query, and dynamic-layer algorithms. The primary formula reference is the
public-domain historical 《紫微斗數全書》; project-authored tables record formula facts, not copied
interpretive prose.

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
