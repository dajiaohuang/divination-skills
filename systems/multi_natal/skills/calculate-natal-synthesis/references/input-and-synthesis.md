# Input and synthesis contract

## Minimum JSON

```json
{
  "birth_date": "1999-09-15",
  "birth_time": "19:05",
  "birthplace": {
    "name": "Nanjing, Jiangsu, China",
    "timezone": "Asia/Shanghai",
    "longitude": 118.7969,
    "latitude": 32.0603,
    "resolution_source": "user_confirmed"
  },
  "calculation_gender": "female"
}
```

Use east-positive longitude and north-positive latitude. Add `fold: 0|1` only
for a repeated DST clock time.

## Optional policy object

```json
{
  "policies": {
    "east_asian_time_basis": "civil",
    "bazi_day_boundary": "midnight",
    "bazi_luck_cycle_direction": null,
    "western_house_system": "whole_sign",
    "ziwei_year_boundary": "lunar_new_year",
    "ziwei_late_zi_policy": "current_day",
    "ziwei_leap_month_policy": "preserve",
    "vedic_lineages": ["parashari", "jaimini", "kp"],
    "jaimini_karaka_policy": "seven"
  }
}
```

Do not infer Bazi luck direction from gender without naming and selecting the
specific lineage policy.

## Optional numerology

```json
{
  "numerology": {
    "name": "Alex Example",
    "mappings": ["pythagorean", "chaldean"]
  }
}
```

For a non-Latin name, include the user's own `transliteration`.

## Meaning of “synthesis”

The output groups source facts under core-identity, inner-reflection, vocation,
relationships, and resources axes. These axes are report navigation only.
Concepts grouped on one axis remain method-specific and must not be counted as
independent confirmations of a prediction.
