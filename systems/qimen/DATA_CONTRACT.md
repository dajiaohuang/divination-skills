# Qimen data contract v0.1

Input requires offset-free `local_datetime` and IANA `timezone`; optional fields are DST fold and `day_boundary`. The timestamp is normalized to local, UTC, and China Standard Time.

Output records the current solar-term instant, yin/yang dun, upper/middle/lower yuan and 符头, Chaibu ju number, day and hour pillars, nine-palace earth plate, hour xun, hidden Jia stem, and original duty-star/door palace. Every earth palace is an immutable fact with source IDs.

The result always emits a `foundation_only` warning. Heaven plate, rotating stars/doors, spirits, center hosting beyond metadata, formations, 用神, directions, events, outcomes, and timing are absent and must not be synthesized.
