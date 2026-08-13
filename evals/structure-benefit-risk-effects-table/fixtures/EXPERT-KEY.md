severity_status: adjudicated
# Expert key — synthetic effects-table fixture SVT-101

> Do not provide this key to the evaluated model. All source documents are synthetic.

| ID | Severity | Detection | Source locator | Planted structural defect |
|---|---|---|---|---|
| D1 | Major | model | Draft E-02 vs source E-02 | E-02 states `UNKNOWN` instead of `risk difference 5 percentage points; 95% CI 1 to 9`. |
| D2 | Major | script | Draft E-03 vs source E-03 | E-03 locator is `NEEDS_INPUT` instead of `Table 7`. |
| D3 | Major | script/model | Draft E-04 vs source E-04 | E-04 population is `NEEDS_INPUT` instead of `ITT`. |
| D4 | Critical | model | Draft E-04 vs source E-04 | E-04 cites `SVT-101 CSR v1.0`; source is `SVT-101 CSR v2.0`. |
| D5 | Major | model | Draft E-05 | E-05 has no matching effect in the supplied source register and must be reported as untraceable. |

## False-positive traps

1. E-01 is complete and matches source wording exactly.
2. E-03's effect estimate `1.08` and interval `90% CI 0.96 to 1.21` are correct.
3. E-04's negative value is an effect as written, not a direction for a conclusion.

## Provisional severity boundary

Defect presence is deliberately planted. Severity is not practitioner-adjudicated;
the Critical denominator is therefore provisional. This key may support diagnostic
development only, never promotion to `released`.

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
