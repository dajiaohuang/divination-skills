# Implementation completion audit

Date: 2026-07-24

This audit maps both implementation plans to repository evidence. “Passed” means the authorized
technical scope is present and automatically verified. It never substitutes for real domain,
rights, or deployment-privacy approval.

## M0–M5 — original implementation plan

| Milestone | Evidence | Result |
|---|---|---|
| M0 governance and ignored references | `.gitignore`, `references/README.md`, `docs/policies/`, `CONTRIBUTING.md`, `SECURITY.md` | passed |
| M1 schemas, lineage, validation and build | `common/schemas/`, `tooling/src/divination_skills/`, `.github/workflows/validate.yml` | passed |
| M2 Bazi vertical slice | `systems/bazi/calculator/`, `validator.py`, `core/`, three original Skills | passed |
| M3 Bazi evaluation and release gates | `systems/bazi/tests/`, `evaluations/`, `reviews/`, `MODEL_CARD.md` | technical pass; human review pending |
| M4 Tarot and Western astrology | `systems/tarot/`, `systems/western_astrology/` | passed |
| M5 seven further vertical slices | Ziwei, I Ching, Liuyao, Qimen, Lenormand, runes and numerology directories | passed |

The ignored Vedic, iztro and kinqimen checkouts are reproducible research references only. The
repository now has its own source-backed Vedic implementation; it does not import or copy the
ignored checkout. There is no `.gitmodules`, no tracked `references/upstream/` file, and no
production import, subprocess, vendored code, test fixture, or package dependency on those
repositories.

## M6 — shared session, confidence and timeline contracts

| Requirement | Evidence | Result |
|---|---|---|
| Six system-neutral contracts | `common/schemas/{reading-session,chart-import,confidence-profile,timeline,comparison,report-profile}.schema.json` | passed |
| Stable IDs and legacy chart wrappers | `tooling/src/divination_skills/contracts.py` | passed |
| Precision-based degraded/blocked modules | confidence-profile examples and `tooling/tests/test_contracts.py` | passed |
| Ephemeral defaults and log redaction | reading-session contract and privacy tests | passed |
| Report-section selection without new rules | report-profile contract and `common/product_views.py` | passed |

## M7–M9 plus source-backed extension — native Ziwei v0.5

| Requirement | Evidence | Result |
|---|---|---|
| Solar/lunar input and explicit leap/year/late-Zi policies | `systems/ziwei/engine.py`, `policies.py`, `input.schema.json` | passed |
| Extended star catalog and four twelve-stage cycles | `catalog.py`, `cycles.py`, structured rule files | passed |
| Six dynamic scopes and shared timeline | `systems/ziwei/timing.py` | passed |
| Palace/star/空宫/三方四正/四化 queries | `systems/ziwei/analyzer.py` | passed |
| NOAA apparent solar time, classical brightness, and self-transformation provenance | `solar_time.py`, `star_catalog.py`, external regression | passed |
| Reader, validator, core and synastry boundaries | six Ziwei Skills and supporting modules | passed |
| 100 standard, 30 boundary, 20 dispute and 50 synastry replay cases | `systems/ziwei/tests/` | passed |
| Independent upstream difference classification without dependency | ignored iztro reference plus native tests/package audit | passed |
| Expert acceptance | 150 pending domain-review records | pending |

The native implementation does not claim total parity with iztro. Difference categories remain
explicitly school-, boundary-, reference-, project-, or research-dependent.

## M10 — Bazi and Western eight-role expansion

| System | Reader/validator | Timing | Synastry | Rectifier | Replay cases | Result |
|---|---:|---:|---:|---:|---:|---|
| Bazi | structured JSON and explicit pillar text; native facts immutable | luck/year/month structural activations | directional Ten Gods and symmetric branch relations | double-hour ranges with training/holdout events | 150 | passed |
| Western astrology | JSON/CSV and tolerance-aware comparison | transits and solved solar returns | directional house overlays and symmetric aspects | candidate intervals with training/holdout events | 150 | passed |

Both rectifiers return ranked intervals or `underdetermined`; neither may manufacture a unique
minute. Imported charts generate comparison records and never overwrite native calculations.

## M11 — shared product views

`common/product_views.py` and its report profiles provide career, relationship, timing and bounded
Q&A selection for Bazi, Western astrology and Ziwei. The views reuse registered fact/rule IDs,
include limitations, preserve fact immutability and downgrade medical, legal, financial, safety,
employment and other high-impact questions to reflective information.

No specialist view creates a hidden calculation path or an uncatalogued domain rule.

## M12 — comparison, rectification and horary assessment

- Bazi, Western astrology and Ziwei have independently validated two-chart comparison layers.
- Bazi and Western astrology have retained-event, training/holdout rectification workflows.
- `docs/evaluations/WESTERN_HORARY_FEASIBILITY.md` records that Western horary astrology requires a
  separate lineage, input contract, calculation scope, sources, rules and Golden Set. It was
  intentionally not mixed into natal astrology.
- I Ching, Liuyao and Qimen remain separate immediate-question systems; no Vedic Prashna rule is
  reused.

## M13 — long-tail depth

