---
name: qimen-hour
description: Calculate a bounded, auditable Shijia Zhuanpan Chaibu Qimen hour chart with solar term, yin/yang dun, three-yuan ju, earth and heaven stems, nine stars, eight doors, eight spirits, 空亡、入墓、击刑 and 门迫 markers. Use for 奇门遁甲时盘、拆补局 verification, or full plate replay. Do not infer 用神, favorable directions, outcomes, or timing.
---

# Qimen hour

Produce the v0.3 project full plate while keeping calculation and judgment separate.

## Workflow

1. Require `--local-datetime` and an IANA `--timezone`; retain the chosen day boundary. Use civil time unless the caller explicitly selects apparent solar time with longitude.
2. Run `scripts/run.py` and preserve civil time, calculation time, solar correction, UTC, and China Standard Time.
3. Cite `QIMEN-CHAIBU-JU-001` for term, dun, yuan, and ju; cite `QIMEN-CLASSICAL-PLATE-PROVENANCE-001` for the shared classical vocabulary.
4. Cite `QIMEN-EARTH-PLATE-001`, `QIMEN-HEAVEN-STAR-PLATE-001`, and
   `QIMEN-DOOR-SPIRIT-PLATE-001` for plate facts.
5. Treat 空亡、入墓、击刑 and 门迫 as named facts under `QIMEN-STATE-MARKERS-001`,
   never as automatic outcomes.
6. Cite `QIMEN-TIME-APPARENT-SOLAR-001` only when that explicit time basis is selected.
7. Never infer auspicious directions, 用神, events, outcomes, or timing.
8. Apply [references/safety.md](references/safety.md) to high-impact or third-party questions.

An external chart using 飞盘, 置闰, 阴盘, a different term boundary, hosting policy, or time
convention belongs to another lineage and must not be silently compared.
