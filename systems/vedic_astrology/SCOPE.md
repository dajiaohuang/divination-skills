# Vedic Astrology scope

This system produces auditable sidereal chart facts for three explicitly
separated Jyotiṣa lineages:

- `parashari-structural-v0.1`: rāśi positions, whole-sign houses, nakṣatra and
  pāda, navāṃśa, and a bounded Vimśottarī mahādaśā schedule;
- `jaimini-structural-v0.1`: selectable seven- or eight-chara-kāraka policy,
  rāśi dṛṣṭi, and ārūḍha lagna under a declared exception policy;
- `kp-stellar-v0.1`: sign lord, star lord, and Vimśottarī-proportional sub-lord
  identity only.

The common astronomy layer uses geocentric true ecliptic-of-date positions,
mean lunar nodes, strict IANA civil-time normalization, and a declared
Spica-anchored true-Citrā sidereal origin. The project does not import code,
rules, resources, prompts, or runtime packages from another astrology
repository.

This release does not make event predictions, medical or financial claims,
remedial prescriptions, or deterministic statements about a person. It does
not silently merge Parāśarī, Jaimini, and KP rules.

KP support is deliberately named a stellar layer rather than a complete KP
chart. Placidus cusps, cusp sub-lords, ruling planets, significator ranking,
horary-number charts, and event judgment remain out of scope.
