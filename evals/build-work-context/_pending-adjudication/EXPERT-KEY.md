severity_status: provisional
# Expert key — synthetic context-conflict fixture TVX-201

> **Answer key. Do not supply this to the model under evaluation.**
>
> 12 planted defects. Every one is discoverable from the four `planted-*`
> documents alone; none requires outside knowledge.

## What a "defect" is for this skill

`build-work-context` is a **context-building utility, not a document reviewer**.
It does not QC a clinical document, and it has no clinical finding classes. The
defects planted here are therefore **inconsistencies between a supplied existing
professional context and the new project documents** — precisely the material the
skill's "Reconcile updates without silent overwrite" step exists to catch.

A run passes a defect when it **surfaces the inconsistency and keeps both sides
visible**, classified `CONFLICT` or `STALE` as appropriate. Silently adopting the
project document's version, or silently keeping the old one, is a miss even where
the chosen side happens to be the sensible one.

## The documents

| File | Role |
|---|---|
| `planted-existing-context.md` | The existing professional context, version 3.0 — the confirmed baseline |
| `planted-project-brief.md` | New project document: roles, status, deliverables, sources |
| `planted-project-status-note.md` | New project document, dated later than the brief |
| `planted-source-manifest.md` | New project document: the complete source manifest, the team's authority order, its glossary and a handling note |

The five pre-existing fixtures in this directory (`update-*`, `stale-context.md`,
`prompt-injection-source.md`, `unsupported-docx-host.md`) belong to other cases
and are not part of this fixture.

## Severity rubric used here

This skill ships no severity table, so one is stated rather than assumed:

| Severity | Definition |
|---|---|
| Critical | Would make the produced context assert something false about **authority, permission, or the data boundary** — what the holder may decide, what may be sent, which source wins, or where material may be processed |
| Major | Would make the context materially wrong about **the work** — status, milestone, deliverable, terminology that carries meaning, or the source set — without changing a permission |
| Minor | Terminology or metadata hygiene that a reader would notice but not act on |

## The twelve

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | role-contradiction | **Critical** | either | Brief roles table vs context decision rights | The brief gives the context holder **approval authority for the PK analysis plan**. The context states the holder **recommends; does not approve analysis plans**, with approval escalating to the department head |
| D2 | deliverable-conflict | Major | script | Brief deliverables vs context deliverables | Brief specifies a **weekly exposure summary**; the context records a **monthly synthetic PK status summary** |
| D3 | stale-status | Major | script | Brief status vs status note | Brief states **protocol finalised**; the later status note states the protocol is **still in draft** with Amendment 1 under discussion |
| D4 | stale-milestone | Major | script | Brief status vs status note | Brief plans first patient in for **2026-09-01**; the status note moves it to **2026-11-01** |
| D5 | unlisted-source | Major | model | Status note vs source manifest | The status note bases its exposure assumptions on **the TVX-201 PBPK memo (2026-06-14)**, which does not appear in the manifest. The manifest states **This manifest is complete.** |
| D6 | approval-rule-conflict | **Critical** | either | Status note vs context external-action rule | The status note records that the exposure summary **was shared with the external CRO**, with no approval record attached. The context states **Every external send requires named owner approval** |
| D7 | authority-conflict | **Critical** | script | Manifest authority order vs context hierarchy | Manifest asserts **Interim listings take precedence over the signed analysis plan**. The context states **Signed analysis plan outranks interim listings** |
| D8 | terminology-conflict | Major | script | Glossary vs context terminology | Glossary defines "data cut" as **the date the database was locked for the study**; the context defines it as **the timestamped extract used for an interim analysis**. Two different objects behind one term |
| D9 | terminology-conflict | Minor | script | Glossary vs context terminology | Glossary defines "working pack" as **the printed handout circulated before a committee meeting**; the context defines it as **a self-contained context file assembled for one project** |
| D10 | data-boundary-conflict | **Critical** | script | Manifest handling note vs context permitted environments | Handling note says the pack may be processed in **any general-purpose assistant**. The context states **no public consumer chat tool may receive project material** |
| D11 | stale-unknown | Minor | script | Context known unknowns vs brief roles table | The context still carries **Whether the sponsor's modelling platform is approved for this program** as an open unknown. The brief states the platform **which is approved for TVX-201**. The unknown is resolved and the context has not been updated |
| D12 | unlisted-source | Major | model | Brief deliverables vs source manifest | The brief draws on **the 2026-05 dose-justification memo**, which does not appear in the manifest and was not supplied. Same class as D5, a different instance |

