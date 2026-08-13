---
module: hepatic-impairment
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [fda-hepatic, fda-labeling-cp, cfr-201-57-c-13]
consumers: [review-csr-pk-consistency, verify-nca-outputs, review-protocol-pk-sections, review-uspi-section-12-content, review-ctd-272-content, prepare-dose-justification-evidence, assess-development-plan-gaps, reconcile-cross-document-facts]
---

# Study-type module — hepatic impairment

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

⚠️ **Anchor gap.** `fda-hepatic` is **not present** in
`shared/assets/guidance-index.md`; the FDA hepatic impairment guidance
(*Pharmacokinetics in Patients with Impaired Hepatic Function*) is cited by title
only. **UNVERIFIED:** its status, date, and whether a revision supersedes it. Add
the row from FDA's own page before any skill quotes a date here.

## Design conventions to check

- Classification system named explicitly — **Child-Pugh** or **NCI-ODWG** — used
  consistently across every table, with category stated per subject rather than
  only as a group label.
- A normal-function control group with its matching criteria stated (commonly
  age, weight, sex — PROVISIONAL, practice convention, not a stated requirement).
- Which categories were studied, and where one is absent, why — a reduced design
  is a documented choice, not a silent omission.
- Unbound concentrations addressed where the drug is highly protein-bound;
  albumin is itself a classification component.
- Single- versus multiple-dose design stated, with exposure metrics matching it.

### Classification components — what must be present to reproduce a category

| System | Components | Category bins |
|---|---|---|
| Child-Pugh | Total bilirubin, serum albumin, INR or prothrombin time, ascites, hepatic encephalopathy — 5 components, each scored 1–3, total 5–15 | A = 5–6, B = 7–9, C = 10–15 |
| NCI-ODWG | Total bilirubin and AST, each relative to ULN | Normal, mild, moderate, severe |

**UNVERIFIED:** Child-Pugh components and bins are long-standing in practice but were not checked against a primary source in this pass. Confirm before use. **UNVERIFIED:** the NCI-ODWG
bilirubin and AST cut-points per bin — enforce no numeric threshold from this
module until they are read from the source.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Classification | Named system, plus per-subject category |
| Comparison | Geometric mean ratio, each impaired category / normal control |
| Precision | 90% confidence interval on every reported ratio |
| Parameters | AUC (AUC0-inf single dose, AUCtau steady state) and Cmax at minimum |
| Protein binding | Unbound fraction, and unbound exposure ratios, where measured |
| Dosing statement | Per category: an adjustment, no adjustment, or "not studied / cannot be recommended" |

## Mechanical checks this module enables

1. **Categories studied and categories carrying a dosing statement are the same
   set.** Severe-impairment dosing text with no severe subjects enrolled has no
   supporting arm; a category enrolled but unmentioned is the converse gap.
2. **One classification system throughout.** Child-Pugh in the methods and
   NCI-ODWG in a table is two vocabularies for one variable; category counts
   cannot be reconciled across them.
3. **Category label matches the reported score.** A subject scored 8 labelled
   Child-Pugh A is an arithmetic contradiction between two reported facts.
4. **Subject counts reconcile** — enrolled, per category, analysed — across the
   synopsis, the tables, and the label. Delegated to T05.
5. **Ratio recomputes** from the impaired and normal group means where both are
   reported, and the 90% CI brackets its point estimate. Delegated to T03.
6. **Direction agrees with the ratio.** A stated "increased exposure" against a
   ratio below 1.00 is a contradiction, not an interpretation.
7. **Total and unbound results are not interchanged.** A ratio labelled unbound
   equal to the total ratio, where fu differs between groups, is a traceability
   failure, not a conclusion to draw.
8. **Label text matches the study result** across CSR, Module 2.7.2 and USPI
   12.3 — same categories, same ratios, same statements. Delegated to T05.

## Boundaries

This module does not decide whether an exposure change is *clinically*
significant, does not select or calculate a dose adjustment, does not judge
whether a reduced design was adequate, and does not decide whether a category may
be extrapolated rather than studied. It never classifies a subject — only checks
that a stated classification is consistent with the stated scores. A qualified
reviewer applies judgment and owns any regulatory commitment. Renal impairment is
a **separate** assessment under `fda-renal`; do not carry criteria between them.
