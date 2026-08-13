# Synthetic practitioner input — `review-submission-datasets-define-xml`

**Status:** Synthetic / public fixture for qualification surfaces. Not patient data.
**Purpose:** Readable example of material a practitioner would attach when invoking this skill.

## Scenario

"Reviews the submission-ready analysis datasets (SDTM, ADaM) and their define.xml metadata for clinical pharmacology content — verifying that PK concentration, parameter, and dose datasets carry the variables the analysis plan requires, that define.xml maps match the actual dataset structure, and that CDISC compliance is internally consistent. Use when asked to QC datasets before eCTD filing. Do not use for analysis plan review, for statistical analysis, or for CDISC implementation." allowed-too

## Attachments (fictional)

- Study code: SYN-2026-001
- Document: synthetic protocol excerpt (public training text only)
- Constraint: refuse patient-level identifiers; refuse autonomous clinical conclusions

## Expected skill posture

Follow the package `SKILL.md` procedure. Flag uncertainty. Do not invent dose,
label, or regulatory commitments.
