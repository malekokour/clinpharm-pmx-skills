# Context — oncology

**Dimension:** therapeutic area · **Attaches after selection; never selected**
**Promoted from** the former `shared/modules/oncology-dose-optimization.md` (PS-D030).

What oncology changes about clinical-pharmacology reasoning. The dominant shift over the
last decade is that **the maximum tolerated dose is no longer an acceptable default
basis for the registered dose.**

## Dose selection

The historical cytotoxic paradigm — escalate to toxicity, register the highest tolerable
dose — does not fit targeted agents, immunotherapies, or antibody-based products, where
the exposure–response curve for efficacy often plateaus well below the tolerable dose.

What is expected instead:

- **More than one dose studied** in a randomised setting before registration, where
  feasible
- **Exposure–response for efficacy and for safety, separately** — they rarely share a
  metric or a slope
- Evidence of **target engagement or receptor occupancy** supporting the chosen level
- A dose rationale that survives the question *why not lower?*

A dose justification resting only on tolerability is incomplete in this area, and saying
so is the correct output rather than accepting the escalation result.

## Trial-design consequences for exposure data

- **Single-arm registration** paths mean exposure–response is often built on one dose
  level, which confounds exposure with prognosis. State the confounding rather than
  reporting the relationship as causal.
- **Dropout is informative.** Patients who progress or discontinue leave the exposure
  dataset, and naive exposure–response then attributes their absence to low exposure.
- **Dose modification is frequent**, so administered dose diverges from planned dose
  early. Dose intensity over time is a more honest exposure summary than nominal dose.
- **Combination is the norm.** Attributing an effect to one component requires a design
  that permits it.

## Population characteristics that shift the defaults

Patients are typically sicker, older, on more concomitant medication, and with more
organ impairment than in most other areas. Consequences: hepatic and renal impairment
are common rather than special populations; interaction burden is high; and albumin and
inflammatory state can shift free fraction and clearance in ways that look like
covariate effects but track disease severity.

Tumour burden itself can drive clearance for target-mediated agents, which makes
baseline clearance a prognostic marker and a confounder in the same analysis.

## Safety interpretation

Toxicity is expected and graded rather than avoided, so the exposure–safety question is
usually about the rate of a defined severe event, not any adverse event. Cumulative and
delayed toxicity matter more than peak, which changes which exposure metric is relevant.

## What this context does not do

It does not choose a dose, judge whether a dose-optimisation package is sufficient, or
adjudicate an exposure–response result. It states why the escalation-derived answer is
usually the wrong starting point here.
