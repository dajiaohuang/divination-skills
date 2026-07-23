# Runes data contract v0.3

Input requires `spread` (`single` or `three-rune`) and accepts optional question and replay seed. Reversals are unsupported. Questions are output only as SHA-256.

Output discloses seed, commitment, symbol-set hash, draw ID, and unique symbols drawn without replacement. Each result records position, Elder Futhark project symbol ID, index, conventional name, upright orientation, fact ID, and source IDs.

v0.3 also records `character`, `codepoint`, `unicode_name`, `transliteration`, and `identity_lineage`. Identity facts cite Unicode and the Swedish History Museum; modern reflection remains project-sourced.

Interpretation uses newly authored project keywords and is explicitly modern symbolic reflection. It is not presented as a reconstruction of historical Germanic divination.
v0.2 `build_layers` accepts a valid draw and returns disjoint `historical_evidence` and
`modern_reflection` arrays. Every record has its own fact, rule, and source IDs.
`historical_divinatory_meaning_claimed` is always false and the cross-layer policy is explicit.
