# Context — small molecule

**Dimension:** modality · **Attaches after selection; never selected**

The default assumptions most clinical-pharmacology methods were built around. This file
exists so those assumptions are **stated rather than implied** — a skill that silently
assumes them will mislead when the molecule is something else.

## What holds by default

| Area | Default expectation |
|---|---|
| Absorption | Oral, dissolution- and permeability-limited; food and gastric pH can matter |
| Distribution | Plasma protein binding relevant; tissue distribution follows physicochemistry |
| Metabolism | CYP and UGT pathways; the standard reaction-phenotyping framework applies |
| Transport | Uptake and efflux transporters are in scope for interaction assessment |
| Elimination | Renal and hepatic routes both plausible; mass balance resolves the split |
| Half-life | Hours to a few days |
| Immunogenicity | Not a PK variable |
| Bioanalysis | Chromatographic with mass-spectrometric detection |

## Where the default still breaks

Being a small molecule does not make the standard path automatic:

- **Highly bound compounds** — free-fraction changes matter more than total-concentration
  changes, and organ impairment can shift them.
- **Transporter substrates without CYP involvement** — a clean reaction-phenotyping
  result does not mean no interaction.
- **Non-linear kinetics** from saturable metabolism, auto-induction, or
  solubility-limited absorption. Dose proportionality is a question, never an assumption.
- **Active or reactive metabolites** — human metabolite safety testing may be triggered
  and the parent-only story becomes incomplete.
- **Prodrugs** — the moiety that matters for exposure–response is not the one dosed.
- **Enantiomers** — a racemate analysed as a single analyte can hide the whole story.

## Interaction assessment

The full framework applies and is expected: in-vitro reaction phenotyping, inhibition
and induction of the major enzymes, transporter substrate and inhibitor assessment,
then model-informed or clinical confirmation as the results direct. Absence of a
clinical study is defensible only when the in-vitro and model-based case is complete
and stated.

## Populations

Renal and hepatic impairment are both live questions and usually need explicit
handling. Pharmacogenomic variation in metabolising enzymes is a real source of
exposure variability and may itself drive a labelling statement.

## Formulation

Biopharmaceutics matters here in a way it does not for most other modalities:
formulation change, food effect, acid-reducing agents, and biowaiver justification all
sit on the critical path.

## What this context does not do

It does not certify that the standard framework was correctly applied. It states what
the framework assumes, so a skill can check whether those assumptions hold for this
compound rather than inheriting them silently.
