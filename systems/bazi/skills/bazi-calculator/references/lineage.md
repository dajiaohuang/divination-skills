# v0.2 calculation policy

- Year changes at the exact instant of 立春.
- Month changes at the exact instant of the 12 节.
- Naive solar-term timestamps from the pinned provider are interpreted as fixed UTC+08:00, not historical `Asia/Shanghai` DST.
- Day changes at midnight by default; `zi_initial` changes it at 23:00.
- The late-Zi hour stem uses the next civil day's stem basis.
- Local civil time comes from IANA `zoneinfo`; it remains the default calculation clock.
- Explicit `apparent_solar` uses NOAA's fractional-year equation-of-time approximation plus longitude correction before pillar date/hour selection. The physical UTC instant and solar-term boundaries remain unchanged.
- 纳音, ten-stem 十二长生, and 旺相休囚死 use bounded tables/formulas sourced to 《三命通会》; visible element counts exclude hidden stems.
- Luck-cycle direction is explicit, never inferred from gender.
- Luck-cycle start age uses the adjacent-term interval divided by three days per year and is method-specific.

Disclose non-default choices. Do not present this policy as the only historical lineage.
