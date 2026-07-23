# Auditable report contract v0.1

Every runtime result separates four layers:

1. `normalized_input`: validated calculation or draw parameters, including explicit lineage and time/randomness policy.
2. `computed_facts`: immutable, reproducible facts. Each addressable fact should carry a stable `fact_id` and source IDs where practical.
3. `derived_findings`: rule results that cite rule IDs, evidence, confidence, and sources. Findings never overwrite computed facts.
4. `narrative`: user-facing statements. Every factual or symbolic statement must cite at least one fact ID and one rule ID. Limitations may be plain strings.

The result also includes:

- `schema_version`;
- engine name, version, dependencies, and source IDs;
- validation status and warnings;
- audit data required to replay randomized results.

Writers must deep-copy or otherwise protect `computed_facts` before rule evaluation. A report is invalid if narrative references an unknown fact or rule, if a cross-system rule appears without an explicit bridge contract, or if missing calculation facts are reconstructed from model memory.
