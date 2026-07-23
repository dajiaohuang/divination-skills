# Tarot data contract v0.3

Input fields are `spread`, optional `question`, optional 64-character `seed_hex`, and boolean `allow_reversals`. Supported spreads are `single`, `situation-challenge-guidance`, and `option-a-option-b-focus`. Questions are represented in output only by SHA-256.

The engine returns the normalized spread and reversal policy, a disclosed replay seed, seed commitment, deck hash, draw ID, and immutable `computed_facts.cards`. Each card records position, project card ID, deck index, conventional name, orientation, fact ID, and source IDs. Drawing is without replacement using SHA-256 counter rejection sampling.

v0.3 requires `arcana`, `deck_index`, `rank`, `suit`, `element`, and `identity_lineage=rws-identity-v0.3` on each card fact, with both project and Waite source IDs.

`derived_findings` and `narrative` are added only by the report layer. They must preserve all draw facts and cite orientation, position, and sequence rules. Invalid spreads, seeds, or policy types fail closed.
v0.2 supports `elemental-five`, `relationship-six`, `horseshoe-seven`, and `celtic-cross` in
addition to the existing layouts. Combination output contains adjacent arcana/element/suit/rank
relations and aggregate counts without causal interpretation.

Journal entries require explicit `consent_to_store=true`. They retain draw ID, question hash,
spread, card IDs, positions, orientations, user reflection, and tags; raw questions are never
stored. Statistics return counts only.
