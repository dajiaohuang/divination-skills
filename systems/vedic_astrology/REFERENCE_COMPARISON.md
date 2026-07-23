# Vedic reference comparison

## Independence statement

The ignored `references/upstream/vedic-astro-skills` checkout is pinned at
commit `e6d3d39073baca87f8e540b9b92fa758a1f5085a`. Its code is declared AGPL and
its instruction/resource layer carries additional commercial restrictions.
This system therefore does not import, vendor, translate, rewrite, or package
that repository's code, prompts, rules, resources, ephemeris files, or Python
dependencies.

The upstream repository is used only to identify comparison surfaces and
failure modes. The production implementation in this repository is written
against its own Apache-2.0 contracts and registered sources.

## v0.1 comparison matrix

| Surface | Upstream reference advertises | This repository v0.1 | Audit result |
|---|---|---|---|
| Time handling | Time zone conversion and DST failure handling | Strict IANA time, explicit fold, DST gap rejection | Implemented independently |
| Astronomy | Swiss Ephemeris / PyJHora stack | Astronomy Engine 2.1.19 and local formulas | No runtime or repository dependency |
| Sidereal origin | True Citra | Fixed-Spica true-Citra, explicitly not called Lahiri/KP | Same comparison family; independently specified |
| Core grahas | Seven planets plus nodes | Seven apparent geocentric planets plus mean nodes | Implemented; node policy disclosed |
| Lagna/houses | Sidereal lagna and sign-based houses among broader outputs | Sidereal lagna and whole-sign bhavas | Implemented |
| Nakshatra/pada | 27 nakshatras and four padas | 27 equal nakshatras and four padas | Implemented |
| D9 | Navamsha among many vargas | D9 sign only | Implemented; higher vargas unavailable |
| Vimshottari | Mahadasha/antardasha through PyJHora | Mahadasha only with declared 365.2425-day year | Partial by explicit scope |
| Jaimini karakas | Seven primary and eight reference | Seven/eight selectable, tie failure, Rahu reversal | Implemented and isolated |
| Jaimini sign techniques | Chara Dasha and additional modules | Rashi drishti and Arudha Lagna only | Partial by explicit scope |
| KP | Optional Placidus/cusp/star/sub calculations | Sign/star/sub identity only | Bounded; not described as complete KP |
| Strength systems | Shadbala, Ashtakavarga and other derived layers | Unavailable | Deliberately not approximated |
| Predictive Skills | Core/career/love/prashna/synastry/rectification | No predictive interpretation in Vedic v0.1 | Out of scope pending rules and review |

## Algorithmic cross-checks retained in tests

- The element-start and movable/fixed/dual formulations of D9 produce the same
  sign sequence across all 108 navamsha cells.
- The seven-kāraka ordering and optional eight-kāraka Rāhu reversal match the
  declared comparison surface.
- Nakshatra, pāda, Vimshottarī order, and KP unequal sub-lord arithmetic use
  unrounded half-open boundaries.
- Whole-sign Parāśarī bhāvas are never re-exported as KP cusps.
- No external checkout appears in package manifests or runtime dependencies.

These checks demonstrate contract consistency and comparison coverage. They do
not establish the empirical validity of astrology, do not replace an
independent Jyotiṣa review, and do not certify the upstream implementation.
