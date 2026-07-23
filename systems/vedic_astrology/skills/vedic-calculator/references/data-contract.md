# Calculator contract

Require `local_datetime`, `timezone`, `longitude`, and `latitude`. Optional
fields are `fold`, `lineages`, `jaimini_karaka_policy`, and
`ayanamsha=true_citra`.

The common chart contains true-ecliptic-of-date seven-planet positions, mean
Rahu and opposite Ketu, a fixed-Spica true-Citra sidereal conversion, lagna,
nakshatra, pada, sign lord, whole-sign house, source IDs, and rule IDs.

Only selected lineage modules appear. Supported years are 1900–2100. Unknown
fields, unsupported policies, DST gaps, and unresolved DST folds fail closed.
See the system `DATA_CONTRACT.md` and `KNOWN_LIMITATIONS.md` for the complete
contract.
