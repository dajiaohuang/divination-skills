---
name: qimen-hour
description: Calculate a bounded, auditable Shijia Zhuanpan Chaibu Qimen hour foundation with solar term, yin/yang dun, three-yuan ju, earth plate, hour xun, hidden Jia, and duty origin. Use for 奇门遁甲基础排盘, 拆补局 verification, or earth-plate replay. Do not call it a complete pan or infer 用神, directions, outcomes, or timing because heaven, rotating star/door, and spirit plates are absent.
---

# Qimen hour

Produce the v0.1 foundation and keep the incomplete boundary visible.

## Workflow

1. Require `--local-datetime` and an IANA `--timezone`; retain the chosen day boundary.
2. Run `scripts/run.py` and preserve normalized local, UTC, and China Standard Time.
3. Cite `QIMEN-CHAIBU-JU-001` for term, dun, yuan, and ju.
4. Cite `QIMEN-EARTH-PLATE-001` and `QIMEN-DUTY-ORIGIN-001` for the nine earth palaces and original duty location.
5. Enforce `QIMEN-FOUNDATION-BOUNDARY-001`: label the result `foundation_only`.
6. Never synthesize the absent heaven, rotating star/door, or spirit plates and never infer auspicious directions, 用神, events, outcomes, or timing.
7. Apply [references/safety.md](references/safety.md) to high-impact or third-party questions.

An external chart using 飞盘, 置闰, 阴盘, a different term boundary, or a different time convention belongs to another lineage and must not be silently compared.
