---
asset: review-rubric-library
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
consumers: [review-bioanalytical-report, verify-nca-outputs, review-model-analysis-deliverable, review-protocol-pk-sections, review-ctd-272-content]
---

# Review rubric library

Content-conformance rubrics shared across skills. A skill **consumes** a rubric;
it never re-implements one. This is why `review-bioanalytical-report` has no
private copy of the ICH M10 checks.

## ICH M10 — bioanalytical method validation

Consumed by `review-bioanalytical-report` (primary) and `verify-nca-outputs`
(cross-reference only). Anchors: `ich-m10`, `fda-bioanalytical`.

| Element | Present | Adequate | Locator |
|---|---|---|---|
| Method description and analyte definition | | | |
| Calibration curve range and model | | | |
| Accuracy and precision, within and between run | | | |
| Selectivity and specificity | | | |
| Matrix effect and recovery | | | |
| Carryover assessment | | | |
| Dilution integrity | | | |
| Stability: stock, short-term, long-term, freeze-thaw, processed sample | | | |
| Incurred sample reanalysis, with acceptance outcome | | | |
| Chromatogram inclusion per the applicable requirement | | | |
| Deviations and their impact assessment | | | |

**Boundary.** A rubric records presence and adequacy against the standard. It
never re-validates the method and never certifies GLP or GCP compliance.

## Exposure–response — `fda-exposure-response`

Question framed · population and dose range · exposure metric justified ·
model form stated with assumptions · uncertainty characterised · alternatives
considered · conclusion traceable to the analysis · limitations stated.

## PBPK format and content — `fda-pbpk`

Purpose and context of use · model structure and parameters with sources ·
verification against observed data · sensitivity analysis · simulation design ·
results with uncertainty · conclusions bounded by the stated context of use.

## Model analysis plan / report — `ich-m15`

Objective and decision context · data and its provenance · model development
strategy · evaluation criteria pre-stated · results · conclusions traceable ·
deviations from the plan documented and justified.

**Boundary for all three.** These rubrics assess whether an analysis is
*reported* completely and consistently. They never re-fit, re-run or critique
model structure — that is pharmacometrics execution, which is out of scope.
