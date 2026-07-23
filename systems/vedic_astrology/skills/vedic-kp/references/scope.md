# KP stellar scope

Each 13°20′ nakshatra is divided into nine unequal sub-lord intervals. The
order starts with the nakshatra lord and follows the Vimshottari cycle. Each
interval occupies `nakshatra_size × lord_years / 120`. Boundaries are half-open
and use unrounded sidereal longitude.

This module does not implement a KP house model. In particular, it has no
Placidus cusps, cusp sub-lords, ruling planets, significator ranking,
horary-number mapping, or event judgment. Whole-sign house numbers in the
common/Parashari chart are not KP cusps.
