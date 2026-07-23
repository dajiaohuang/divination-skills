# Clean-room implementation policy

## Purpose

External implementations may be studied to understand public interfaces, broad architecture, test categories, and interoperability requirements. Their protected expression, restricted prompts, proprietary datasets, and incompatible code must not leak into production project files.

## Rules

1. Keep external repositories under the ignored `references/upstream/` directory.
2. Register the URL, exact commit, retrieval date, license, additional terms, and intended use in `references/README.md` and a source manifest.
3. Do not copy or closely paraphrase external `SKILL.md`, prompts, reports, resource prose, rule compilations, or tests unless a reviewed license explicitly permits that use.
4. Do not import AGPL or otherwise reciprocal code into a differently licensed production component without a recorded architecture and licensing decision.
5. Reimplement from independent specifications, public-domain sources, permissively licensed sources, or newly authored requirements.
6. Preserve an evidence trail showing which accepted sources support each production rule and test.
7. When uncertain, mark the source `reference_only` or `pending`; do not promote derived content to production.

## Review record

Every pull request that adds external-derived behavior must answer:

- Which source manifests were used?
- Which exact facts or public interfaces were learned?
- Was any protected expression copied or adapted?
- Are implementation authors permitted to use each source for this purpose?
- Which tests demonstrate independent behavior?

## Vedic reference

`vedic-astro-skills` is currently reference-only. Its module separation and validation-first architecture may inform high-level design. Its instruction and resource text must not be copied into production Skills, and its code must not be incorporated without a separate AGPL compatibility decision.
