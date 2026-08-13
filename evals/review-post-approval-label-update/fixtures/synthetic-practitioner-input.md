# Synthetic practitioner input — `review-post-approval-label-update`

**Status:** Synthetic / public fixture for qualification surfaces. Not patient data.
**Purpose:** Readable example of material a practitioner would attach when invoking this skill.

## Scenario

"Assesses a proposed change to an approved US label. It maps which other sections carry a fact the change alters and flags any the proposal omits, checks whether the proposed wording is stronger or weaker than the evidence behind it, and runs the check nobody runs - whether statements that are staying unchanged are still true afterwards, since new evidence can make an untouched sentence wrong. It also separates evidence-driven changes from changes required only because another section moved. Use

## Attachments (fictional)

- Study code: SYN-2026-001
- Document: synthetic protocol excerpt (public training text only)
- Constraint: refuse patient-level identifiers; refuse autonomous clinical conclusions

## Expected skill posture

Follow the package `SKILL.md` procedure. Flag uncertainty. Do not invent dose,
label, or regulatory commitments.
