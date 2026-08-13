severity_status: adjudicated
# Expert key — synthetic reference-safety fixture

> Do not provide this key to the evaluated model. All source documents are synthetic.

| ID | Severity | Detection | Source locator | Planted divergence |
|---|---|---|---|---|
| D1 | Major | script | CCSI §4.8 vs label §4.8 | `Neutropenia` appears only in CCSI v3.0. |
| D2 | Major | script | CCSI §4.8 vs label §4.8 | `Injection-site reaction` appears only in regional label v2.0. |
| D3 | Major | model | CCSI §4.8 vs label §4.8 | `Hepatotoxicity` and `Hepatic injury` are different supplied strings; preserve both, do not declare them equivalent. |
| D4 | Critical | model | PBRER §4.2 vs label header | PBRER declares CCSI v3.0; regional label is v2.0 effective 2026-05-15. The result is a version divergence, not a required-change determination. |
| D5 | Major | model | PBRER §4.2 | `Injection-site reaction` has no PBRER change-record entry; mark change-record status `CANNOT_ASSESS` rather than infer no change. |

## False-positive traps

1. `Hypersensitivity` occurs in both lists and is not divergent.
2. `QT prolongation` occurs in both lists; its wording update is documented in PBRER.
3. PBRER's CCSI declaration does not prove a filing obligation or required local action.

## Provisional severity boundary

Defect presence is deliberately planted. Severity is not practitioner-adjudicated;
the Critical denominator is therefore provisional. This key may support diagnostic
development only, never promotion to `released`.

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
