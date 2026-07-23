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
