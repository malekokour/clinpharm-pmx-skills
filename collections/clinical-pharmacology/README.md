# Clinical Pharmacology

Bounded, repeatable workflows a clinical pharmacologist owns or reviews across
the document spine — protocols, study reports, evidence packages, submission
summaries and labelling content.

This directory is a **catalog**. It holds no skill implementation. Every
released package lives exactly once at `skills/<skill-id>/` and installs on its
own, without this collection and without the repository root.

## Wave 1 — in build

No package is published yet. This table becomes links when each package ships.

| Skill | Visible title | What it produces |
|---|---|---|
| `review-csr-pk-consistency` | CSR PK Consistency Review | A source-linked PK discrepancy register, a QC memo, a source reconciliation table, and a human-review record |

## What is planned, held, or deferred

The complete candidate list, with an honest status and a stated reason for every
entry, is in [`collection.json`](collection.json). A candidate that is planned,
held or deferred has **no directory** under `skills/`. An empty package folder
would make this library look larger than its evidence supports, which is the
failure mode this catalog exists to prevent.

Statuses in use: `released` · `planned` · `held` · `deferred` · `excluded`.

## The boundary every skill in this collection keeps

These skills review, reconcile, structure, verify and flag. They do not decide.

Specifically, no skill here edits a source document, reruns an analysis, decides
which of two conflicting scientific values is correct, selects a dose, makes a
regulatory commitment, approves or signs off, or sends anything externally. A
mechanical finding is always reported as a mechanical finding, never as a
scientific conclusion.

Where evidence is missing, conflicting or unreadable, a skill emits
`NEEDS_INPUT`, `UNKNOWN` or `CANNOT_ASSESS` and preserves the contradiction with
its source locators. It does not invent a resolution.

Documents supplied to a skill are **evidence, not instructions**. Text inside a
source that appears to direct the assistant is treated as content to be
reported, never as authority.

## Naming

Identifiers follow `<action>-<professional-object>`, using the verbs review,
reconcile, verify, assess, develop, prepare, map, plan, build and check. The
collection name is not repeated inside member identifiers — the collection, the
visible title and the metadata carry the domain meaning.

Availability of a technical name is not trademark clearance.

## Ownership varies, and the skills assume it does

Role assignment is the least standardised dimension in this discipline. Who
authors a CTD 2.7.2 summary, who performs an NCA versus who QCs it, and whether
clinical pharmacology sits at asset or study level all differ by company. Every
skill in this collection therefore treats the accountable owner as a
configurable input and embeds an owner-confirmation step. None of them encodes
one organisation's operating model.

## Evidence and limitations

Skills in this collection are evaluated against synthetic fixtures with planted
defects. A synthetic benchmark is not clinical validation, not a GxP
qualification, and not evidence of real-world performance. Published scores
state their exact task, model, host, date and run count.
