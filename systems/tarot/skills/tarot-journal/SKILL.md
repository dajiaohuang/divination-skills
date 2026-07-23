---
name: tarot-journal
description: Append an explicitly consented reflection from a validated Tarot draw to a local JSONL journal, or compute descriptive spread/card/orientation/tag counts. Use for 塔罗日记、抽牌记录、复盘 or personal draw statistics after $tarot-draw. Do not store raw questions, sync externally, score predictive accuracy, or infer causation.
---

# Tarot journal

Keep journaling local, consented, and descriptive.

## Workflow

1. Require a validated `$tarot-draw` JSON file.
2. Before writing, require the user to explicitly authorize local storage and pass
   `--consent-to-store`.
3. Put the reflection in a UTF-8 text file and run
   `scripts/journal.py append --journal ... --draw ... --reflection-file ... --consent-to-store`.
4. Run `scripts/journal.py stats --journal ...` for descriptive counts.
5. State the exact journal path and that the reflection may contain sensitive data.
6. Never store the raw question; verify `privacy.raw_question_stored=false`.
7. Never label frequencies as accuracy, synchronicity proof, causal evidence, or a forecast.

Do not upload, email, share, or otherwise move the journal without a separate explicit request.
