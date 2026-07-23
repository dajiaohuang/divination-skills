---
name: western-reader
description: Read untrusted Western astrology JSON or position CSV into an isolated import envelope. Use for natal chart JSON ingestion, CSV position exchange, external chart inspection, or reader-to-validator handoff. Do not infer missing birth data, silently convert zodiac or house systems, overwrite native calculations, parse screenshots/PDFs, or treat import success as astronomical validation.
---

# Western reader

1. Accept UTF-8 JSON or CSV with `body` and `longitude_degrees`; optional `house`.
2. Run `scripts/run.py --input <file> --format json|csv`.
3. Preserve imports under `imported_chart` and set `native_facts_overwritten: false`.
4. Hand the import and a native chart to `western-validator`.
5. Cite `WESTERN-READER-IMPORT-001` and apply [references/safety.md](references/safety.md).

Reject OCR, images, PDFs, implicit tropical/sidereal conversion, and undeclared house-system repair.
