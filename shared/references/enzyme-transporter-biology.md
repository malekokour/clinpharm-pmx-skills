---
module: enzyme-transporter-biology
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
anchors: [ich-m12, fda-ddi-invitro, ema-ddi]
consumers: [review-ddi-evidence, assess-development-plan-gaps, review-uspi-section-12-content]
---

# Reference — enzyme and transporter biology

Reference content only. It supplies the criteria a DDI workflow applies; it runs no
workflow of its own.

**Why this is a reference and not a skill (PS-D030).** No practitioner asks an agent to
"do enzyme and transporter biology." There is no distinct input document, no distinct
output artifact, and nothing to refuse. The work lives in the in-vitro and clinical DDI
skills; this file is what they read.

## Design conventions to check

- **Reaction phenotyping covers the pathways that matter.** A fraction metabolised
  attributed to a single enzyme should be supported by more than one approach — chemical
  inhibition, recombinant enzymes, correlation analysis — because each has a
  characteristic failure.
- **Fraction metabolised sums honestly.** Contributions across identified pathways plus
  an unassigned remainder should account for elimination. A package that assigns 95% to
  one enzyme and never states the remainder has usually not looked.
- **Transporters are assessed, not assumed absent.** Substrate and inhibitor evaluation
  against the transporters named in current guidance is expected. A compound with clean
  CYP data and no transporter data has an incomplete package, not a negative one.
- **Inhibition covers reversible and time-dependent mechanisms.** Reporting a reversible
  inhibition constant alone leaves the mechanism-based question open.
- **Induction is assessed at the mRNA and activity level** where the design allows, with
  a positive control that behaved.
- **Cut-offs are the current ones.** Basic-model thresholds and their revisions change;
  a package evaluated against a superseded cut-off may reach the opposite conclusion.
- **In-vitro to in-vivo extrapolation states its assumptions** — unbound fraction, gut
  concentration assumptions, and which model was used.

## Expected statements in a report

- Which enzymes and transporters were evaluated, and which were not, with the reason.
- The fraction metabolised by each identified pathway, and the unassigned remainder.
- Whether each in-vitro signal crossed the decision threshold, and which threshold.
- For each crossed threshold: the follow-up taken — clinical study, model-based
  assessment, or labelling statement — and why that route was sufficient.
- Where a clinical study was **not** done, the model or reasoning that replaced it.
- The victim and perpetrator roles the compound can occupy, stated separately.

## Mechanical checks this module enables

- Every enzyme or transporter named in the label appears in the in-vitro package.
- Every in-vitro signal above threshold has a terminus — study, model, or label text.
- Fraction-metabolised values across pathways do not exceed unity.
- Threshold values cited match the guidance version cited.
- Units and directions are consistent between the in-vitro report and the summary.

## Boundaries

This module supplies criteria. It does **not** judge whether an interaction is
clinically significant, decide whether a clinical study is required, adjust a dose,
accept the adequacy of an assay, or conclude that no interaction exists. Whether an
exposure change matters clinically is a judgment that stays with a qualified human, and
a complete in-vitro package is evidence for that judgment rather than a substitute for
it.
