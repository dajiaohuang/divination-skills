# v0.1 calculation policy

- Year changes at the exact instant of 立春.
- Month changes at the exact instant of the 12 节.
- Naive solar-term timestamps from the pinned provider are interpreted as fixed UTC+08:00, not historical `Asia/Shanghai` DST.
- Day changes at midnight by default; `zi_initial` changes it at 23:00.
- The late-Zi hour stem uses the next civil day's stem basis.
- Local civil time comes from IANA `zoneinfo`; no mean or apparent solar-time correction is applied.
- Luck-cycle direction is explicit, never inferred from gender.
- Luck-cycle start age uses the adjacent-term interval divided by three days per year and is method-specific.

Disclose non-default choices. Do not present this policy as the only historical lineage.
