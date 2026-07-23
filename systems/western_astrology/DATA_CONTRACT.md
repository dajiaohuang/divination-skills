# Western astrology data contract v0.3

Input requires offset-free `local_datetime`, IANA `timezone`, longitude, latitude, and optional DST `fold`. `house_system` is `whole_sign` by default or explicit `equal`. The supported civil-year range is 1900–2100.

Output retains local and UTC instants, coordinates, fold, house system, tropical geocentric true-ecliptic-of-date longitudes and speeds for Sun through Pluto, retrograde flags, Ascendant, Midheaven, twelve house cusps, house assignments, and fixed-orb major aspects. Every position, cusp, angle, and aspect is an immutable fact with stable IDs and source IDs.

v0.3 adds optional `traditional_condition` to the seven traditional planet records. It includes matched statuses, complete table values, `scoring_applied=false`, lineage, and Ptolemy source ID; Uranus, Neptune, and Pluto omit the field.

The report layer may add only evidence-linked structural themes. It must not recalculate positions, silently change house system or zodiac, or infer events. Unsupported coordinates, DST gaps/ambiguities, years, and house systems fail closed.
