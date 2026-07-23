# Ziwei data contract v0.1

Input requires offset-free `local_datetime`, IANA `timezone`, and explicit `calculation_gender`
(`male` or `female`); optional DST `fold` resolves ambiguous civil times. Supported years are
1900–2099. `calculation_gender` is an algorithm parameter and is never inferred as identity.

Output records local/UTC time, fold, time index, lunar and sexagenary date facts, zodiac/sign labels,
命宫/身宫 branches, 命主/身主, 五行局, and twelve palaces. Every palace and star carries a stable fact
ID and production source ID. Major and minor star placement, 四化 labels, and decade ranges are
project-native deterministic calculations.

The report is structural only. It must not interpret stars, decades, traits, relationships, or
events. iztro output may be compared during review but must never enter the runtime result.
