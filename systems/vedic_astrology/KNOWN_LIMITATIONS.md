# Known Vedic Astrology limitations

- Only the true-Citrā fixed-Spica sidereal origin is implemented.
- Spica uses declared J2000 coordinates without annual aberration or a
  proper-motion correction.
- Rāhu/Ketu are mean nodes; true nodes are unavailable.
- The calculation range is 1900–2100 and has not been certified for historical
  chronology.
- Only D1 and D9 are implemented; no higher vargas or divisional dignity logic
  is provided.
- Vimśottarī output is mahādaśā-only and its calendar boundaries use the
  declared 365.2425-day computational year.
- Jaimini chara daśā, argalā, upapada, sthira kārakas, and interpretive
  judgments are unavailable.
- KP output is not a complete KP chart: no Placidus cusps, cusp sub-lords,
  ruling planets, significator ranking, horary-number chart, or prediction.
- No yogas, avasthās, ṣaḍbala, aṣṭakavarga, gochara interpretation, remedial
  advice, compatibility score, or event prediction is implemented.
- Modern Jaimini and KP references are rights-restricted corroboration, not
  redistributed training corpora.
- The upstream `vedic-astro-skills` repository is ignored, reference-only, and
  neither imported nor packaged.
