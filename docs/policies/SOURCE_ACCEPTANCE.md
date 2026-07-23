# Source acceptance policy

## States

```text
proposed -> rights_checked -> extracted -> reviewed -> tested -> production
                    \-> rejected
```

`reference_only` is a terminal usage classification for sources that may inform research but cannot support production rules or content.

## Production gate

A source may support production knowledge only when:

- author, title, edition or version, retrieval date, and stable locator are recorded;
- license or permission scope is recorded and permits the intended use;
- commercial, derivative, translation, and image rights are individually classified;
- the exact file or snapshot has a SHA-256 hash when locally retained;
- a reviewer records an accepted rights decision;
- source quality and lineage relevance are recorded;
- precise page, section, verse, API version, or code revision locators are available.

Unknown rights never mean permission. A public URL is not by itself a reusable license.

## Source hierarchy

Prefer, in order:

1. official calculation standards and primary technical documentation;
2. public-domain primary texts with verified edition metadata;
3. permissively licensed datasets and implementations;
4. licensed modern scholarship and practitioner manuals;
5. independently collected and consented expert annotations.

Forums, unattributed summaries, model-generated prose, and copied competitor reports cannot be authoritative production sources.

## Personal and consultation data

Cases require consent or a documented lawful basis, data minimization, pseudonymization, retention limits, and a deletion mechanism. Public-figure birth data still requires provenance and reliability classification.
