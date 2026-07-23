# Implementation completion audit

Date: 2026-07-23

This audit maps the explicit `IMPLEMENTATION_PLAN.md` requirements to repository evidence. A green
technical gate is not a substitute for a real domain, rights, or privacy approval.

## M0 — reference baseline and governance

| Requirement | Evidence | Result |
|---|---|---|
| Upstream Vedic reference is reproducible but not tracked | `.gitignore`, `references/README.md`, `catalog/sources/SRC-VEDIC-REF-001.json` | passed |
| Reference is not a submodule | no `.gitmodules`; `git ls-files references/upstream` is empty | passed |
| Clean-room, source, contribution, security and ADR policies | `docs/policies/`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/adr/` | passed |

## M1 — cross-system contracts and tooling

| Requirement | Evidence | Result |
|---|---|---|
| Four core schemas | `common/schemas/` | passed |
| At least three valid and three invalid checks per core schema | `tooling/tests/test_schemas.py` | passed |
| ID, reference, lineage and production-rights gates | `divination_skills.validation`, `tooling/tests/test_validation.py` | passed |
| Auditable report, evaluation and sign-off contracts | `common/report-spec/`, `common/evaluation/` | passed |
| Per-system completeness and Skill metadata checks | `validate_system_completeness`, `validate_skill_packages` | passed |
| CI validates, tests, lints, audits and builds | `.github/workflows/validate.yml` | passed locally; CI definition present |

## M2/M3 — Bazi vertical slice and production evaluation

| Requirement | Evidence | Result |
|---|---|---|
| Frozen scope, lineage, data and failure contracts | `systems/bazi/{SCOPE,LINEAGE,DATA_CONTRACT,KNOWN_DISPUTES,KNOWN_LIMITATIONS}.md` | passed |
| Deterministic four pillars, hidden stems, Ten Gods, relations and optional luck cycles | `systems/bazi/calculator/` | passed |
| 100 standard, 30 edge, 20 dispute and 20 invalid-input cases | `systems/bazi/tests/` | passed |
| Independent comparator | 97 comparable sxtwl cases pass; three Jie-date exclusions are recorded | passed within declared comparator boundary |
| Evidence-linked report without fact mutation | `systems/bazi/core/`, report-contract tests | passed |
| Layered calculation/rule/narrative/lineage metrics | `systems/bazi/evaluations/EVALUATION_REPORT.json` | technical pass |
| 50 expert reasoning candidates | `systems/bazi/evaluations/expert_candidates/` | prepared, 0 accepted |
| Domain, rights and privacy release approvals | `systems/bazi/reviews/release-signoff.json` | pending |

## M4/M5 — extension systems

Tarot, Western astrology, Ziwei, I Ching, Liuyao, bounded Qimen foundation, Lenormand, runes and
numerology each have an isolated scope and lineage, data contract, source ledger, structured rules,
Golden Set, edge case, dispute case, deterministic engine, report boundary, Skill, tests, domain
review batch and fail-closed release record.

The nine extension review batches contain 78 cases. They are intentionally pending and must be
accepted independently; one system cannot inherit another system's approval. Qimen remains the
explicit `foundation_only` slice described in its scope, not a complete interpretive pan. Wave C
(feng shui, palmistry and physiognomy) and Human Design remain outside the authorized current
scope exactly as stated in the plan.

## Installable Skill artifacts

The builder packages 14 Skills with fixed ZIP timestamps, project-authored runtime code, directly
installable pinned `requirements.txt` files and SHA-256 sidecars. Ziwei uses the project-native
foundation and the existing lunar-python calendar dependency; it has no Node.js or iztro runtime.
Reference-only source manifests and ignored repositories are excluded from artifacts.

Every artifact also includes a per-file `CONTENT_MANIFEST.json`, an extracted-package verifier, the
complete Apache-2.0 `LICENSE`, project license decision record and a license-status notice.
`PROJECT_LICENSE.json` records the owner's selected open-source model.

The repository also has a schema-validated deployment decision record at
`common/deployment/DEPLOYMENT_PRIVACY.json`. It is intentionally `undecided`; readiness refuses
release until the owner records the real deployment's data flows, retention, controls, user rights,
providers, minors policy and incident role. Retained user data activates stricter control checks.

`divination-build --release` enforces the terminal gate before creating an output directory. The
current undecided deployment policy and pending reviews produce `release_not_ready` and zero formal
release artifacts; ordinary builds remain validation packages.

`tooling/tests/test_build.py` extracts every ZIP outside the repository and executes all 14 scripts
with isolated Python path handling. This proves that the artifacts do not depend on the source
checkout. A second build must produce identical hashes.

## Current terminal gate

Technical implementation can pass while release remains closed:

```text
technical_complete = 10 / 10
release_ready = 0 / 10
project_license_status = selected
deployment_privacy_status = undecided
bazi expert_accepted = 0 / 50
extension domain-review cases accepted = 0 / 78
```

The implementation objective cannot be called production-approved until the owner selects the
deployment data policy and real reviewers complete the domain queues and the rights/privacy reviews
of the intended deployment. Automation must not generate those decisions, identities or approvals.

Accepted domain and release records require hashed evidence. `divination-evidence` creates a
repository-relative evidence record, and readiness rejects changed retained files or paths that
escape the repository. Sensitive evidence may remain in controlled external storage with a stable
locator and SHA-256 value.
