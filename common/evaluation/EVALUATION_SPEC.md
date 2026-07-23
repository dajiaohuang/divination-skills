# Evaluation specification v0.1

Release evidence is reported by layer. A single aggregate “accuracy” score is prohibited.

## Required metrics

### Calculation

- Golden Case exact consistency: supported deterministic fields match committed expected output.
- Independent comparator consistency: comparable cases match a separately maintained implementation; exclusions are enumerated and justified.

### Rules

- Required-rule recall: Golden Case rules that must fire are present in evaluated findings or linked narrative.
- Unknown-rule misuse rate: cited rule IDs absent from the repository are counted as errors.

### Narrative

- Citation completeness: each non-limitation statement has fact and rule IDs.
- Fact-reference validity: every cited fact ID exists in immutable computed facts.

### Lineage

- Cross-system contamination rate: rule IDs from another system without an explicit bridge contract.

### Human review

- Accepted review count and required count are reported separately and never synthesized from automated tests.

Each metric records numerator, denominator, value, threshold, comparison direction, pass/fail, and evidence locators. Zero-denominator metrics are invalid. Technical pass and release-ready are separate: external signoffs and human review may keep release-ready false after all automated metrics pass.
