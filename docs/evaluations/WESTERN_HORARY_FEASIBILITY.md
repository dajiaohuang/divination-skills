# Western horary feasibility evaluation

Status: evaluated, not implemented

Production Skill: none

Reference lineage: traditional horary, William Lilly baseline
Reference source: `SRC-WESTERN-LILLY-001`

## Decision

Western horary astrology must remain a separate system boundary. The current Western natal,
timing, synastry, and rectification modules cannot be relabeled as horary. Astronomy Engine can
provide much of the astronomical position layer, but the repository does not yet contain the
traditional judgment model required to answer a question.

No `western-horary` Skill will be exposed until the contract, calculations, rules, sources,
Golden Cases, and expert review below are complete. This is a deliberate fail-closed decision,
not an invitation for a language model to improvise missing doctrine.

## Required input contract

- the exact moment and place at which the astrologer receives and understands the question;
- timezone, UTC offset, DST fold/gap handling, latitude, and longitude;
- one clearly scoped question and a declared question category;
- an explicit policy for repeated, trivial, coercive, or third-party-private questions;
- a question chart ID that can never be confused with a natal chart ID.

## Missing calculation layer

- the chosen traditional house system, with Regiomontanus evaluated before adoption;
- essential dignity tables, sect, planetary condition, speed, retrogradation, combustion,
  cazimi, under-the-beams status, and accidental dignity;
- applying and separating aspects with temporal perfection, not only static orb matching;
- the Moon's last and next applications and void-of-course policy;
- house rulers, derived houses, and category-specific significator assignment;
- reception, prohibition, refranation, frustration, translation of light, and collection of
  light;
- traditional considerations before judgment, recorded as warnings rather than silently used
  to reject a chart.

The current production engine supports only whole-sign and equal houses and major static
aspects. Those capabilities are insufficient for this lineage.

## Required rule packs

Rules must be split by task instead of collapsed into one prompt:

1. chart radicality and considerations before judgment;
2. querent, quesited, Moon, and co-significator selection;
3. perfection and denial of perfection;
4. reception and dignity;
5. timing estimates with explicit unit-selection rules;
6. question-category packs such as property, relationship, missing objects, and travel;
7. privacy and high-impact restrictions.

Every conclusion must cite chart facts, reviewed rule IDs, source locators, counterevidence, and
known disputes. Natal personality statements cannot be used as a substitute for horary rules.

## Evidence and release gates

Before implementation is considered releasable, prepare at minimum:

- 100 verified question charts;
- 30 time, DST, latitude, house-cusp, and station boundary cases;
- 20 explicit lineage or judgment disputes;
- 50 expert-review candidates with full reasoning and prohibited conclusions;
- at least two independent calculation comparators;
- retained holdout cases that rule authors cannot inspect;
- a completed domain review and rights review.

The historical reference is `reference_only`; it is not copied into Skill packages. A future
implementation must transcribe only the necessary public-domain facts with exact locators and
must undergo a separate rules review.
