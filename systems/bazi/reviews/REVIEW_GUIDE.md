# Bazi v0.1 external review guide

This workflow is for real, accountable reviewers. Do not use automation or an AI-generated identity to mark a review accepted.

## 1. Domain review

Reviewer qualification: an independent Bazi practitioner who can evaluate the frozen `ziping-calculation-baseline` decisions and every rule ID cited by the candidate analyses.

For each file in `systems/bazi/evaluations/expert_candidates/`:

1. Recompute or independently inspect the referenced case facts.
2. Check every `fact_id` and `rule_id` in the reasoning chain.
3. Confirm that the statement stays within the selected lineage and does not claim a fixed event.
4. Set `review.status` to `reviewed`.
5. Record the reviewer's stable organizational ID, review date, decision, and concrete notes.
6. Use `accepted` only when the whole candidate is acceptable; otherwise use `changes_requested` or `rejected`.

After all 50 files are accepted, the domain reviewer may update the `domain` entry in
`release-signoff.json`. Retain the signed review record, run
`divination-evidence <record-path> --root .`, and place the resulting locator and SHA-256 object in
the signoff evidence array. The readiness audit rehashes evidence retained in the repository.

## 2. Rights review

The rights reviewer must inspect every manifest in `systems/bazi/sources/`, the clean-room policy, the source-acceptance policy, the packaged contents, and dependency licenses. Confirm that reference-only sources are not distributed or promoted into production rules. Record any deployment-specific commercial obligations in the signoff notes.

## 3. Privacy review

The privacy reviewer or product owner must bind the generic policy to the actual deployment: whether birth data is stored, the retention period, access controls, encryption, export/deletion workflow, logging, incident handling, and the lawful/consent basis. A policy template without real deployment settings is not sufficient.

## 4. Validation

Run:

```powershell
.\.venv\Scripts\pytest.exe systems\bazi -q
.\.venv\Scripts\divination-validate.exe .
.\.venv\Scripts\divination-readiness.exe . --require-technical
.\.venv\Scripts\python.exe -m systems.bazi.reviews.release --report-only
```

The release is eligible only when `expert_accepted` is 50, every signoff is `accepted`, and `ready` is `true`. The audit checks structure and counts; it does not verify that a reviewer identity is genuine. Organizational release control must verify that separately.
