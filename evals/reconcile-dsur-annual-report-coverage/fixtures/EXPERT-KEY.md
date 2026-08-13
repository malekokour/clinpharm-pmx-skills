severity_status: adjudicated
# Expert key — synthetic DSUR and annual-report period fixture

> Answer key. Do not supply this file to a model under evaluation.

The seven report records are synthetic. Five are assessable; two are
deliberately unassessable. Defect presence and exact date arithmetic are fixed
by construction. Severity remains provisional until a clinical pharmacologist
and regulatory safety reviewer adjudicate it.

## Deterministic findings

| ID | Rule | Provisional severity | Report A | Report B | Inclusive affected dates |
|---|---|---|---|---|---|
| D1 | `same-kind-gap` | Critical | DSUR-2025-A | DSUR-2026-A | 2025-04-01 through 2025-04-02 |
| D2 | `same-kind-overlap` | Major | DSUR-2026-A | DSUR-2027-A | 2026-03-30 through 2026-03-31 |
| D3 | `same-kind-duplicate-period` | Major | IND-AR-2025-A | IND-AR-2025-B | 2024-06-15 through 2025-06-14 |
| D4 | `cross-format-potential-duplicate-coverage` | Major | DSUR-2025-A | IND-AR-2025-A | 2024-06-15 through 2025-03-31 |
| D5 | `cross-format-potential-duplicate-coverage` | Major | DSUR-2025-A | IND-AR-2025-B | 2024-06-15 through 2025-03-31 |
| D6 | `cross-format-potential-duplicate-coverage` | Major | DSUR-2026-A | IND-AR-2025-A | 2025-04-03 through 2025-06-14 |
| D7 | `cross-format-potential-duplicate-coverage` | Major | DSUR-2026-A | IND-AR-2025-B | 2025-04-03 through 2025-06-14 |

## Visible unassessable records

| ID | Required state | Reason |
|---|---|---|
| N1 | `NEEDS_INPUT` | `BROKEN-LOCATOR` has an empty locator |
| N2 | `NEEDS_INPUT` | `BAD-RANGE` has `period_end` before `period_start` |

## Preserved policy states

| ID | Required state |
|---|---|
| U1 | `UNKNOWN_FINAL_RULE_STATUS` remains `UNKNOWN` |
| U2 | `UNKNOWN_DSUR_IN_LIEU_PRACTICE` remains `UNKNOWN` |

## Exact denominators

| Measure | Expected |
|---|---:|
| Reports supplied | 7 |
| Reports assessable | 5 |
| Reports unassessable | 2 |
| Same-kind adjacency comparisons | 3 |
| Cross-format comparisons | 6 |
| Findings | 7 |
| Policy unknowns | 2 |

## Why severities are provisional

D1 is provisionally Critical because an uncovered period in a safety-reporting
calendar could materially affect a regulatory safety workflow. The remaining
date conflicts are provisionally Major because they require review before a
period register is relied upon. Neither rationale has been practitioner
adjudicated. Moving a severity changes the Critical denominator, so no model run
against this key can qualify the package until the key is frozen by the named
reviewers and the run is repeated.

## False-positive traps

1. `DSUR-2027-A` does not overlap either IND annual-report record.
2. The two-day gap is 2025-04-01 through 2025-04-02; 2025-03-31 is covered by
   the earlier DSUR and 2025-04-03 by the later DSUR.
3. The two-day overlap is 2026-03-30 through 2026-03-31; 2026-04-01 is covered
   only by `DSUR-2027-A` among assessable DSURs.
4. Different versions on `IND-AR-2025-A` and `IND-AR-2025-B` are provenance,
   not evidence that either period is legally required or sufficient.

## Adjudication boundary

Every finding preserves both report IDs and both locators and remains `open`.
Any output that determines a filing obligation, converts either policy unknown
to fact, characterises a safety conclusion, approves a report, or closes a
finding fails regardless of its date arithmetic.

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
