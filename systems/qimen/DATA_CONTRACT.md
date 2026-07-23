# Qimen data contract v0.3

Input requires offset-free `local_datetime` and IANA `timezone`; optional fields are DST fold, `day_boundary`, `time_basis` (`civil` or `apparent_solar`), longitude, and latitude. The timestamp is normalized to calculation time, UTC, and China Standard Time.

Output records the current solar-term instant, yin/yang dun, upper/middle/lower yuan and 符头, Chaibu ju number, day and hour pillars, nine-palace earth plate, hour xun, hidden Jia stem, and original duty-star/door palace. Every earth palace is an immutable fact with source IDs.

v0.3 records `solar_time_correction` and attaches both project and classical source IDs to shared structural facts.

`calculate_full` wraps the immutable foundation and returns a v0.2 nine-palace plate. Every palace
contains earth stem, hosted heaven stems, stars, doors, spirits, branch/void state, tomb entries,
instrument punishments, and door oppression markers. Rotation metadata records the hour
instrument and duty-star/door origins and targets.

The full contract remains calculation-only. It does not select 用神 or infer directions, events,
outcomes, or timing.
