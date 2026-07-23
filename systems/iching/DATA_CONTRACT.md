# I Ching data contract v0.1

Input accepts an optional question and optional 64-character replay seed. Unknown fields, invalid questions, and invalid seeds fail closed. Questions are retained only as SHA-256.

Output discloses the seed, commitment, cast ID, and algorithm. Six `computed_facts.lines` are ordered bottom-to-top and contain three coin values, total 6–9, polarity, moving flag, changed polarity, fact ID, and source IDs. Primary and changed hexagrams record binary lines, lower/upper trigrams, conventional King Wen number and name, and project themes.

The report layer cites mapping, moving-line, and structural-reflection rules. It reports all moving lines and does not invent classical judgment, image, or line text.
## Classical source layer v0.2

`build_classical_layer` accepts a valid cast, explicit `policy_id`, and optional edition IDs. It
returns selected logical passage units and edition-aware source locators. `text_included` is always
false. Edition differences remain `not_collated` until reviewed variant data exists.

Supported policies are `all-moving-lines-v0.2` and `zhu-xi-count-routing-v0.2`. Their selected
units are data, not predictions or interpretations.
