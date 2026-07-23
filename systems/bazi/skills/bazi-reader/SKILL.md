---
name: bazi-reader
description: Read untrusted Bazi JSON or explicit four-pillar text into an isolated import envelope. Use for 八字命盘导入, external chart ingestion, JSON exchange, four-pillar text parsing, or reader-to-validator handoff. Do not infer birth data, silently choose a day boundary or lineage, overwrite native calculations, parse screenshots/PDFs, or interpret imported pillars as verified.
---

# Bazi reader

1. Accept UTF-8 JSON or exactly four stem-branch pillars in year-month-day-hour order.
2. Run `scripts/run.py --input <file> --format json|four_pillar_text`.
3. Preserve the imported object under `imported_chart` with `native_facts_overwritten: false`.
4. Hand imported and native charts to `bazi-validator`; reader success is syntax, not calculation agreement.
5. Cite `BAZI-READER-IMPORT-001` and apply [references/safety.md](references/safety.md).

Reject OCR, images, prose with ambiguous pillar order, inferred time, and hidden third-party data.
