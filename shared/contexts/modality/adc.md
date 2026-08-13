# Context — antibody-drug conjugate

**Dimension:** modality · **Attaches after selection; never selected**

An ADC is not one molecule and cannot be characterised as one. Everything downstream
follows from that.

## The defining problem: there is no single analyte

At minimum, exposure must be described for several species that behave differently:

| Analyte | What it represents | Why it matters |
|---|---|---|
| Conjugated antibody / ADC | Intact conjugate | Delivery of payload to target |
| Total antibody | Conjugated plus unconjugated | Deconjugation over time |
| Unconjugated payload | Free cytotoxic in circulation | Off-target toxicity |
| Payload metabolites | Where relevant | Can dominate the safety picture |

**A skill that reports "the PK" of an ADC without naming which analyte has not
characterised anything.** The relationship between analytes changes over time as the
conjugate deconjugates, so a single time point does not settle it.

Drug-to-antibody ratio drifts in vivo. Mean DAR at dosing is not mean DAR at 21 days,
and exposure metrics that ignore it describe a molecule that no longer exists.

## Exposure–response splits

Efficacy and safety commonly track **different analytes**. Efficacy usually follows
conjugated antibody or delivered payload; toxicity often follows unconjugated payload.
An exposure–response analysis that uses one exposure metric for both is answering half
the question, and is the most common defect in this modality.

## Interaction assessment

Both frameworks apply, to different parts of the molecule:

- The **antibody component** behaves as in `mab.md` — catabolism, FcRn, immunogenicity.
- The **payload** is usually a small molecule with real CYP and transporter liability,
  and free payload concentrations are what matter for that assessment.

Concluding "no DDI expected" from the antibody framework alone misses the payload
entirely.

## Toxicity and dose optimisation

Off-target toxicity is frequently payload-driven and can be dose-limiting well before
target-mediated effects. Ocular, haematologic, hepatic and neuropathic toxicities recur
across payload classes and are payload-specific rather than target-specific — the
comparator that informs the safety expectation is often another ADC with the same
payload, not another antibody against the same target.

Dose optimisation for this modality is under active regulatory attention: maximum
tolerated dose is a weak basis when the therapeutic window is set by free payload.

## Bioanalysis

Multiple assay formats run in parallel — ligand-binding for the antibody species,
chromatographic for free payload — with different validation expectations and
different interference profiles. Assay-format mismatch between analytes is a real
source of apparently impossible results.

## Populations

Hepatic impairment can matter more than the antibody framework suggests, because the
payload and its metabolites may be hepatically cleared. Renal impairment matters where
payload metabolites are renally eliminated. Neither can be dismissed by reasoning about
the antibody alone.

## What this context does not do

It does not choose the exposure metric, accept a bioanalytical package, or judge
whether a toxicity is payload-attributable. It states why one number is never enough.
