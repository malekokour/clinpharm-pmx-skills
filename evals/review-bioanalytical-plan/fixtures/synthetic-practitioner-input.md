# Synthetic practitioner input — `review-bioanalytical-plan`

**Status:** Synthetic / public fixture for qualification surfaces. Not patient data.
**Purpose:** Readable example of material a practitioner would attach when invoking this skill.

## Scenario

"Reviews a bioanalytical plan before samples are collected - which analytes will be measured, in what matrix, over what calibration range, and whether that range covers the concentrations the study will actually produce. It derives required analytes from the objectives before reading the plan, compares the lower limit against predicted terminal concentrations rather than peak, checks long-term stability against the interval to the last analysis rather than the first, and flags points where the p

## Attachments (fictional)

- Study code: SYN-2026-001
- Document: synthetic protocol excerpt (public training text only)
- Constraint: refuse patient-level identifiers; refuse autonomous clinical conclusions

## Expected skill posture

Follow the package `SKILL.md` procedure. Flag uncertainty. Do not invent dose,
label, or regulatory commitments.
