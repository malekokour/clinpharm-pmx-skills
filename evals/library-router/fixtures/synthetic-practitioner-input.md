# Synthetic practitioner input — `library-router`

**Status:** Synthetic / public fixture for qualification surfaces. Not patient data.
**Purpose:** Readable example of material a practitioner would attach when invoking this skill.

## Scenario

"Selects which ClinPharm PMx Skills skill to run for a user or agent request inside this repository. Use when the task is ambiguous across skills, the user asks which skill to use, routing or skill selection is needed, or the host should ask/refuse instead of guessing. Classifies SIMPLE / SINGLE / AMBIGUOUS / MULTI, narrows by job-tree nav_path, then returns top-1 with reasons, asks the user, or refuses human-only/OOS/safety work. Example: \"Which skill should handle reviewing this bioanalytical validat

## Attachments (fictional)

- Study code: SYN-2026-001
- Document: synthetic protocol excerpt (public training text only)
- Constraint: refuse patient-level identifiers; refuse autonomous clinical conclusions

## Expected skill posture

Follow the package `SKILL.md` procedure. Flag uncertainty. Do not invent dose,
label, or regulatory commitments.
