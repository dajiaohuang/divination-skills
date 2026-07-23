# Bazi data contract v0.2

## Input

```json
{
  "local_datetime": "2024-02-04T16:27:08",
  "timezone": "Asia/Shanghai",
  "fold": 0,
  "day_boundary": "midnight",
  "time_basis": "apparent_solar",
  "longitude": 121.4737,
  "latitude": 31.2304,
  "luck_cycle_direction": "forward"
}
```

Required fields are `local_datetime` and `timezone`. The datetime must not include an offset because the named time zone is the auditable source of historical offset rules. `fold` is required only when the local time occurs twice during a backward clock transition.

`day_boundary` defaults to `midnight`; `time_basis` defaults to `civil`. `luck_cycle_direction`, coordinates, and `fold` are optional. `apparent_solar` requires longitude and uses the NOAA approximation to produce a separate calculation clock. The civil UTC instant is never replaced.

## Output layers

```text
raw_input
normalized_input
computed_facts
derived_findings
narrative
validation
```

The calculator emits the first three layers plus validation. Rule evaluation adds `derived_findings`; only a reporting Skill may add `narrative`.

Every pillar and relation includes a stable `fact_id`. Every rule-derived finding must record the fact IDs and rule ID it used. Narrative must not mutate calculator output.

## Failure behavior

- Unknown time zone: fail.
- Nonexistent local time during a forward clock transition: fail.
- Ambiguous local time without `fold`: fail.
- Date outside supported range: fail.
- Apparent solar time without longitude or with lunar input: fail.
- Conflicting `time_basis` and legacy `true_solar_time`: fail.
- Missing luck-cycle direction: return the chart without luck cycles and add a warning.
