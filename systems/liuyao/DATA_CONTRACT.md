# Liuyao data contract v0.1

Input requires offset-free `local_datetime` and IANA `timezone`; it accepts optional question, replay seed, DST fold, and `day_boundary` of `midnight` or `zi_initial`. The cast inherits the I Ching three-coin audit protocol and the calendar layer inherits Bazi time normalization.

Output contains primary/changed hexagrams, moving positions, eight-palace identity and stage, palace element, 世/应 positions, month commander, day pillar, 旬空, and six bottom-to-top lines. Each line retains coin facts plus 纳甲, line element, 六亲, 六神, role, void flag, fact ID, and sources.

v0.1 does not select 用神 or calculate 旺衰, 伏神, advanced change relations, 吉凶, or 应期. The report must keep that boundary explicit.
