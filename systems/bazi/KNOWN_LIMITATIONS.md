# Known limitations

- Solar-term timestamps depend on the pinned `lunar_python` implementation. Its naive timestamps are treated as fixed UTC+08:00; this assumption needs broader astronomical comparison before production promotion.
- The supported date window is deliberately narrower than the dependency's possible range.
- Pre-1970 historical time-zone data can contain approximations inherited from IANA data.
- Apparent solar time uses NOAA's compact fractional-year approximation, not NREL SPA or an ephemeris-grade implementation; it is never selected implicitly.
- Luck-cycle start age is a method-specific decimal, not a universally accepted calendar timestamp.
- The optional project seasonal-support score is an engineering baseline, not an expert-approved canonical strength judgment. It is off by default and cannot support structure, useful-god, climate, or event-timing claims.
- Synthetic development cases are not evidence of predictive validity.
- Timing relations are structural activations and do not predict events.
- Synastry facts do not score compatibility or infer intent, fidelity, or outcome.
- Rectification scans double-hour ranges only and returns `underdetermined` when retained events
  cannot separate candidates; it cannot establish a unique minute.
- Reader and validator accept structured JSON or explicit four-pillar text only, not OCR/PDF.
- The user-supplied external regression covers one chart; its unreported provider/version prevents
  broader compatibility claims.
