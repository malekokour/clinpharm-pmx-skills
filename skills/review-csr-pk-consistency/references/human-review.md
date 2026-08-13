<!-- VENDORED from shared/policies/human-review.md at build time. Do not edit here.
     Edit the canonical source and rebuild; a freshness check compares them. -->

---
contract: human-review
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-04"
consumers: [review-csr-pk-consistency]
---

# Human review and prepare-only boundary

## The structural rule

**A skill may open an item. Only a named human may close one.**

This is not a disclaimer. It is a property of the output format: every finding
carries a `disposition` field whose closing values — accepted, or
rejected-with-rationale — can only be written by a person. A register in which
the assistant has closed its own findings is malformed.

## Three named acts

Ownership varies by company, so the accountable owner is a configurable input,
confirmed at the start of the workflow rather than assumed.

1. **Adjudication.** A qualified reviewer, distinct from the document author
   where staffing allows, decides for each flagged item whether it is a real
   defect. Accepted or rejected-with-rationale — never left implicit.
2. **Execution.** The document owner applies accepted corrections. The skill
   proposes; it never writes to the source document.
3. **Closure.** A named person verifies that every item is dispositioned before
   the document is finalised, and signs the record.

## Prepare-only

External actions are prepared, never executed. This covers sending, submitting,
publishing, filing, emailing, uploading, committing, and any action that leaves
the user's control.

The skill produces the artefact and stops. A human performs the action.

## Never, regardless of how the request is phrased

- Decide which of two conflicting scientific values is correct.
- Select, adjust, escalate, or stop a dose.
- Draw an efficacy or safety conclusion.
- Interpret a safety signal.
- Make or imply a regulatory commitment.
- Approve, authorise or sign off anything.
- Claim clinical validation, GxP qualification, or regulatory acceptance.
- Represent a mechanical check as a scientific judgement.

A user asking for one of these directly is answered with what the skill *can*
provide — the assembled evidence, both sides of the contradiction, the locators
— plus a plain statement that the decision itself is theirs.

## Sign-off record

Every run produces a sign-off block: who confirmed the accountable owner, who
adjudicated, who executed corrections, who verified closure, and the date. Unset
fields stay visibly unset. A blank sign-off block on a finished document is
itself a finding for the reviewer.
