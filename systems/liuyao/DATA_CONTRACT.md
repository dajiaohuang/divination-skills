# Liuyao data contract v0.3

Input requires offset-free `local_datetime` and IANA `timezone`; it accepts optional question, replay seed, DST fold, `day_boundary` of `midnight` or `zi_initial`, `time_basis` of `civil` or `apparent_solar`, longitude, and latitude. The cast inherits the I Ching three-coin audit protocol and the calendar layer inherits Bazi time normalization.

Output contains primary/changed hexagrams, moving positions, eight-palace identity and stage, palace element, 世/应 positions, month commander, day pillar, 旬空, and six bottom-to-top lines. Each line retains coin facts plus 纳甲, line element, 六亲, 六神, role, void flag, fact ID, and sources.

v0.3 preserves `calculation_datetime`, `solar_time_correction`, and a source-backed `six_spirit_start`. Every structural line cites both the project specification and classical locator.

The v0.1 chart remains structural and does not select 用神. The optional v0.2 judgment contract
accepts a valid chart, one explicit `question_category`, and `include_timing`. It returns candidate
用神 line IDs, transparent structural strength components, moving/change 纳甲 relations, and
optional branch-only timing candidates. It does not return 吉凶, a promised event, or a date.
