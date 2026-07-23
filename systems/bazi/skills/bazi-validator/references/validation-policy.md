# Validation policy

Accept a chart only when its input and calculation policy are reproducible.

Check, in order:

1. Gregorian local date and recorded clock precision;
2. IANA time zone, historical UTC offset, and DST fold;
3. exact 立春 and monthly 节 boundaries;
4. midnight or 23:00 day-boundary selection;
5. whether true solar time was claimed;
6. four pillars and late-Zi hour handling;
7. hidden stems, Ten Gods, relations, and luck-cycle method;
8. engine version and registered source IDs.

A visual chart without its birth input is `unverified_external`. A chart with a pillar mismatch is `invalid` until the mismatch is resolved. A near-boundary chart remains `valid_with_warnings` only when its recorded time precision is adequate.
