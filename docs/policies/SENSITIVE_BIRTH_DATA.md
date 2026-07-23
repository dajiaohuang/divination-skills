# Sensitive birth-data policy

Birth dates, exact times, locations, coordinates, names, contact details, and chart histories can identify or profile a person. Treat them as sensitive user data even when local law does not assign a special statutory category.

## Default behavior

- Calculator and Skill invocations are stateless by default; persistence requires a separate, explicit user action.
- Do not place real birth data in source control, Golden Sets, fixtures, prompts, analytics events, exception traces, or model-training exports.
- Use synthetic inputs for tests. An anonymized case is not automatically safe if date, time, place, occupation, and life events can be recombined to identify someone.
- Do not use submitted data for model training, benchmarking, marketing, or practitioner review without purpose-specific consent.

## If product persistence is enabled

- Collect only fields required by the selected calculation and disclose the purpose before collection.
- Encrypt in transit and at rest; separate account identifiers from chart payloads; restrict access by role; audit reads and exports.
- Default retention is 30 days for saved draft calculations and zero days for unsaved calculations. A product may choose a shorter period, but extending it requires a documented purpose and explicit consent.
- Provide export and deletion controls. Complete deletion from primary stores within 7 days and from encrypted backups within the documented backup rotation, no longer than 35 days.
- Redact local times, coordinates, names, emails, IP addresses, and free-text life events from operational logs. Retain only coarse error codes and non-identifying performance measurements.
- Users may revoke future processing consent without losing access to already purchased static reports, subject to applicable law and the product's disclosed terms.

## Case review and feedback

Case collection requires an explicit consent record, a data-minimization review, and a re-identification risk rating. Separate pre-event claims from later outcomes with independent timestamps. Never edit a prior claim after an outcome is known; corrections are appended as a new version.

## Incident response

Follow `SECURITY.md`, suspend affected exports, preserve access logs, assess legal notification duties by jurisdiction, and notify affected users when required. A privacy reviewer must sign the Bazi release record before production promotion.
