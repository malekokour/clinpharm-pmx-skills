# Interview and operating modes

Use this reference to run a short, adaptive interview rather than a fixed
questionnaire.

## Interview protocol

1. Establish the data boundary.
2. Inspect any existing context before asking repeat questions.
3. Ask up to four related questions per round.
4. Explain why each round matters.
5. Accept `skip`, `unknown`, or `not applicable`.
6. Confirm the round in a compact summary.
7. Stop when the requested output can be produced honestly.

Avoid asking for facts that can be derived safely from supplied, permitted
sources. Never infer mutable organizational facts from an old context file.

## CREATE

Use when there is no usable prior context.

### Minimum viable interview

1. What function or department best describes your work?
2. What is your role and level of responsibility?
3. What recurring decisions or deliverables do you own or support?
4. Which sources or people govern the work?
5. What information must not be used in this AI environment?
6. What makes an output immediately usable for you?

### Completion threshold

CREATE can finish when:

- the data boundary is clear;
- the user's function, responsibility, and intended use are known;
- source authority and human-review expectations are stated;
- at least one output preference is known; and
- missing items are labeled rather than invented.

## UPDATE

Use when the user supplies an existing professional context.

1. Ask what changed and the effective date.
2. Compare it with the relevant existing sections.
3. Classify proposed changes:
   `ADD`, `UPDATE`, `REMOVE`, `CONFLICT`, `STALE`, or `UNCHANGED`.
4. Ask only about decision-changing conflicts.
5. Produce the revised context and change summary.

Do not silently delete old constraints, reviewers, or authority rules.

## PROJECT

Use for one bounded project.

1. Confirm the project name or safe slug.
2. Inventory supplied sources.
3. Establish the source authority order.
4. Extract purpose, current status, deliverables, decisions, constraints, risks,
   and open questions.
5. Keep project-specific facts out of the stable professional constitution.
6. Produce a project capsule.

If more than five files or 2,000 lines are supplied, create a source manifest
and reading index before synthesis.

## REFRESH

Use to assess existing context quality.

Check:

- review date passed;
- mutable role or project facts lack a date;
- references no longer exist or are superseded;
- unresolved conflicts;
- completed projects still presented as active;
- tools or permissions treated as current without confirmation;
- ambiguous or missing human-review rules; and
- context that has grown too broad for practical reuse.

Return:

- `CURRENT`;
- `STALE`;
- `CONFLICTING`;
- `INCOMPLETE`; or
- `BLOCKED_BY_DATA_BOUNDARY`.

## EXPORT

Use when the user needs a self-contained attachment for one task or project.

1. Include the full Safety Kernel.
2. Select only relevant Professional Constitution sections.
3. Include one current Project Capsule.
4. Add a short task brief if the user supplied one.
5. Remove unrelated projects and unnecessary personal information.
6. Add "How to use this file" at the beginning.
7. Add sources, unknowns, and required reviewers at the end.

The exported working pack should be small enough to attach repeatedly and
complete enough that a new AI conversation does not need hidden prior context.

## Conflict questions

Use one of these patterns:

- "The project brief says X, while the analysis summary says Y. Which source
  governs this decision?"
- "Your previous context lists A as current, but the new file dates B later.
  Should B replace A or remain project-specific?"
- "This reviewer role changed. Is the change effective for all work or only this
  project?"

Do not ask the user to re-answer the entire interview because one field changed.
