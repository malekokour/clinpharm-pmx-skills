---
module: mass-balance-ame
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [fda-mass-balance, fda-renal, ich-m12, fda-labeling-cp]
consumers: [review-csr-pk-consistency, verify-nca-outputs, review-protocol-pk-sections, review-ddi-evidence, review-uspi-section-12-content, assess-development-plan-gaps, review-ctd-272-content, reconcile-cross-document-facts]
---

# Study-type module — human radiolabeled mass balance (ADME)

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

**Anchor status.** `fda-mass-balance` sits in the guidance index as **final,
2024-07** with `Verified` reading `research-sourced` — never checked against
FDA's own page. Verify it in pipeline stage 1 per index maintenance rule 1. **No
section number from that guidance is asserted below**, deliberately. The study is
the pivotal source for route of elimination and fm, so most of the value here is
cross-document rather than within-study.

## Design conventions to check

- Single radiolabeled dose; label position stated, with a statement that it is
  metabolically stable (not on a cleaved or exchangeable position).
- Administered radioactivity stated with units (µCi or kBq, per subject or per
  kg) and consistent across protocol, CSR, and any dosimetry section.
- Excreta collection to a **pre-specified** stopping rule; matrices named, with
  expired air, bile, or vomitus addressed or excluded. **PROVISIONAL:** the usual
  "<1% of dose per 24 h" cutoff is convention, not attributed here to guidance.
- Total radioactivity in blood **and** plasma (so blood-to-plasma is derivable)
  plus parent by validated assay; profiling method and pooling scheme stated.
- Sample size small and non-inferential by design; a comparative statistical
  claim from such a study is a design mismatch to flag.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Total recovery | % of administered radioactivity, with the collection window it covers |
| Route split | % urine and % feces, each labelled as % of **administered dose** or % of **recovered** — never unlabelled |
| Parent in excreta | Fraction excreted unchanged (fe), stated separately from total urinary radioactivity |
| Metabolite profile | Each component as % of total radioactivity in the named matrix, plus the unassigned remainder |
| Fraction metabolized | fm overall, and fm by named pathway wherever enzyme attribution is claimed |
| Circulating metabolites | Each as % of total drug-related exposure, with matrix and pooling basis |
| Downstream statement | Explicit sentence on whether renal, hepatic, or DDI evaluation is triggered or considered unnecessary |

## Mechanical checks this module enables

1. **Route percentages sum to the stated total recovery** — urine + feces + any
   other named route. Delegated to T03.
2. **Denominator consistency.** One number given as "% of dose" in one table and
   "% of recovered radioactivity" in another is a unit inconsistency, not
   rounding — the most common defect in this study type.
3. **fe does not exceed total urinary radioactivity** — parent cannot exceed the
   total it is a component of. Same relation for feces.
4. **Metabolite components in a matrix sum to ≤100%** of total radioactivity
   there, with the unassigned remainder stated rather than implied.
5. **fm and fe reconcile** against the elimination account in the text. T03; a
   deviation is an inconsistency between two values, not proof either is wrong.
6. **Route-of-elimination claim matches the numbers wherever repeated** — CSR,
   Module 2.7.2, IB, USPI Section 12.3. T05. "Primarily renally eliminated"
   beside a majority-fecal recovery table is a cross-document contradiction.
7. **Radiolabel dose, label position, and collection stopping rule** agree
   between protocol and report, with any deviation noted.
8. **Trigger statements carry their supporting number** — a claim that a renal
   study is unwarranted needs an fe value in the same document set, a DDI
   liability claim needs an fm for that pathway. Presence check only.
9. **Threshold statements carry both the value and the threshold used.**
   **UNVERIFIED:** the commonly cited 10%-of-total-drug-related-exposure
   criterion for circulating metabolites comes from MIST / ICH M3(R2), neither of
   which has an anchor ID in the index — never assert it until one exists.

## Boundaries

This module does not decide whether recovery is adequate, whether a renal,
hepatic-impairment, or DDI study is warranted, or whether any metabolite is
safety-relevant. It does not select or adjust a dose, commit to anything with a
regulator, or approve a labelling statement.

**PROVISIONAL:** the cut-points used to trigger those workstreams — an fe
threshold for renal, an fm threshold for a DDI liability — are convention and
vary by programme. This module checks only that a stated threshold and its
supporting value are both present and consistent; take the criterion itself from
`fda-renal` or `ich-m12`, once that row is verified.

This module does not decide whether any observed difference is **clinically significant**, and does not **select, adjust or justify a dose**. Both are reserved for a qualified reviewer.
