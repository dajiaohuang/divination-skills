# Known limitations

- Solar-term timestamps depend on the pinned `lunar_python` implementation. Its naive timestamps are treated as fixed UTC+08:00; this assumption needs broader astronomical comparison before production promotion.
- The supported date window is deliberately narrower than the dependency's possible range.
- Pre-1970 historical time-zone data can contain approximations inherited from IANA data.
- Coordinates are retained but do not trigger mean or apparent solar-time correction.
- Luck-cycle start age is a method-specific decimal, not a universally accepted calendar timestamp.
- The optional project seasonal-support score is an engineering baseline, not an expert-approved canonical strength judgment. It is off by default and cannot support structure, useful-god, climate, or event-timing claims.
- Synthetic development cases are not evidence of predictive validity.
