---
name: western-validator
description: Compare an imported Western chart with project-native tropical geocentric facts using an explicit longitude tolerance and path-level position, house, and angle differences. Use for external natal chart validation, JSON/CSV comparison, or engine discrepancy review. Do not overwrite either chart, silently change frames or house systems, promote the reference to truth, or interpret differences as life claims.
---

# Western validator

1. Require native and imported JSON files.
2. Run `scripts/run.py --native ... --imported ... --tolerance-degrees 0.01`.
3. Report missing bodies, longitude deltas, house differences, and angle differences by path.
4. Preserve both inputs; do not repair one from the other.
5. Cite `WESTERN-VALIDATOR-COMPARE-001` and apply [references/safety.md](references/safety.md).
