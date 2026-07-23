# Bazi v0.2 scope

## Supported

- Gregorian birth date and local civil time from 1900 through 2100;
- IANA time-zone identifiers, historical offsets, ambiguous-time `fold`, and nonexistent-time rejection;
- exact solar-term instant boundaries supplied by `lunar_python` 1.4.8;
- year, month, day, and hour pillars;
- hidden stems, five elements, polarity, visible and hidden Ten Gods;
- optional NOAA apparent-solar calculation clock from explicit longitude;
- 纳音, day-master and pillar-self 十二长生, seasonal 旺相休囚死, and visible five-element counts;
- deterministic branch combinations, clashes, harms, and punishments;
- optional forward or reverse ten-year luck-cycle sequence using the documented three-days-per-year start-age method;
- structured JSON facts, validation warnings, source IDs, rule IDs, and engine version;
- extraction/validation and conservative core explanation Skills.
- structured JSON and four-pillar text reading that never overwrites native facts;
- path-level imported/native pillar and day-boundary comparison;
- active luck-cycle, target year/month pillars, structural activation facts, and shared timeline;
- directional A-to-B/B-to-A visible Ten-God comparison plus symmetric branch relations;
- double-hour candidate rectification with at least five dated events and training/holdout separation;
- an explicitly selected `project-seasonal-support-v0.1` feature path that emits a low-confidence, fully disclosed support label; it is disabled by default and not release-eligible until external expert review.

## Not supported in v0.2

- lunar-calendar birth input;
- dates outside 1900–2100;
- automatic geocoding;
- automatic or undeclared true-solar-time correction, geocoding, or ephemeris-grade solar position;
- inferred luck-cycle direction from sex or gender;
- canonical school-specific strength adjudication, special structures, transformation structures, useful-god selection, climate adjustment, blind-school imagery, compatibility scoring, date selection, or deterministic event prediction;
- OCR/PDF reading, minute-level rectification, personality tie-breakers, and unique birth-time claims;
- medical, legal, financial, fertility, mortality, or other high-risk conclusions.

Unsupported fields must produce a validation error or explicit warning. They must never be approximated silently.
