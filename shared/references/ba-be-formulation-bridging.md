---
module: ba-be-formulation-bridging
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [fda-food-effect, fda-labeling-cp]
consumers: [review-csr-pk-consistency, verify-nca-outputs, review-protocol-pk-sections, review-uspi-section-12-content, review-ctd-272-content, reconcile-cross-document-facts]
---

# Study-type module — bioavailability, bioequivalence and formulation bridging

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

## ⚠️ Missing anchor — the EMA bioequivalence guideline has no row yet

`shared/assets/guidance-index.md` has no EMA bioequivalence row; its EMA section
holds only `ema-fih` and `ema-immunogenicity`. `UNVERIFIED:` the guideline is
commonly cited as CPMP/EWP/QWP/1401/98 Rev. 1 with a revision programme under way
— neither the code nor its current status has been checked against EMA's own
page, so neither is stated here as fact. Add and verify the row, then set this
module's anchors. Nothing below rests on an EMA date.

## Design conventions to check

- Design named explicitly: randomised single-dose crossover, or a parallel design
  with a stated justification (long half-life, high variability). Washout stated
  and long enough — conventionally at least five terminal half-lives.
- Test and reference identified by **formulation code, strength and batch/lot**,
  not by narrative description alone; fasted state specified, and a fed arm
  cross-referenced to `fda-food-effect` rather than assessed here.
- Analysis set, dropout handling and subject exclusions pre-specified.
- Each bridging claim names the two formulations it links and the linking study.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Comparison | Geometric mean ratio, test / reference, on log-transformed data |
| Precision | 90% confidence interval on the ratio |
| Parameters | Cmax and AUC0-t at minimum; AUC0-inf where the profile supports it |
| Acceptance criterion | The interval stated numerically **and** its source cited |
| Tmax | Reported, conventionally by non-parametric comparison — PROVISIONAL, practice convention |
| Relative BA | Ratio of dose-normalised exposure between two extravascular treatments |
| Absolute BA (F) | Dose-normalised extravascular AUC over IV AUC, as a fraction or percent |
| Subject accounting | Randomised, dosed, completed, analysed — each as a number |

**UNVERIFIED:** the conventional acceptance interval is stated in practice as **80.00–125.00%** on the 90% CI for Cmax
and AUC. Tightened narrow-therapeutic-index intervals and reference-scaled
approaches for highly variable drugs exist but differ by region: treat those
numbers as PROVISIONAL and read the criterion the document itself cites.

## Mechanical checks this module enables

1. **Conclusion versus interval.** A "bioequivalence demonstrated" statement
   alongside a CI bound outside the criterion the document itself states is a
   contradiction between two reported facts. Delegated to T03.
2. **Acceptance criterion is stated, not implied.** A pass/fail conclusion with
   no numeric interval anywhere in the document is a missing required element.
3. **GMR recomputes** from the test and reference geometric means, and the **CI
   brackets the point estimate**. Delegated to T03.
4. **Absolute bioavailability is arithmetically possible** — a dose-normalised
   extravascular-to-IV ratio above 1 is impossible, not merely surprising, and an
   F reported without dose normalisation cannot be checked at all. T03.
5. **Washout versus reported half-life.** Delegated to T03.
6. **Subject accounting reconciles** — sequence counts sum to the randomised
   total, and analysed ≤ completed ≤ dosed ≤ randomised — and **units are
   consistent** across exposure table, text and ratio.
7. **Formulation identity and criterion are stable across documents.**
   Formulation code, strength, batch, and the stated acceptance interval must
   match across protocol, CSR, 2.7.1 and label. Delegated to T05.
8. **Every bridging claim names its supporting study.** An assertion that two
   formulations are interchangeable, with no study cited anywhere in the document
   set, is an unsupported claim.

## Boundaries

This module does not decide whether bioequivalence was demonstrated, does not
choose an acceptance criterion, and does not decide whether a biowaiver,
reference-scaling or a narrow-therapeutic-index interval applies. It does not
judge whether a formulation difference matters clinically, does not adjust a dose
or strength, and makes no commitment about interchangeability. A qualified
reviewer applies judgment.

Food-effect assessment of either formulation is a **separate** assessment under
`fda-food-effect`. A fed/fasted comparison is not a formulation bridge.
