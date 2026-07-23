# Numerology data contract v0.1

Input requires ISO `birth_date` and a `name`. Names are Unicode-normalized, accents are removed, and only Latin A–Z letters remain. The normalized name must contain a vowel and consonant; unsupported years and names without usable Latin letters fail closed.

Output records the normalized letters, Pythagorean repeating 1–9 mapping, master numbers 11/22/33, and immutable life-path, birthday, expression, soul-urge, personality, and maturity facts. Each fact contains raw total, reduction steps, final value, master flag, project theme, fact ID, and source IDs.

The report presents themes as symbolic prompts, not measured traits. No automatic transliteration, compatibility, forecast, or identity inference is permitted.
v0.2 accepts optional `mapping` (`pythagorean` or `chaldean`) and optional `transliteration`.
`transliteration` is required when the original name contains non-Latin letters and rejected for
an already Latin name. The output records the exact mapping lineage and transliteration policy.
