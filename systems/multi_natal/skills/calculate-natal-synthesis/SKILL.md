---
name: calculate-natal-synthesis
description: Calculate all repository birth-based systems from one birthday, local birth time, and confirmed birthplace, then produce an auditable non-merging synthesis across Bazi, Western natal astrology, Ziwei Dou Shu, Vedic Parashari/Jaimini/KP Stellar, and optional numerology. Use when a user asks for one combined reading, all natal charts at once, a multi-system birth report, 八字西占紫微印度占星一起排盘, 综合命盘, or cross-system natal comparison.
---

# Calculate natal synthesis

Run every birth-based calculator from one confirmed input and present the
systems independently before the structural crosswalk.

## Workflow

1. Collect:
   - Gregorian birth date;
   - offset-free local birth time;
   - birthplace name;
   - confirmed IANA time zone, longitude, and latitude;
   - explicit `calculation_gender` for Ziwei.
2. If the place name is ambiguous, resolve it with an available gazetteer or
   geocoder and confirm the selected place. Never guess coordinates, historical
   time zone, or calculation gender.
3. Read [references/input-and-synthesis.md](references/input-and-synthesis.md)
   before selecting policy overrides.
4. Use civil time by default. Apply apparent solar time to Bazi and Ziwei only
   when the user explicitly requests it.
5. Add `numerology` only when the user supplies a usable name and wants that
   system. Require user-supplied Latin transliteration for non-Latin names.
6. Write the confirmed input JSON and run:

   `python scripts/calculate.py input.json`

7. Present the result in this order:
   - normalized place, time zone, coordinates, UTC instant, and policies;
   - one independent section for each native system;
   - objective UTC and retained-tropical-coordinate checks;
   - the five structural synthesis axes;
   - limitations and unresolved policy choices.

## Synthesis rules

- Preserve every native chart and its lineage labels.
- Treat Western tropical and Vedic sidereal signs as different frames.
- Describe synthesis axes as side-by-side navigation, not votes.
- Do not assign an accuracy score or say repeated symbolism proves a claim.
- Cite the provided fact IDs and rule IDs for every structural statement.
- Keep KP labelled `stellar_identity_only`.
- If Bazi luck direction is absent, report that its luck cycles were omitted.

## Safety and privacy

- Treat birth data as sensitive personal data; do not persist it without
  explicit consent.
- Do not infer third-party thoughts, fidelity, health, legal outcomes,
  investment results, hiring decisions, or physical safety.
- Do not turn symbolic timing into guaranteed events.
- Do not repair an invalid or ambiguous input from memory.
