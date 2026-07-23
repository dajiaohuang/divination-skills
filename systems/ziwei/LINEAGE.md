# Ziwei lineage

`project-native-ziwei-foundation-v0.1` is an independently implemented structural baseline. It uses
the local civil solar date, lunar-python only for Gregorian/lunar calendrical conversion, the
project's explicit double-hour table, 五虎遁 palace stems, 纳音-derived 五行局, 紫微/天府 star groups,
four time/month minor stars, year-stem 四化, and explicit decade direction.

Local hours map to 13 indices: early 子 at hour 0, twelve two-hour blocks, and late 子 at hour 23.
The caller supplies `calculation_gender` only as an algorithm parameter affecting decade direction.
It is not inferred and must not be described as identity.

The implementation is intentionally versioned as a foundation rather than a universal Ziwei
standard. iztro 2.5.8 is reference-only and cannot define or execute the production lineage.
