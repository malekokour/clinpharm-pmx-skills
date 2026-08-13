---
module: pd-and-biomarkers
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
anchors: [fda-biomarker-qualification, ich-e16, bestbiomarkers]
consumers: [review-model-analysis-deliverable, assess-development-plan-gaps, prepare-dose-justification-evidence]
---

# Reference — pharmacodynamics and biomarkers

Reference content only. It supplies criteria that exposure–response, biomarker and
dose-justification workflows apply.

**Why this is a reference and not a skill (PS-D030).** "Pharmacodynamics and biomarkers"
names a subject area, not a workflow: no single trigger, no single input, no single
artifact. The workflows that use it — biomarker fit-for-purpose, exposure–response,
target-engagement strategy — are separate skills.

## Design conventions to check

- **The biomarker's role is named.** Pharmacodynamic, predictive, prognostic,
  monitoring, safety and surrogate are different claims with different evidence
  requirements. A file that calls everything "a biomarker" hides the claim being made.
- **Fitness is for a stated purpose.** A marker adequate for dose-ranging may be
  inadequate to support an efficacy claim. Fit-for-purpose is not a property of the
  assay alone.
- **Baseline and its variability are characterised**, including diurnal, prandial and
  disease-activity effects, before any change from baseline is interpreted.
- **The direction and time course of the effect are specified**, and the sampling
  schedule can actually observe them. A marker sampled only at trough cannot describe a
  peak-driven effect.
- **Hysteresis is examined, not assumed absent.** A direct-effect model applied to an
  indirect response produces a confident and wrong potency estimate.
- **Placebo and disease progression are modelled** where the endpoint moves without
  drug.
- **Surrogacy is a claim requiring separate evidence** — that the marker predicts the
  clinical outcome, not merely that both respond to drug.

## Expected statements in a report

- What the marker is, what it measures mechanistically, and its role in this programme.
- The assay, its validation status, and its quantifiable range relative to observed
  values.
- Baseline distribution and within-subject variability.
- The exposure metric used and why it suits the effect's time course.
- The model used, whether hysteresis was assessed, and what was concluded.
- The purpose the marker is being claimed fit for, and the evidence for that purpose.
- Where a marker is used as a surrogate, the evidence linking it to outcome.

## Mechanical checks this module enables

- Every biomarker claim in a summary names its role and its intended purpose.
- Observed values fall inside the assay's validated range, or the exceedances are flagged.
- The sampling schedule contains time points capable of observing the stated time course.
- Exposure metrics used for pharmacodynamic analysis match those used elsewhere, or the
  difference is explained.
- A surrogate claim carries a citation to the surrogacy evidence, not only to the
  drug-effect evidence.

## Boundaries

This module supplies criteria. It does **not** decide whether a biomarker response is
clinically meaningful, accept a marker as a surrogate, qualify an assay, select a dose,
or judge model adequacy. Whether a change in a marker matters to a patient is a
judgment reserved for a qualified human.
