# Vedic Astrology data contract

## Input

```json
{
  "local_datetime": "1999-09-15T19:05:00",
  "timezone": "Asia/Shanghai",
  "longitude": 119.917,
  "latitude": 31.30,
  "fold": 0,
  "lineages": ["parashari", "jaimini", "kp"],
  "jaimini_karaka_policy": "seven",
  "ayanamsha": "true_citra"
}
```

Required fields are `local_datetime`, `timezone`, `longitude`, and `latitude`.
`lineages` defaults to all three supported modules. `fold` is required only for
an ambiguous civil time. Unknown fields and nonexistent local times fail
closed.

The only accepted ayanāṃśa in v0.1 is `true_citra`. The only accepted Jaimini
kāraka policies are `seven` and `eight`.

## Output layers

The calculator returns:

1. `raw_input`;
2. `normalized_input`, including the selected policies and exact UTC instant;
3. `computed_facts.astronomy`, with tropical positions and the calculated
   ayanāṃśa;
4. `computed_facts.sidereal_chart`, with grahas, mean nodes, lagna, nakṣatra,
   pāda, and whole-sign house;
5. only the requested lineage modules under
   `computed_facts.lineages.parashari|jaimini|kp`;
6. `warnings`, `rule_ids`, `source_ids`, and `trace`.

Every substantive nested fact carries its own `rule_ids` and `source_ids`.
No natural-language prediction is emitted by the calculator.

## Numerical policies

- Supported civil years: 1900 through 2100.
- Longitudes are normalized to `[0, 360)`.
- Boundary selection uses half-open intervals.
- Stored display longitudes are rounded to eight decimal places; branch
  decisions use unrounded values.
- Vimśottarī schedule timestamps use a proleptic Gregorian duration of
  `365.2425` days per computational year.
- Exact Jaimini degree ties fail with `karaka_tie`.

## Failure codes

The public calculator may return:

- `unknown_fields`
- `missing_<field>`
- `invalid_longitude`
- `invalid_latitude`
- `invalid_lineages`
- `invalid_ayanamsha`
- `invalid_karaka_policy`
- `ambiguous_local_time`
- `nonexistent_local_time`
- `date_out_of_range`
- `karaka_tie`
- `angle_undefined`
