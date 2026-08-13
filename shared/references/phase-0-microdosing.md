---
module: phase-0-microdosing
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
anchors: [ich-m3, fda-exploratory-ind, ema-microdose]
consumers: [assess-development-plan-gaps, review-human-pk-prediction, review-fih-dose-rationale]
---

# Reference — phase 0 and microdosing approaches

Reference content only. It supplies criteria for evaluating whether an exploratory
human study is appropriate and what its results can support.

**Why this is a reference and not a skill (PS-D030).** The decision of whether to run
one is made inside *Study versus model versus waiver decisions*, which is a skill. This
file is the criteria that decision reads.

## Design conventions to check

- **The question is stated before the design.** A microdose study answers "does human
  disposition resemble the prediction?" It does not answer "what dose works."
- **The dose meets the definition** — below the level expected to produce a
  pharmacological effect, and below a stated fraction of the predicted therapeutic dose,
  by the applicable regional definition.
- **The reduced nonclinical package matches the exploratory route claimed.** Different
  exploratory approaches carry different toxicology expectations, and choosing the study
  does not choose the lightest package by default.
- **Linearity between microdose and therapeutic dose is a hypothesis**, not a premise.
  Saturable absorption, saturable metabolism, and transporter involvement all break it,
  and the compounds most likely to break it are the ones most likely to be studied.
- **Analytical sensitivity is established first.** Accelerator mass spectrometry or
  equivalent sensitivity is often required; a microdose study with an assay that cannot
  quantify the profile produces nothing.
- **What the result will change is stated in advance.** If no prediction would be
  revised by either outcome, the study is not informative.

## Expected statements in a report

- The exploratory route used and the regional definition it satisfies.
- The dose administered, and its ratio to the predicted therapeutic dose.
- The nonclinical package supporting it.
- The analytical method and its lower limit of quantification relative to observed
  concentrations.
- The prediction being tested, and how the observed disposition compared.
- An explicit statement of whether linear extrapolation to therapeutic dose is supported
  by these data, and on what basis.
- What the result changed in the development plan.

## Mechanical checks this module enables

- The stated dose is consistent with the exploratory route claimed.
- Observed concentrations lie above the assay's lower limit of quantification.
- Any extrapolation from microdose to therapeutic dose is flagged and its assumption
  stated.
- The nonclinical package cited matches the route's requirements.
- Claims about human disposition cite the microdose study rather than the prediction it
  tested.

## Boundaries

This module supplies criteria. It does **not** decide whether to run an exploratory
study, judge whether linearity holds, accept a reduced nonclinical package, or select
or adjust any dose — including the first-in-human dose. It does **not** decide whether
a difference between predicted and observed disposition is clinically significant.
Whether microdose data justify a therapeutic-dose inference is a judgment reserved for
a qualified human.
