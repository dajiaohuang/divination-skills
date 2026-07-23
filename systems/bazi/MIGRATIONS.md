# Bazi data-contract migration policy

Current contract version: `0.1.0`.

- Calculator output is immutable for a given `schema_version`; breaking field changes require a new minor or major schema version.
- Additive optional fields may use a patch version only when older consumers remain valid.
- Every migration must be a deterministic, side-effect-free function with input/output schema tests, fixture hashes, and an explicit lossiness flag.
- The registry in `migrations/registry.json` must contain a continuous path from every supported stored version to the current version. Never rewrite stored user charts in place without an exportable backup.
- Skill package version and chart schema version are independent. The package manifest records both.
- Version support is maintained for at least the current and immediately preceding minor schema version; removal requires a changelog entry and user-visible export notice.

There is no migration in v0.1 because it is the first contract. The empty registry is intentional and tested.