| System | Implemented technical scope | Replay corpus | Result |
|---|---|---:|---|
| Liuyao | explicit question packs, candidate 用神, transparent strength factors, moving/change facts, branch timing keys | 50 | passed |
| Qimen | heaven/earth plates, nine stars, eight doors, eight spirits, void/tomb/punishment/oppression flags | 100 | passed |
| I Ching | two explicit moving-line policies, two edition locators, uncollated-version status | 70 | passed |
| Lenormand | pairs, nine-card coordinates and 4×9 Grand Tableau houses/significator coordinate | 70 | passed |
| Tarot | four added spreads, adjacency/distribution analysis, consent-gated local journal/statistics | 70 | passed |
| Runes | public-domain historical metadata separated from modern reflective prompts | 70 | passed |
| Numerology | isolated Chaldean method and mandatory explicit non-Latin transliteration | 70 | passed |

These capabilities are deliberately bounded. They do not create expert-approved predictive
judgments, copy modern guidebooks or deck art, or silently merge disputed methods.

## M14 — independent multi-lineage Vedic astrology

| Requirement | Evidence | Result |
|---|---|---|
| Source-traced sidereal base chart | `systems/vedic_astrology/calculator/`, registered public-domain/official astronomy and classical sources | passed |
| Explicit astronomical and civil-time policy | true-Citra fixed-Spica anchor, mean lunar node, strict IANA time, stated apparent/mean choices | passed |
| Parāśarī scope | whole-sign D1, D9 navamsha and Vimshottari Mahadasha with declared computational year | passed |
| Jaimini scope | isolated seven/eight Chara Karaka modes, rashi drishti and Arudha Lagna | passed |
| KP scope | bounded sign/star/sub-lord mathematical identity; no cusp, significator or prediction layer | passed |
| School isolation and disputes | 16 structured rules, five explicit dispute records, lineage selectors and fail-closed boundaries | passed |
| Independent replay evidence | 8 Golden, 4 edge and 5 dispute cases plus direct unit/property checks | passed |
| Upstream independence | ignored `vedic-astro-skills` comparison only; no runtime/build/test dependency or copied prompt/resource | passed |
| Expert acceptance | 17 pending domain-review records | pending |

The implementation does not claim to cover all Jyotiṣa schools. Modern Jaimini and KP pages are
reference-only corroboration and are excluded from installable packages.

## M15 — multi-natal birth orchestration

| Requirement | Evidence | Result |
|---|---|---|
| One confirmed birth profile | `systems/multi_natal/calculator/input.schema.json`, strict IANA zone/coordinate/location-source/gender validation | passed |
| Native independent charts | Bazi, Western, Ziwei and Vedic engines run unchanged; optional numerology requires an explicit name and mapping | passed |
| Shared-instant audit | all four core charts must normalize to one UTC instant or calculation fails | passed |
| Astronomy audit | Western tropical and Vedic retained tropical Sun–Saturn/Ascendant coordinates agree within `1e-6°` | passed |
| Lineage isolation | civil/apparent-solar, house, Ziwei boundary, Parāśarī/Jaimini/KP and numerology policies remain explicit | passed |
| Bounded synthesis | five navigation axes retain source fact/rule IDs and prohibit equivalence, voting, recurrence or agreement scores | passed |
| Replay evidence | one Golden, one DST-fold edge and one time-basis dispute case plus schema/failure/property tests | passed |
| Standalone package | package contains required native project runtimes and pinned Python requirements with no external repository dependency | passed |
| Expert acceptance | 3 pending domain-review records | pending |

The orchestration layer is counted as a technical system directory, not as a twelfth divination
tradition. It stores every native chart under its original system identity and never rewrites a
school-specific fact into a universal prediction.

## Installable Skill artifacts

The builder packages 35 Skills with fixed ZIP timestamps, directly installable pinned
`requirements.txt` files, SHA-256 sidecars, a per-file `CONTENT_MANIFEST.json`, an extracted-package
verifier, Apache-2.0 license materials and third-party notices.

`tooling/tests/test_build.py` builds every package twice, verifies identical hashes, extracts the
artifacts outside the repository and executes every Skill entry workflow under isolated Python path
handling. Reference-only manifests and ignored repositories never enter an artifact. Ziwei has no
Node.js or iztro runtime.

## Automated evidence snapshot

```text
technical_system_directories = 12
skills = 35
structured_rules = 141
source_manifests = 47
baseline_golden = 264
edge_cases = 74
dispute_cases = 55
invalid_inputs = 20
extension_replay_cases = 850
pytest = 1584 passed
technical_complete = 12 / 12
```

The focused engine and Skill re-audit, confirmed fixes, evidence hierarchy and residual limits are
recorded in `docs/ENGINE_SKILL_AUDIT_2026-07-24.md`.

## Terminal release gate

Technical implementation is complete while formal release remains closed:

```text
release_ready = 0 / 12
project_license_status = selected
deployment_privacy_status = undecided
bazi expert_accepted = 0 / 50
extension domain-review cases accepted = 0 / 243
```

`divination-build --release` enforces this gate before creating an output directory. Ordinary
builds are validation artifacts, not production-approved releases.

Real reviewers must accept the domain queues and supply hashed evidence. The owner must also record
the intended deployment’s rights and privacy decisions. Automation must not generate reviewer
identities, signatures or approvals.
