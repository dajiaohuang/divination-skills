# Release review protocol

Every system is technically auditable before it is commercially releasable. The two states are
deliberately separate.

Project-authored material uses the owner-selected Apache-2.0 model recorded in
`common/licensing/PROJECT_LICENSE.json`. Changing that decision requires a new owner decision and
compatibility review; the selected license does not override any external source terms.

The actual deployment also needs an owner-configured data policy in
`common/deployment/DEPLOYMENT_PRIVACY.json`. While it is `undecided`, privacy sign-off cannot be
accepted and `release_ready` remains false. The readiness audit applies additional protections when
the deployment retains accounts, birth data, questions, or readings.

`reviews/release-signoff.json` must contain exactly one `domain`, `rights`, and `privacy` entry.
Pending entries are valid repository state but make `release_ready` false. An accepted entry must
identify a real reviewer, a timestamp, and durable evidence. Generated identities, self-approval by
automation, and inherited approval from another system are prohibited.

The domain reviewer checks lineage decisions, every case listed in `reviews/domain-review.json`,
dispute handling, derived claims, and known limitations. Each case receives an explicit decision;
the batch can be accepted only when every case is accepted. Bazi uses its larger, equivalent
`evaluations/expert_candidates/` queue. The rights reviewer checks every source and asset used by a
production rule or interface. The privacy reviewer checks the actual deployed collection,
retention, export, deletion, access-control, and logging settings.

Accepted records require a SHA-256 evidence object. Retain an evidence file under the repository
and create that object with `divination-evidence <path> --root .`; readiness rehashes retained files
and fails on changes. External evidence may be referenced by a stable locator and hash with
`retained_in_repository=false`, but the organization remains responsible for preserving it. Do not
commit signature scans, birth data, private contact details, or other sensitive evidence merely to
make the automated hash check available.

Run `divination-readiness .` for the consolidated audit. CI uses `--require-technical`, which fails
for incomplete contracts or malformed sign-off records while allowing honest pending human review.
Use `--require-ready` only for a release promotion.
