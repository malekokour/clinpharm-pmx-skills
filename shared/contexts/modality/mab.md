# Context — therapeutic protein and monoclonal antibody

**Dimension:** modality · **Attaches after selection; never selected**
**Promoted from** the former `shared/modules/biologics-mab-pk.md` (PS-D030).

What changes when the molecule is a therapeutic protein or mAb, relative to a
small-molecule default. This sharpens a skill; it never replaces one, and it never
relaxes a refusal.

## Disposition — what the default assumption gets wrong

| Default assumption | What actually holds |
|---|---|
| Absorption is first-order from gut | Subcutaneous absorption is slow and lymphatic; bioavailability typically well below complete, and route matters |
| Hepatic metabolism by CYP enzymes | Catabolism to peptides and amino acids; **CYP-mediated DDI is generally not the question** |
| Renal filtration clears the drug | Molecular size prevents filtration; renal impairment is usually not a dosing driver on its own |
| Clearance is constant | Target-mediated drug disposition can make clearance concentration- and target-dependent, especially at low dose |
| Half-life of hours | Days to weeks, driven by FcRn recycling |
| Steady state within days | Weeks; loading strategies and sampling schedules must reflect it |

## Interaction assessment

The CYP and transporter framework is largely not applicable. What replaces it:

- **Cytokine-mediated interactions.** In inflammatory disease, disease activity can
  suppress CYP expression; a biologic that lowers cytokines can restore it and change
  the exposure of co-administered small molecules. This is a real interaction pathway
  with a different mechanism.
- **Combination with another biologic** raises immunogenicity and target-competition
  questions rather than enzyme questions.
- **Protein–protein displacement** is rarely the driver people assume.

Do not report "no DDI expected" as a conclusion. Report which mechanisms were assessed
and which do not apply, with the reason.

## Immunogenicity is a PK variable, not only a safety topic

Anti-drug antibodies can increase clearance, shorten half-life, and produce apparent
non-linearity or high inter-individual variability. Any exposure dataset without ADA
status attached is incompletely characterised. Where ADA data exist, exposure should be
described with ADA status as a covariate rather than pooled silently.

## Dose and regimen

- **Fixed versus weight-based** is a live question for this modality and has regulatory
  precedent in both directions. Body-size effect size, not convention, decides it.
- Flat dosing simplifies handling and reduces error; weight-based can matter when the
  exposure–response slope is steep and the weight range is wide.
- Loading doses are common where FcRn-driven accumulation is slow.

## Populations

- **Renal impairment:** usually not a dosing driver. Say why rather than omitting it.
- **Hepatic impairment:** catabolism is not hepatic in the small-molecule sense;
  severe disease may still alter distribution and albumin binding.
- **Paediatric:** allometric scaling behaves differently from small molecules; maturation
  of FcRn and of clearance follows its own course.
- **Pregnancy:** placental transfer is FcRn-mediated and increases through gestation —
  a modality-specific consideration with no small-molecule analogue.

## Bioanalysis

Ligand-binding assays, not chromatography. That changes what "validated" means, what
interference looks like, and how free versus total analyte is reported. When target
concentration is high, free-versus-total reporting becomes decision-relevant rather
than technical detail.

## What this context does not do

It does not decide dose, declare a DDI absent, or accept an immunogenicity result. It
tells a skill which of its default assumptions do not hold here.
