# Known Tarot disputes

- `DSP-TAROT-REVERSALS-001`: use reversals or an upright-only deck. v0.2 defaults to reversals but records an explicit caller override.
- `DSP-TAROT-RWS-UNIVERSAL-001`: RWS is a named deck lineage, not universal Tarot. v0.3 rejects silent substitution from other traditions.
- Deck lineage is fixed to the project RWS-compatible text baseline. Marseille, Thoth, oracle decks, and modern commercial guidebook wording are not interchangeable.
- Multi-card sequence is read in declared position order. Elemental dignities, card counting, and free-form adjacency methods are not silently added.

All alternative methods require a new lineage ID, source manifest, rules, and Golden Cases.
