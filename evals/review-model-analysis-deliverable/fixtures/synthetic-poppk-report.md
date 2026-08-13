# SYNTHETIC — Population pharmacokinetic analysis report PMX-FZD-RPT (v1.0)

> Fully synthetic. Generated for evaluation only. This is the deliverable under
> review.

**Analysis:** population pharmacokinetics of fenzaridine
**Report version:** v1.0, dated 2026-03-19
**Analysis plan referenced by this report:** PMX-FZD-PLAN v1.0

---

## 1. Objectives

To develop a population pharmacokinetic model for fenzaridine, to quantify the
effect of body weight and renal function on apparent clearance, and to simulate
steady-state exposure at the regimens under consideration.

## 2. Data

Pooled data from FZD-1001, FZD-1003 and FZD-2001.

All subjects with evaluable pharmacokinetic data were included in the analysis
dataset. Dataset composition is given in Appendix C.

## 3. Methods

A two-compartment model with first-order absorption described the data.
Estimation was performed using **the SAEM algorithm**.

The assumption of time-invariant clearance was not tested.

Model evaluation used goodness-of-fit plots, a visual predictive check, and a
bootstrap of **1000 replicates**.

The pre-specified acceptance criterion for the visual predictive check was that
**≥90% of observations fall within the 90% prediction interval**. This criterion
was met.

## 4. Results

### 4.1 Parameter estimates

Apparent clearance was estimated at **CL/F 12.4 L/h** with between-subject
variability of 28% CV. Apparent volume of distribution of the central compartment
was 214 L with between-subject variability of 42% CV. Shrinkage on the absorption
rate constant was 24%.

Full parameter estimates are given in Appendix C, Table C-1.

### 4.2 Covariates

Body weight was retained on apparent clearance. eGFR was retained on apparent
clearance, with a 19% lower clearance at the lower bound of the observed eGFR
range relative to the reference subject. The covariate relationships are shown in
Appendix C, Table C-4.

### 4.3 Simulations

Steady-state exposure was simulated at the regimens carried forward. Simulated
regimens and their outputs are listed in Appendix C.

## 5. Conclusions

1. A two-compartment model with first-order absorption adequately described
   fenzaridine pharmacokinetics.
2. Body weight and eGFR were retained as covariates on apparent clearance.
3. Exposure at **200 mg once daily** is comparable to that at 150 mg once daily
   in subjects over 100 kg, and the 200 mg regimen is therefore supported for
   Phase 3 in that subgroup.
4. No dose adjustment is required for subjects with moderate hepatic impairment.

## 6. Limitations

The analysis pooled studies of differing design, and the Phase 2 sampling was
sparse. The eGFR range represented in the dataset does not extend to severe
impairment.
