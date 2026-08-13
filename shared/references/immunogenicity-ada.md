---
module: immunogenicity-ada
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [ema-immunogenicity, ich-m10, fda-bioanalytical, fda-labeling-cp]
consumers: [review-csr-pk-consistency, review-bioanalytical-report, review-uspi-section-12-content, review-ctd-272-content, reconcile-cross-document-facts, review-protocol-pk-sections, assess-development-plan-gaps]
---

# Study-type module — immunogenicity and anti-drug antibodies

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

## Anchor status

`ema-immunogenicity` (Immunogenicity Assessment of Therapeutic Proteins, final,
2017-05) is **research-sourced** in the guidance index and has not been
re-verified against EMA's own page. Verify it in pipeline stage 1 before this
module freezes. **No section or paragraph number of that guideline is cited
anywhere in this module** — none was verified, and an invented one would be
worse than its absence.

The assay-tiering and incidence-category vocabulary below is **industry
convention codified across guidance and white papers**, not a numbered
requirement of any single document. Treat every threshold as study-defined and
checkable against the study's own stated definition, never against a number
this module supplies.

## Design conventions to check

- **Tiered assay strategy stated**: screening → confirmatory (specificity) →
  characterisation (titer, and neutralising-antibody assay where applicable).
  A single-tier "ADA assay" with no confirmatory step is a findable gap.
- **Cut points stated** for screening and confirmatory tiers, with the method
  used to derive them. PROVISIONAL: 5% screening / 1% confirmatory false-positive
  targets are common practice, not a regulatory threshold — check the study's
  own stated value, do not impose these.
- **Drug tolerance and assay sensitivity reported**, with the sampling schedule
  positioned relative to drug washout so ADA sampling is interpretable.
- **Sampling schedule**: baseline (pre-first-dose) sample present, on-treatment
  samples, and post-treatment follow-up. Follow-up duration stated.
- **NAb assay** present where the product's mechanism makes neutralisation
  relevant, or its absence justified.
- **ADA-evaluable population defined**, and distinct from the PK and safety
  populations.
- **PK, PD, exposure-response and safety analyses pre-specify ADA status as a
  covariate or subgroup** rather than discovering it post hoc.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Denominator | Number of ADA-evaluable subjects, stated explicitly |
| Overall incidence | n / N with the percentage |
| Baseline status | Pre-existing ADA (positive at baseline) reported separately |
| Treatment-emergent | Baseline-negative → post-baseline-positive, as its own count |
| Treatment-boosted | Baseline-positive with a defined titer rise, as its own count |
| Persistence | Transient versus persistent, each with the study's own time definition (PROVISIONAL: a ≥16-week separation is a common convention, not a rule) |
| Titer | Reported as titer or dilution, with the reporting unit stated |
| Neutralising | NAb-positive count, with its denominator stated (ADA-positive subjects, or all evaluable — which one must be explicit) |
| PK impact | PK parameters presented by ADA status, with the parameter and the ADA category both named |
| Exposure-response | An explicit statement of how ADA-positive subjects were handled in the E-R analysis |
| Assay | Method, sensitivity, drug tolerance, and validation reference |

## Mechanical checks this module enables

1. **Incidence recomputes.** Stated percentage versus its own n / N. Delegated
   to T03.
2. **Denominator is stated at all.** A bare percentage with no N is an
   uncheckable number, and the most common defect in this section.
3. **Subset containment.** NAb-positive ≤ ADA-positive; treatment-emergent ≤
   total ADA-positive; any subgroup count ≤ its parent count. A violation is an
   arithmetic contradiction between two reported facts.
4. **Categories sum to the total.** Transient + persistent, and pre-existing +
   treatment-emergent, each reconcile with the stated overall count, or the
   report states why they do not.
5. **NAb denominator is named**, because the same NAb count over two different
   denominators yields two different percentages — a frequent cross-document
   divergence.
6. **Cross-document incidence agreement.** Same n, N and percentage in CSR,
   CTD 2.7.2, and label. Delegated to T05.
7. **Baseline sample exists** for every subject counted as treatment-emergent.
   A treatment-emergent classification without a baseline result is an absent
   required element.
8. **PK-by-ADA-status comparison is present** wherever the text asserts an
   effect (or absence of effect) of ADA on exposure. An assertion with no
   supporting stratified parameter is an unsupported claim.
9. **Assay sensitivity and drug tolerance are reported**, not merely referenced.
10. **Titer units are stated and consistent** across tables, text, and any
    figure axis.
11. **ADA follow-up duration versus half-life.** Sampling that ends before drug
    washout makes the post-treatment ADA count uninterpretable; flag as a
    stated-fact mismatch, not as a conclusion.
12. **Labelling location.** PROVISIONAL and requires verification: US labelling
    convention places ADA incidence under Adverse Reactions rather than the
    Clinical Pharmacology section. The subsection number was not verified — do
    not enforce one until it is checked against the current labelling rule.

## Boundaries

This module does not decide whether an observed ADA incidence is *clinically*
meaningful, does not judge whether a PK change in ADA-positive subjects warrants
a dose adjustment, and does not conclude that immunogenicity does or does not
confound an exposure-response relationship. It does not assess assay
suitability, approve a validation package, or determine whether a NAb assay was
required for a given product. It supplies criteria and finds arithmetic and
consistency defects; a qualified reviewer applies judgment.

Immunogenicity **safety** signals — hypersensitivity, infusion reactions, loss
of efficacy — are outside this module entirely.
