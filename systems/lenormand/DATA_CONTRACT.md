# Lenormand data contract v0.1

Input requires `spread` (`single`, `three-card`, or `nine-card`) and accepts optional question and replay seed. `allow_reversals` must be false in this lineage. Questions are output only as SHA-256.

Output discloses seed, commitment, deck hash, draw ID, and unique symbols drawn without replacement. Each symbol records position, project symbol ID, deck index, conventional name, upright orientation, fact ID, and source IDs.

The report uses only project-authored keywords plus position and sequence rules. It must not add reversals, person identity claims, hidden facts, or fixed predictions.
v0.2 adds `grand-tableau` to the auditable draw contract. `analyze_layout` returns adjacent pairs,
nine-card rows/columns/diagonals/mirrors, or Grand Tableau houses and optional significator
coordinates as appropriate. The source draw remains immutable.
