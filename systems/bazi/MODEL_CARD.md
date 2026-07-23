# Bazi Skill suite v0.2 Model Card

Status: technical candidate; **not approved for production release**. The executable audit in `reviews/release.py` remains blocked until real domain, rights, and privacy reviewers sign the release record.

## Intended use

The suite converts a supported Gregorian local date/time and IANA time zone into traceable Bazi calculation facts, validates structured charts, and produces bounded explanations whose claims point to fact and rule IDs. It supports educational, reflective, and software-testing uses. It is not a scientific predictor and must not be used to determine medical care, legal rights, financial transactions, employment, insurance, education access, fertility, mortality, or other high-impact decisions.

## Components

- `bazi-calculator`: deterministic JSON calculation, no prose interpretation.
- `bazi-validator`: contract and provenance validation.
- `bazi-core`: evidence-linked report construction that cannot mutate computed facts.
- Optional `project-seasonal-support-v0.1`: isolated, low-confidence engineering feature model; disabled by default and not a canonical Ziping judgment.

## Calculation and lineage scope

The baseline uses exact Li Chun year change, 12 Jie month boundaries, IANA civil time, a default midnight day boundary with an explicit 23:00 alternative, explicit luck-cycle direction, and a three-days-per-year decimal start-age method. Civil time is the default; callers may explicitly select the NOAA apparent-solar approximation with longitude. The calculation layer also emits fixed 纳音, ten-stem 十二长生, seasonal 旺相休囚死, and visible-element counts without treating them as strength or useful-god judgments. See `LINEAGE.md`, `SCOPE.md`, and `KNOWN_DISPUTES.md` for frozen decisions and alternatives.

## Data and sources

The test data is synthetic. There are 100 standard calculation cases, 30 boundary cases, 20 dispute cases, and 20 invalid-input cases. Fifty traceable reasoning-chain candidates exist for human review, but none currently claims expert acceptance. Source manifests and rights decisions live in `sources/`; the local Vedic repository is ignored and governed by the clean-room policy.

The calculation path uses pinned `lunar-python 1.4.8`, Python `zoneinfo`, and `tzdata 2026.3`. The independent development comparator `sxtwl-modern 1.1.2` agrees on all four pillars for 97 of 100 standard fixtures; three inputs on Jie calendar dates are excluded because that API exposes date-level rather than exact-instant year/month boundaries. It is reference-only pending complete license review.

## Evaluation

Separate test groups cover:

- calculation: schema validation, 100 standard replays, 30 boundary replays, two-source comparison, date-cycle properties, DST folds/gaps, historical offsets, luck-cycle methods, and deterministic reproduction;
- rules: predicate/operator behavior, status gating, exception handling, lineage isolation, and immutable fact layers;
- narrative: every explanatory statement has at least one fact ID and rule ID, unsupported lineages are rejected, and optional strength output is off by default;
- failure handling: 20 invalid inputs must return documented typed errors rather than guessed repairs.

Run `pytest`, `ruff check .`, and `divination-validate .`. Run `python -m systems.bazi.reviews.release` for the fail-closed release gate. Current test counts are recorded by CI rather than hard-coded here.

## Known limitations

- Solar-term instants inherit the pinned provider and its fixed UTC+08 interpretation.
- The supported Gregorian window is 1900–2100; historical time-zone records can be approximate.
- Apparent solar time is optional, approximate, and never selected implicitly; it is not an ephemeris-grade SPA implementation.
- No gender-based luck direction is inferred.
- Classical strength, structure, transformation, climate adjustment, useful-god, relationship, and event-timing modules are not approved.
- Symbolic descriptions are not evidence of predictive validity. Synthetic fixtures cannot establish real-world accuracy.
- English/Chinese localization and accessibility review remain product-surface responsibilities.

## Human oversight and release method

A named independent Bazi expert must review 50 reasoning chains and the selected lineage. An authorized rights reviewer must approve all production sources, and a privacy reviewer must approve actual retention settings. Each reviewer signs `reviews/release-signoff.json`; machine-generated signatures are prohibited. Any rejected or changed item invalidates derived approvals until re-reviewed.

## Privacy

The default runtime is stateless. Real birth data must not enter source control, fixtures, prompts retained for training, or logs. If a product enables storage, follow `docs/policies/SENSITIVE_BIRTH_DATA.md`, including explicit purpose, encryption, access control, export/deletion, redaction, and retention limits.

## Packaging and changes

`divination-build` creates deterministic Skill zip artifacts with SHA-256 sidecars and embedded package/schema versions. Contract migrations follow `MIGRATIONS.md` and the machine-readable registry. Release-impacting changes require changelog entries, rerunning all evaluations, and renewed sign-off when evidence or lineage decisions change.
