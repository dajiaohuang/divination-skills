# Numerology data contract v0.3

Input requires ISO `birth_date` and a `name`. Names are Unicode-normalized, accents are removed, and only Latin A–Z letters remain. The normalized name must contain a vowel and consonant; unsupported years and names without usable Latin letters fail closed.

Output records the normalized letters, selected name mapping, separate `date_masters` and `name_masters` policies, and immutable life-path, birthday, expression, soul-urge, personality, and maturity facts. Date-derived Life Path and Birthday always follow the project date policy and preserve 11/22/33. Chaldean name-derived and maturity facts reduce without master preservation. Each fact contains raw total, reduction steps, final value, master flag, project theme, fact ID, and source IDs.

v0.3 adds `computed_facts.name_trace` and `computed_facts.date_trace`. Chaldean name-derived and maturity facts include `SRC-NUMEROLOGY-CHEIRO-001`; date-only and Pythagorean facts cite the project policy.

The report presents themes as symbolic prompts, not measured traits. No automatic transliteration, compatibility, forecast, or identity inference is permitted.
v0.2 accepts optional `mapping` (`pythagorean` or `chaldean`) and optional `transliteration`.
`transliteration` is required when the original name contains non-Latin letters and rejected for
an already Latin name. The output records the exact mapping lineage and transliteration policy.
