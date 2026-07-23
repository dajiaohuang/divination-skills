# Vedic Astrology lineage policy

## Shared astronomical baseline

All enabled lineages receive the same normalized instant and geocentric
ecliptic facts. Tropical longitudes are converted to sidereal longitudes by
subtracting a dynamically calculated true-Citrā offset: the tropical
ecliptic-of-date longitude of Spica is anchored to 180° sidereal. The fixed
stellar coordinates are the J2000 catalogue values declared in the project
contract; annual aberration and stellar proper motion are not applied to the
anchor. This is not labelled Lahiri, Raman, KP, Yukteśvara, or any other
ayanāṃśa.

Rāhu is the mean ascending lunar node calculated from a documented polynomial;
Ketu is exactly opposite. Users must not compare these node positions to a
true-node chart without changing the policy in a future version.

## Parāśarī structural profile

`parashari-structural-v0.1` uses:

- sidereal rāśis and whole-sign bhāvas from sidereal lagna;
- 27 equal nakṣatras of 13°20′, each divided into four pādas;
- the Ketu–Venus–Sun–Moon–Mars–Rahu–Jupiter–Saturn–Mercury Vimśottarī order;
- navāṃśa signs derived from the movable/fixed/dual starting-sign rule;
- a 365.2425-day computational year for ISO schedule boundaries.

The last item is a software time-scale policy, not a claim that every
Parāśarī school uses the same daśā year length.

## Jaimini structural profile

`jaimini-structural-v0.1` supports two non-mergeable chara-kāraka policies:

- `seven`: Sun through Saturn, excluding the nodes;
- `eight`: Sun through Saturn plus Rāhu, whose within-sign arc is reversed.

Ranks are determined by descending effective degree within a sign. Exact ties
are rejected because silently breaking them would manufacture a lineage rule.

Rāśi dṛṣṭi follows the movable/fixed/dual sign-class relation. Ārūḍha lagna
uses the counted distance from lagna to its lord and repeats that distance from
the lord. When the ordinary result is the source sign or its seventh, this
profile places the ārūḍha tenth from the lord and reports the exception.

## KP stellar profile

`kp-stellar-v0.1` implements only a reproducible stellar identity:

- sidereal sign lord;
- nakṣatra/star lord;
- one of nine unequal sub-lords in Vimśottarī order and proportion.

It intentionally does not reuse whole-sign bhāvas as KP cusps. Complete KP
practice requires a separately sourced and tested cusp, significator, ruling
planet, and judgment layer.

## Source hierarchy

Classical texts establish historical terminology and structural concepts.
Official astronomical material establishes the modern nirayana/panchang
context. Modern Jaimini and KP pages are corroborating, rights-restricted
references only. Project-authored contracts resolve software boundaries and
never present a disputed convention as universal doctrine.
