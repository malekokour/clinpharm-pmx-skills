---
module: qt-assessment
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [ich-e14-s7b, fda-labeling-cp, cfr-201-57-c-13]
consumers: [review-csr-pk-consistency, review-protocol-pk-sections, review-uspi-section-12-content, assess-development-plan-gaps, review-ctd-272-content, reconcile-cross-document-facts]
---

# Study-type module — QT/QTc assessment

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

## Anchor scope — read before citing

`ich-e14-s7b` is the **E14/S7B Q&A set (February 2022)**. The numeric
conventions below originate in the **parent E14 guideline and earlier Q&A
revisions**, for which the index carries no row. **UNVERIFIED:** no criterion
below was checked against the ICH text. Cite the criterion, never a section or
Q&A number, until an `ich-e14` row exists and is verified.

## Design conventions to check

- **Approach declared** — dedicated thorough QT (TQT), or concentration-QTc
  (C-QTc) on early-phase ECGs. C-QTc output where the protocol specified a TQT
  is an internal mismatch.
- **Correction method stated and used consistently.** QTcF (Fridericia) is
  usual; a study-specific correction needs its derivation. QTcF in the tables
  with QTcB in the text is a findable defect.
- **ΔΔQTc defined** as baseline- and placebo-corrected, or against a stated
  comparator. Interchangeable "ΔQTc" / "ΔΔQTc" leaves the endpoint undefined.
- **Positive control** in a TQT — conventionally moxifloxacin — with an assay
  sensitivity statement. Absent from a C-QTc-only package it is not a gap,
  provided the substitution is stated.
- **Exposure coverage pre-specified**: the multiple of anticipated clinical Cmax
  covered, and how it is reached (dose, intrinsic/extrinsic factor, DDI arm).
- **PK and ECG time-matched**, pairing scheme stated, hysteresis addressed
  rather than assumed absent.
- **Model form pre-specified** for C-QTc — conventionally linear mixed-effects
  with the concentration slope as parameter of interest. PROVISIONAL: the linear
  default is practice convention (2018 C-QTc white paper), not a requirement.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Primary estimate | Predicted mean ΔΔQTcF at a **named** concentration, usually geometric mean Cmax of the high-exposure scenario |
| Precision | Two-sided 90% CI, equivalently the one-sided 95% upper bound |
| Threshold | **UNVERIFIED:** comparison against the commonly cited 10 ms upper bound, stated as a comparison, not a verdict. Confirm the value against the ICH text before use |
| Slope | Concentration–ΔΔQTc slope with its CI, and the intercept |
| Exposure claimed | The Cmax the estimate is anchored to, and the multiple of clinical Cmax it represents |
| Categorical | Outlier counts by conventional bins — absolute QTc >450 / >480 / >500 ms, change from baseline >30 / >60 ms. PROVISIONAL: confirm against E14 before citing as required |
| Assay sensitivity | Present for a TQT; explicitly waived with a stated basis otherwise |
| Waiver / no-TQT | Explicit statement of why no dedicated TQT was conducted, naming the substituting evidence |

## Mechanical checks this module enables

1. **Upper bound versus threshold.** Whether the reported bound sits above or
   below the applicable threshold is arithmetic. **UNVERIFIED:** confirm the threshold against the ICH text. Report the comparison, never a conclusion.
2. **CI brackets the point estimate**, and the one-sided 95% bound equals the
   upper limit of the two-sided 90% CI. Delegated to T03.
3. **Anchor concentration matches the PK section** for the same dose and
   population. Delegated to T05.
4. **Stated exposure multiple recomputes** from the anchor Cmax and the
   therapeutic Cmax the document itself reports. Delegated to T03.
5. **Correction method consistent** across protocol, tables, CSR text, 2.7.2 and
   label. Delegated to T05.
6. **Sign agreement.** A negative slope with a positive ΔΔQTc estimate at a
   concentration above the intercept contradicts itself.
7. **Categorical counts do not exceed the analysis population**; subgroup counts
   sum to the reported total.
8. **Positive control present where the design claims a TQT**, with an
   assay-sensitivity statement wherever one is reported.
9. **Waiver statement exists and names its evidence.** "A TQT study was not
   conducted" with no stated basis is a missing required element.
10. **Label QT text traces upstream** — a Section 12.2 statement with no
    corresponding estimate, CI and exposure. Delegated to T05.

## Boundaries

This module does not decide whether a QTc effect is clinically significant, does
not assess proarrhythmic risk, does not judge whether a waiver is acceptable,
and does not decide whether nonclinical data substitute adequately for a
positive control or a TQT. It selects no dose, drafts no label language, makes
no regulatory commitment. Cardiac safety beyond QTc — arrhythmia adjudication,
morphological ECG findings, holistic proarrhythmic assessment — is out of scope.
