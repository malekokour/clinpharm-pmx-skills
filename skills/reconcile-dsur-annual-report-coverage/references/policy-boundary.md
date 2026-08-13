# Policy boundary and preserved unknowns

Load this reference for every run and copy both states into the output.

## Build-time source state

The accepted source package recorded the following on 2026-08-10:

| ID | State | Question | Source locator |
|---|---|---|---|
| `UNKNOWN_FINAL_RULE_STATUS` | `UNKNOWN` | Whether the proposed FDA DSUR rule had actually been finalized and made effective | P04:C09; Unified Agenda RIN 0910-AI37 was a timetable, not proof of publication |
| `UNKNOWN_DSUR_IN_LIEU_PRACTICE` | `UNKNOWN` | Whether FDA accepted an ICH E2F DSUR in lieu of a 21 CFR 312.33 annual report as current practice | P04:C11; the practice claim was uncorroborated by an opened primary FDA source |

These are preserved source states, not current-law conclusions. The accountable
regulatory owner must re-check live eCFR, Federal Register, FDA policy or
guidance, and the application-specific record at the time of use.

## Prohibited inference

Neither a gap-free calendar nor a cross-format overlap answers either policy
question. Never output `obligation satisfied`, `compliant`, `accepted in lieu`,
or an equivalent conclusion from period arithmetic.

## Source context

- P04:C08 recorded the 2022 notice of proposed rulemaking.
- P04:C10 recorded ICH E2F policy intent.
- P04:C12 established that the DSUR is a periodic safety-report vehicle and not
  a clinical-pharmacology-content repository.
- OD-40 requires RC-16 to surface the formal-text/practice tension and resolve
  neither side.
