---
asset: human-review-gate-standards
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
consumers: [all skills]
---

# Human-review gate standards

The boilerplate every skill embeds. Ownership is the least standardized dimension
in this discipline, so the accountable owner is always a **configurable input**,
never an assumed organizational model.

## Owner-confirmation block

Every run opens by confirming, not assuming:

```text
Accountable owner for this review: ____________________  (role, not name)
Reviewer distinct from author?      yes / no / not applicable
Organizational model:               asset-level CP · study-level CP · CRO-managed · other
```

If the user cannot state the owner, proceed and mark every finding
`owner: UNCONFIRMED`. Never insert a default.

## The three named acts

1. **Adjudication** — a qualified reviewer decides, per finding, accepted or
   rejected-with-rationale. Never left implicit.
2. **Execution** — the document owner applies accepted corrections. The skill
   proposes; it never writes to the source document.
3. **Closure** — a named person verifies every item is dispositioned before the
   document is finalised, and signs the record.

## Disposition field

`open` is the only value a skill may write. `accepted`, `rejected-with-rationale`
and `closed` require a human. **A register arriving with items already closed is
malformed and must be treated as invalid.**

## Sign-off record

Every run emits it, with unset fields visibly unset:

| Act | Role | Name | Date |
|---|---|---|---|
| Owner confirmed | | | |
| Adjudicated | | | |
| Corrections executed | | | |
| Closure verified | | | |

A blank sign-off block on a finished document is itself a finding.
