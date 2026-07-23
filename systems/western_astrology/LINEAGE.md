# Western astrology lineage

The natal baseline is `tropical-geocentric-v0.1`; v0.2 extensions use
`tropical-geocentric-major-aspects-v0.2`, while retained-event rectification is isolated as
`western-event-retained-rectification-v0.2`.

v0.3 adds `tropical-traditional-condition-v0.3`, an unscored Ptolemaic table layer limited to Sun, Moon, Mercury, Venus, Mars, Jupiter, and Saturn. It never assigns modern outer-planet rulerships.

- Zodiac: tropical, true ecliptic and equinox of date.
- Planet frame: geocentric apparent positions from Astronomy Engine 2.1.19; no topocentric lunar parallax.
- Bodies: ten conventional planets/luminaries from Sun through Pluto.
- Angles: horizon/ecliptic and meridian/ecliptic intersections using observer latitude, east-positive longitude, and Greenwich apparent sidereal time from the pinned engine.
- Houses: whole-sign default; equal house optional. Both are explicit and never silently mixed.
- Aspects: conjunction/opposition 8°, trine/square 7°, sextile 5°; each pair receives at most the closest qualifying major aspect.
- Interpretation: project-authored symbolic labels only, no deterministic event prediction.
- Timing: transit-to-natal major aspects and solved geocentric tropical solar returns; no
  progressions or directions.
- Synastry: symmetric cross-chart aspects remain separate from directional house overlays.
- Rectification: dated training and holdout events are mandatory and unresolved evidence returns
  `underdetermined`.
- Horary astrology is not part of either production lineage. It requires a separate question-time
  contract, house system, dignity tables, significator rules, and expert-reviewed Golden Cases
  before a Skill can be exposed.
