---
name: ziwei-reader
description: Read untrusted structured Ziwei JSON into an isolated import envelope and optionally compare it with project-native facts. Use for JSON chart ingestion, external chart exchange, import inspection, or reader-to-validator handoff. Accept JSON objects only; do not use OCR, screenshots, PDFs, infer missing fields, overwrite native calculations, or invoke iztro.
---

# Ziwei reader

Import a structured chart without granting it native-fact authority.

## Workflow

1. Require a UTF-8 JSON file containing `computed_facts.palaces`.
2. Run `scripts/run.py --input <file>`.
3. Return an import envelope with `native_facts_overwritten: false` and an untrusted-import warning.
4. If native comparison is needed, hand both objects to `ziwei-validator`.
5. Reject prose, OCR, images, PDFs, missing palace arrays, and implicit school conversion.
6. Apply [references/safety.md](references/safety.md).

Reader success means syntactic structural import only; it is not evidence that calculations match.
