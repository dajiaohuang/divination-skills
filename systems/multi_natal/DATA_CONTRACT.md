# Multi-natal data contract v0.1

## Required input

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

`birthplace.name` is display metadata. The IANA time zone and coordinates are
the calculation inputs. An unresolved or ambiguous place name must not be guessed.
`calculation_gender` is passed only to Ziwei and must be explicitly supplied; it
is not inferred from a name or profile.

## Optional policies

```json
{
  "fold": 0,
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

An optional `numerology` object contains `name`, optional `transliteration`, and
one or both mappings from `pythagorean` and `chaldean`.

## Output

The result follows the repository four-layer report contract:

1. `normalized_input`;
2. immutable native charts and cross-checks under `computed_facts`;
3. evidence-linked `derived_findings`;
4. a bounded `narrative`.

The output never persists the birth profile by itself. Callers must apply the
shared consent and privacy contracts before storage.
