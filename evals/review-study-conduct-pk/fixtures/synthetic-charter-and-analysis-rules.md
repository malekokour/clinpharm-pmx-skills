# SYNTHETIC — Study DNX-201, committee charter extract and interim analysis rules

> Fully synthetic. Fictional charter and analysis plan. This is the
> **completeness source and the rule source**: required content is judged against
> the list below, and numbers against the conventions below — never against
> generic expectations.

## Part A — Blinding status statement

Treatment assignments remain **blinded** to the study team, the study PK lead and
the reviewing clinical pharmacologist. A cohort package may contain **pooled
active-cohort summaries by dose level only**. It may not contain any
participant-level treatment attribution, and no check may reconstruct one.

## Part B — Data-cut baseline

| Value class | Authoritative extract | Cut date |
|---|---|---|
| PK concentrations and derived parameters | DNX-201-PK-EXT-07 | **2026-06-02** |
| Dosing and sampling records | DNX-201-ADMIN-EXT-04 | **2026-06-02** |
| Bioanalytical run status | DNX-201-BA-STATUS-03 | 2026-06-01 |

A package value that cannot be tied to the extract and cut above is
`unstated-provenance`. A package citing an earlier cut than the one declared here
is reporting from a superseded extract.

## Part C — Charter required-content list

A cohort package is complete only if each item below is present and labelled.

| # | Required content |
|---|---|
| C1 | Cohort dose level, number dosed, number with evaluable PK |
| C2 | Data-cut identifier and cut date for every value class in the package |
| C3 | Summary PK parameters by cohort: Cmax, AUC0-24, Tmax, terminal half-life, accumulation ratio |
| C4 | **Individual concentration-time profiles for each participant in the cohort** |
| C5 | Mean concentration-time profile, **labelled with the cohort, dose level and study day it represents** |
| C6 | **Bioanalytical run status, including any run pending at the data cut** |
| C7 | Sample accountability — missing and unquantifiable samples |
| C8 | **Sampling and dosing deviations, with actual-versus-nominal times stated wherever a sample is more than 20% off nominal** |
| C9 | Comparison against the previously reported exposures for each earlier cohort |
| C10 | Exposure-safety graphics — **excluded by this charter while the study remains blinded** |

C10 is an exclusion, not a requirement. A package that omits exposure-safety
graphics while blinded is conformant.

## Part D — Interim analysis plan v1.1, applicable conventions

| Rule | Convention |
|---|---|
| Concentration units | ng/mL |
| Exposure units | **ng·h/mL** |
| Clearance units | L/h |
| Reported precision | **three significant figures** |
| Reconciliation tolerance | 1.0% |
| Time basis for derivation | **Actual sampling times**, with any sample more than 20% off nominal disclosed in the package |
| BLQ convention | Reported as `BLQ`; not substituted with a numeric zero |
| Summary statistics | Arithmetic mean for Cmax, AUC and half-life; median with range for Tmax; n stated |

## Part E — Escalation rules (recorded, not applied)

The escalation decision is made by the committee under this charter. The
protocol's escalation rule section cites `ema-fih` and `fda-mrsd` as the anchors
its exposure caps derive from. A reviewer records that the package states the
applicable rule; the reviewer does **not** apply the rule, evaluate the exposure
against it, or state whether the cohort may escalate.
