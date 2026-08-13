---
module: protein-binding-distribution
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
anchors: [fda-hepatic-impairment, fda-renal-impairment, ich-m12]
consumers: [review-csr-pk-consistency, assess-development-plan-gaps, review-human-pk-prediction]
---

# Reference — protein binding and tissue distribution

Reference content only. It supplies criteria that organ-impairment, modelling and
exposure-characterisation workflows apply.

**Why this is a reference and not a skill (PS-D030).** There is no distinct trigger, no
distinct input document, and no artifact that is produced by "doing protein binding."
The work sits inside the hepatic-impairment, renal-impairment and prediction skills.

## Design conventions to check

- **Free fraction is measured, not assumed.** For a highly bound compound, a small
  change in bound fraction is a large change in free concentration. Total concentration
  can be flat while free concentration doubles.
- **The method is stated and fits the compound.** Equilibrium dialysis, ultrafiltration
  and ultracentrifugation each fail differently — non-specific binding, volume shift,
  sedimentation of lipoproteins. A result without a method is uninterpretable.
- **The binding protein is identified.** Albumin and alpha-1-acid glycoprotein move in
  opposite directions in inflammation, so which protein binds the compound determines
  the direction of the disease effect.
- **Concentration dependence is checked** across the clinically relevant range.
  Saturable binding turns a linear-looking exposure into a non-linear free exposure.
- **Species differences are stated** where animal data support a human prediction.
- **Volume of distribution is interpreted against free fraction**, not in isolation.
- **Tissue distribution claims name their evidence** — tissue sampling, imaging, or a
  model. A predicted tissue-to-plasma ratio is a prediction.

## Expected statements in a report

- Free fraction, the method, the concentration range tested, and the matrix.
- Which plasma protein carries the binding, and the evidence for it.
- Whether binding is concentration-dependent over the therapeutic range.
- How free fraction differs in the populations studied — hepatic impairment, renal
  impairment, inflammation, pregnancy, older age — or that it was not measured.
- Whether exposure metrics used for exposure–response are total or free, stated
  explicitly and consistently.
- For a distribution claim, the measurement or model behind it.

## Mechanical checks this module enables

- Every exposure–response analysis names total or free, and uses one consistently.
- A free-fraction value in a summary matches the study report it came from.
- Where organ impairment changed total exposure, the free-fraction consequence is
  addressed rather than omitted.
- Volume of distribution and free fraction are reported in compatible units.
- A tissue concentration claim carries a source.

## Boundaries

This module supplies criteria. It does **not** decide whether a change in free fraction
is clinically significant, adjust a dose, accept a binding assay as validated, or judge
whether a distribution model is fit for its purpose. The clinical meaning of a free-
concentration change is a judgment reserved for a qualified human.
