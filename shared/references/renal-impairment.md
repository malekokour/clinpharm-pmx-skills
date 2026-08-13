---
module: renal-impairment
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [fda-renal, fda-labeling-cp, cfr-201-57-c-13]
consumers: [review-csr-pk-consistency, verify-nca-outputs, review-protocol-pk-sections, review-uspi-section-12-content, review-ctd-272-content, reconcile-cross-document-facts, prepare-dose-justification-evidence, assess-development-plan-gaps]
---

# Study-type module — renal impairment

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

## ⚠️ Anchor status — verify before this module freezes

`fda-renal` sits in the guidance index as **final, March 2024**, on a
`research-sourced` row never checked against FDA's own page. **UNVERIFIED: that
date, the finality status, and which renal-function metric the current version
specifies** — the move from creatinine clearance to eGFR happened across a
revision, so the metric is exactly what a stale citation gets wrong. Verify all
three in pipeline stage 1 first. No section number is recorded here; cite none.

## Design conventions to check

- Renal-function metric **named once and used consistently** — eGFR or creatinine
  clearance — across protocol, CSR and label, units held constant:
  `mL/min/1.73 m²` (indexed) and `mL/min` (de-indexed) are different quantities.
  PROVISIONAL: which applies to enrollment versus dosing is not settled here —
  flag mixing, do not assert which is correct.
- Category boundaries pre-specified and non-overlapping, every enrolled subject
  inside their assigned band. Conventional bands follow the KDIGO G-stages
  (normal, mild, moderate, severe, kidney failure) — PROVISIONAL as to numeric
  cut-points, which must be read off the guidance, not assumed.
- **Design declared as reduced or full.** Reduced enrols normal plus the
  most-impaired category, full covers the intermediate ones; the report states
  which, and what would have escalated a reduced design to full.
- Dialysis subjects, where enrolled, form their own group, sampling timed
  relative to the session, on- versus off-dialysis conditions described.
- Control group defined — matched normal-function subjects, or a declared
  external comparison. **Unbound concentrations** measured where protein binding
  is material, **active metabolites** where they exist.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Comparison | Geometric mean ratio, impaired category / normal, one per category studied |
| Precision | 90% confidence interval on each ratio |
| Parameters | AUC and Cmax at minimum; CL/F or CLR where renal clearance is claimed |
| Renal function | Value and metric per group, in the stated units |
| Unbound and metabolites | Unbound exposure reported separately where protein binding is material; active metabolites where they exist |
| Dialysis | Fraction removed, or an explicit statement it was not assessed |
| Dose statement | A dose recommendation per category, **or** an explicit "no dosage adjustment" for that category |

## Mechanical checks this module enables

1. **Every studied category has a dose statement.** A category present in the PK
   table and absent from the dosing text is a missing required element.
2. **Category assignment matches the reported renal-function value.** A subject
   labelled moderate whose eGFR falls in the severe band is two facts disagreeing.
3. **Units consistent** across protocol, CSR, 2.7.2 and label — indexed and
   de-indexed never silently interchanged. Delegated to **T05
   cross_document_consistency**.
4. **GMR and CI arithmetic** — the CI brackets the point estimate, the ratio
   recomputes from the group geometric means. Delegated to **T03 pk_plausibility**.
5. **Stated trend matches the reported ratios.** Text claiming exposure rises with
   declining renal function against a non-monotonic ratio set is a text-versus-
   table inconsistency — never evidence the data are wrong.
6. **Design completeness.** A declared reduced design missing the most-impaired
   category, or a full design missing an intermediate one it claimed to enrol.
7. **Group n reconciles** across design section, PK results table and label.
8. **Renal clearance claim has supporting data** — "substantially renally cleared"
   with no CLR or urinary-recovery value anywhere in the set. Search via **T05**.

## Boundaries

This module does not decide whether an exposure change is *clinically*
significant, does not select or adjust a dose, does not choose between a reduced
and a full design, does not decide whether a study can be waived or replaced by a
population-PK or PBPK analysis, and does not judge whether the enrolled
renal-function distribution was adequate. It supplies criteria and surfaces
mechanical disagreements; a qualified reviewer applies judgment and owns every
regulatory commitment. `fda-labeling-cp` and `cfr-201-57-c-13` govern *where* a
dose statement belongs in labelling; this module only checks one is **present**.
