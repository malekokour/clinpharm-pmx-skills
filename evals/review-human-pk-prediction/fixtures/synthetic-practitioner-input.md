# Synthetic practitioner input — `review-human-pk-prediction`

**Status:** Synthetic / public fixture for qualification surfaces. Not patient data.
**Purpose:** Readable example of material a practitioner would attach when invoking this skill.

## Scenario

Reviews a human pharmacokinetic prediction deliverable — allometric scaling, in vitro to in vivo extrapolation, or a PBPK model report — against the inputs it declares, the assumptions it states, and the qualification evidence it claims. Use this skill when someone asks to review, QC, or check the basis of a predicted human PK parameter, a first-in-human exposure projection, an IVIVE clearance estimate, or a PBPK model report — for example "does this PBPK report support the exposure it predicts"

## Attachments (fictional)

- Study code: SYN-2026-001
- Document: synthetic protocol excerpt (public training text only)
- Constraint: refuse patient-level identifiers; refuse autonomous clinical conclusions

## Expected skill posture

Follow the package `SKILL.md` procedure. Flag uncertainty. Do not invent dose,
label, or regulatory commitments.
