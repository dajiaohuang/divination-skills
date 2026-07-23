# Input and output contract

Required input:

```json
{
  "local_datetime": "2024-02-04T16:27:08",
  "timezone": "Asia/Shanghai"
}
```

Optional fields are `fold` (`0` or `1`), `day_boundary` (`midnight` or `zi_initial`), `longitude`, `latitude`, `luck_cycle_direction` (`forward` or `reverse`), and `time_basis` (`civil` or `apparent_solar`). The legacy boolean `true_solar_time` is an alias. Apparent solar time requires longitude and accepts solar input only. A UTC offset inside `local_datetime` is invalid because the named IANA zone is required for historical transition auditing.

The JSON output separates `raw_input`, `normalized_input`, `computed_facts`, empty `derived_findings`, empty `narrative`, and `validation`. Preserve the civil and calculation datetimes, solar-time correction details, `fact_id`, `source_ids`, boundary timestamps, engine version, and warnings.

Fail on unknown zones, nonexistent local times, unresolved ambiguous times, dates outside 1900–2100, apparent-solar requests without longitude, and conflicting time-basis fields.