## Counts

| | |
|---|---|
| Total | 12 |
| Critical / Major / Minor | **4 / 6 / 2** |
| Script-detectable | 8 (D2, D3, D4, D7, D8, D9, D10, D11) |
| Script or model (`either`) | 2 (D1, D6) |
| Model-only | 2 (D5, D12) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **4(5) + 6(3) + 2(1) = 40**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

Every defect above was planted deliberately by the fixture author. That a defect
is present, and where, is a **fact** — confirmable by reading the four documents,
and a run that fails to surface one has genuinely missed something.

The **severity column has not been adjudicated by a practitioner.** Neither has
the severity rubric above, which was written for this fixture rather than taken
from the skill — the skill ships none. It must not be used to promote this
package to `released`.

The reason is arithmetic. A promotion gate turns on the **Critical denominator** —
`missed_critical_allowed: 0` means one missed Critical fails the run outright.
The severity column is what fixes that denominator, so moving a single defect
between Critical and Major decides whether the same set of model outputs passes.

The arguable rows, flagged rather than left for a reader to find:

- **D6** is marked Critical because an external send without the recorded
  approval is a breach of a stated rule, not a discrepancy about it. A reviewer
  who reads the status note as reporting a past event outside this context's
  control — something to record rather than to treat as a live permission
  conflict — would mark it Major.
- **D8** is marked Major because "data cut" carries a real operational meaning
  and the two definitions denote different objects. A reviewer who expects any
  downstream reconciliation to be run against the wrong extract because of it
  would mark it Critical.
- **D1** could be read as Major rather than Critical if the brief is treated as
  announcing a genuine role change rather than as contradicting a confirmed fact.
  The skill's own contract resolves the *handling* — it is a `CONFLICT` until the
  owner confirms — but not the severity.

Until a practitioner rules on the column, `severity_status` stays `provisional`.

> **Note for the repository gate.** `validate_repo.py` fails a package whose
> status is `released` while its expert key is `provisional`, and
> `build-work-context` is currently `released`. That collision is real and is
> owner-gated: it resolves either by a practitioner adjudicating this column, or
> by the package's status moving to `built` with an `evidence_gap`. It is
> recorded here rather than worked around, because working around it would mean
> asserting an adjudication that has not happened.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **Protocol TVX-201 v2.0.** The brief and the manifest name the same document
   at the same version. Consistent, not a conflict.
2. **The status note being dated after the brief.** A later date is not by itself
   a contradiction. What conflicts is the status *text* (D3) and the milestone
   (D4), not the existence of a newer document.
3. **The context's `version: "3.0"` against "Protocol TVX-201 v2.0".** Different
   documents with unrelated version numbers. Comparing them is a category error.
4. **The definition of "capsule".** The glossary and the context define it
   identically. An identical definition restated is not a terminology conflict.
5. **"Study statistician" named by role only.** The contract asks for
   stakeholders by role. A role without a personal name is the intended shape,
   not a completeness gap — and asking for the name would be asking for personal
   data the workflow does not need.
6. **"No participant-level data leaves the approved environment"** in the brief.
   That agrees with the context. The data-boundary conflict is the manifest's
   handling note (D10), not the brief's constraint.

## Handling boundary

For every defect above, the expected behaviour is to classify it `CONFLICT` or
`STALE`, **keep both statements visible with their sources**, and leave it
unresolved pending owner confirmation. Specifically:

- The context version is **not** incremented as though the conflicts were
  resolved.
- A `Context-Change-Summary.md` is produced and lists them.
- The two unlisted sources (D5, D12) are recorded as cited-but-not-supplied, not
  assumed to exist and not summarised from their titles.
- No output states that the project pack may be processed in a general-purpose
  assistant, and no output treats the CRO send as approved.
