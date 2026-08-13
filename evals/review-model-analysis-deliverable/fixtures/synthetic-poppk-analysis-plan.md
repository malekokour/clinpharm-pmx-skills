# SYNTHETIC — Population pharmacokinetic analysis plan PMX-FZD-PLAN (v2.0)

> Fully synthetic. Fictional compound "fenzaridine", fictional study identifiers.
> No real compound, subject, sponsor or dataset. Generated for evaluation only.
>
> **This plan is the rule source for the review.** The objectives, the context of
> use, the planned analyses and the evaluation criteria below are read from here
> verbatim before any check runs.

**Analysis:** population pharmacokinetics of fenzaridine
**Plan version:** v2.0, signed 2025-10-07 (supersedes v1.0 of 2025-07-15)

---

## 1. Objectives

1. To develop a population pharmacokinetic model for fenzaridine from pooled
   Phase 1 and Phase 2 data.
2. To quantify the effect of body weight and of mild renal impairment on
   apparent clearance.
3. To simulate steady-state exposure at the regimens under consideration for
   Phase 3.

## 2. Decision context and context of use

The analysis supports the Phase 3 regimen decision. **The stated context of use
of this model is mild renal impairment and body weight only.** No other intrinsic
or extrinsic factor is within the context of use of this analysis, and no
conclusion outside it is supported by this plan.

## 3. Commissioning question

**Does renal function explain the observed variability in trough concentrations
in the Phase 2 study?**

## 4. Data and population

Pooled data from FZD-1001, FZD-1003 and FZD-2001.

**Exclusion rule.** Subjects with a baseline eGFR below 30 mL/min are excluded
from the analysis dataset. This exclusion is pre-specified and is not revisited
after the results are seen.

## 5. Planned analyses

- Base structural model selection between one- and two-compartment disposition
  with first-order absorption.
- Estimation by first-order conditional estimation with interaction (FOCE-I).
- Covariate screening restricted to body weight and eGFR.
- Simulation of steady-state exposure at the regimens carried forward.

## 6. Pre-stated evaluation criteria

Model evaluation is by **goodness-of-fit plots and a bootstrap of 500
replicates**. A parameter is considered adequately estimated when its bootstrap
95% confidence interval excludes zero.

No further evaluation criterion is pre-stated by this plan.

## 7. Reporting conventions

- Parameter estimates are reported to three significant figures.
- **Volume terms are reported in L**; clearance terms in L/h.
- Numeric reconciliation tolerance between the report body and its appendices:
  **1%**.

## 8. Deviations

Any departure from this plan is recorded in the deviation log with a
justification, before the report is finalised.
