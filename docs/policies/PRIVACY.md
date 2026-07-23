# Privacy review baseline

Privacy approval is deployment-specific. A repository policy cannot approve a product that has not
documented its actual collection, storage, access-control, observability, export, retention, and
deletion behavior.

The owner records that behavior in `common/deployment/DEPLOYMENT_PRIVACY.json`. Its schema keeps all
decision fields empty while status is `undecided`. A release requires status `configured`; storing
any user data additionally requires encryption at rest and in transit, role-based access, log
redaction, user export, and user deletion. A deployment that stores none of the declared data
classes must set primary and backup retention to zero.

Before a system's `privacy` sign-off can become `accepted`, the reviewer must verify:

- the minimum fields collected and the purpose of each field;
- whether questions, readings, names, birth dates, exact times, locations, or account identifiers
  are stored;
- retention duration, user export and deletion paths, backup expiry, and log redaction;
- access roles, encryption, processor locations, incident handling, and age restrictions;
- analytics and model-provider data flows, including opt-out and training-use settings;
- the deployed behavior against `SENSITIVE_BIRTH_DATA.md` when birth data is in scope.

Evidence must point to the reviewed deployment configuration or privacy assessment. A privacy
sign-off cannot be accepted while the deployment record is undecided. A pending placeholder is
honest; a generic automated approval is not.
