---
module: pediatric-pk-extrapolation
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [ich-e11a]
consumers: [review-protocol-pk-sections, assess-development-plan-gaps, prepare-dose-justification-evidence, review-ctd-272-content, reconcile-cross-document-facts, review-csr-pk-consistency]
---

# Study-type module — pediatric PK extrapolation

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

## Anchor status — read before relying on a date

**UNVERIFIED:** `ich-e11a` sits on a `research-sourced` row in `guidance-index.md`
(Step 4, 2024-08-21), unchecked against ICH's own page — re-verify in pipeline
stage 1 before citing it. The **age-group taxonomy** (preterm newborn, term
newborn, infant and toddler, child, adolescent) comes from **ICH E11 / E11(R1)**,
which has **no index row at all**; group *boundaries* are deliberately not
reproduced here. Check that group *labels* are consistent across documents; never
check a boundary against a remembered number.

## Design conventions to check

- **Extrapolation concept** and **extrapolation plan** named as distinct items,
  with the **source population** identified (adults, an older pediatric group, or
  another indication) and the **degree of extrapolation** stated in words — full,
  partial, none — identically in every document that mentions it.
- Each **assumption** a discrete listed statement, not implicit in prose. Present
  or absent: similarity of disease, similarity of response to treatment, a stated
  exposure–response relationship in the source population.
- **PK matching target** pre-specified — which parameter (AUC, Cmax, Ctrough,
  other), against which reference value, under what acceptance criterion.
- **Age groups to be enrolled** listed with planned sample sizes, every group in
  the plan present in the enrolment table.
- **Sampling strategy** stated — dense, sparse with population PK, or both — and
  consistent with the parameter matched. A Cmax target supported only by trough
  samples is a mismatch between the stated target and the stated method.
- A **confirmatory or iterative step** described: what data would revise the
  extrapolation once collected.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Extrapolation degree | Full, partial, or none, in words |
| Source population | Named study or pooled dataset, with an identifier |
| Assumptions | Enumerated list, each stated individually |
| Matching parameter | Named, with the acceptance criterion it is judged against |
| Reference value | Source-population value, named parameter, units, dispersion |
| Achieved exposure | Per age group, geometric mean and dispersion, same units |
| Comparison | Ratio or percentage of the reference, per age group |
| Age-group coverage | Every planned group reported, or its absence stated |
| Dosing rule | Explicit mg/kg, mg/m², or banded rule, with the bands stated |
| Conclusion | Whether the pre-specified criterion was met, stated as a fact |

## Mechanical checks this module enables

1. **Every assumption used in the conclusion appears in the assumption list.**
2. **Extrapolation degree identical across documents.** T05 — protocol, CSR and
   Module 2.7.2 disagreeing is a contradiction.
3. **Matching parameter consistent with the sampling strategy** described.
4. **Units consistent** between the reference value and the pediatric value
   compared against it. T03.
5. **Exposure ratio recomputes** from the reported values. T03; a ratio that will
   not reproduce is a contradiction between two reported numbers.
6. **Every planned age group accounted for** — a group with no results row and no
   stated reason is an absent required element.
7. **Dosing-rule arithmetic reproducible** at the stated band edges. T03.
8. **Conclusion judged against the pre-specified criterion.** A criterion restated
   more loosely in the conclusion than in the methods is a contradiction.

## Boundaries

This module does not decide whether extrapolation is scientifically justified,
whether an assumption is true, which age groups must be studied, or what the
pediatric dose should be, and makes no regulatory commitment. It checks only that
required elements are present, internally consistent and arithmetically
reproducible. A qualified reviewer supplies every judgment.

**PROVISIONAL** — treating an exposure ratio near unity, or a 90% CI inside a fixed
percentage band, as *the* acceptance criterion is a bioequivalence convention, not
something sourceable to `ich-e11a`. Never supply a threshold the document omitted.

This module does not decide whether any observed difference is **clinically significant**, and does not **select, adjust or justify a dose**. Both are reserved for a qualified reviewer.
