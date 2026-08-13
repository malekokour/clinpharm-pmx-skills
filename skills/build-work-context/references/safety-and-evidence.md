# Safety and evidence contract

Read this reference before processing user-supplied project material.

## Data profiles

### PUBLIC_OR_SYNTHETIC

The content is public, fictional, or explicitly redistributable.

- It may be used in public examples when licensing permits.
- Preserve source links and distinguish synthetic values.
- Do not infer that public availability makes a source authoritative.

### INTERNAL_APPROVED

The user confirms that the current AI environment is approved for the exact
material and task.

- Use only the minimum content needed.
- Do not transfer the material to another service, agent, connector, or tool
  unless that destination is also approved.
- Avoid reproducing confidential bodies in logs, filenames, or summaries.
- Keep external communication prepare-only.

### RESTRICTED_DO_NOT_PROCESS

The material includes patient-level data, credentials, sponsor-confidential
content, proprietary submissions, or content not approved for the current AI
environment.

- Stop before reading or transforming it.
- Explain the boundary without asking the user to expose more details.
- Offer a synthetic example, abstract schema, or locally approved route.

### UNKNOWN

The environment or material classification is unclear.

- Ask one short question that will resolve the boundary.
- Do not inspect the source while waiting.

## Authority and evidence

Use this claim discipline:

- `SOURCE FACT`: directly stated in an identified source.
- `USER CONFIRMED`: explicitly provided or confirmed by the user.
- `INFERENCE`: reasoned interpretation from facts.
- `ASSUMPTION`: temporary premise requiring confirmation.
- `UNKNOWN`: missing information.
- `CONFLICT`: incompatible statements not yet resolved.

For each consequential project claim, retain:

- the source filename or user confirmation;
- the relevant date or version;
- whether the claim is direct or inferred;
- contradiction status; and
- the human reviewer or decision owner when known.

Do not use majority vote to resolve incompatible sources. Prefer the user's
declared authority order, then current approved primary sources. Keep a conflict
visible when authority is unclear.

## External actions

Generating a draft does not authorize:

- sending or posting;
- submission or approval;
- account, permission, or connector changes;
- purchase or payment;
- medical, dosing, safety, or regulatory decisions; or
- deletion or irreversible changes.

State the required owner action and leave external execution to the user unless
the current conversation separately authorizes it.

## Human review

The working pack must identify which outputs require review by qualified roles.
Do not invent a named reviewer. Use a role such as `clinical pharmacology lead`
or `regulatory reviewer` until the user confirms a person.

## Sensitive-detail minimization

Prefer:

- role labels over personal names;
- project codes over proprietary asset names;
- aggregate or synthetic examples over raw records;
- source locators over copied document bodies; and
- explicit exclusions over vague claims of safety.
