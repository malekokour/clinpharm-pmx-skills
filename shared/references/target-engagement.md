---
module: target-engagement
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
anchors: [fda-midd, ich-e4]
consumers: [prepare-dose-justification-evidence, assess-development-plan-gaps, review-fih-dose-rationale]
---

# Reference — target engagement

Reference content only. It supplies criteria for interpreting engagement evidence.

**Why this is a reference and not a skill (PS-D030).** The work of building an
engagement strategy is a separate job-model row that *is* a skill — *Biomarker and
target-engagement strategy*. This file is the criteria that skill and its neighbours
read, which is why the ledger records it as carried by that row.

## Design conventions to check

- **Engagement is distinguished from effect.** Occupancy demonstrates the drug reached
  and bound the target. It does not demonstrate that binding produced benefit, and the
  two are routinely conflated in dose rationales.
- **The relationship between exposure and occupancy is characterised**, not assumed
  linear. Occupancy saturates; the exposure that gives 90% occupancy is far more than
  the exposure that gives 50%.
- **The occupancy threshold has a basis.** A target occupancy level chosen because it is
  achievable is not a rationale; one chosen from preclinical efficacy, from a comparator,
  or from a mechanistic model is.
- **The measurement site is the relevant compartment.** Peripheral occupancy is not
  central occupancy, and tumour occupancy is not plasma occupancy.
- **Timing captures the trough**, since sustained engagement usually matters more than
  peak. Occupancy measured only at peak overstates coverage.
- **Displacement and tracer assumptions are stated** for imaging-based measurements.
- **For irreversible or long-residence binding**, recovery kinetics — resynthesis rate —
  govern the dosing interval more than plasma half-life does.

## Expected statements in a report

- The target, the method of measuring engagement, and the compartment sampled.
- The exposure–occupancy relationship, with the model and its parameters.
- The occupancy level targeted, and the evidence for choosing it.
- Occupancy at trough for the proposed regimen, not only at peak.
- For irreversible binders, the recovery rate and how it sets the interval.
- What engagement evidence does and does not support about efficacy.

## Mechanical checks this module enables

- A dose rationale citing occupancy states the level, the time point, and the basis.
- Occupancy values lie between zero and one hundred percent and are consistent across
  documents.
- The exposure used in an occupancy relationship matches the exposure metric used
  elsewhere, or the difference is explained.
- Any claim that engagement supports efficacy carries separate efficacy evidence.
- The compartment measured is named wherever an occupancy number appears.

## Boundaries

This module supplies criteria. It does **not** select a target occupancy, decide that
engagement is sufficient for efficacy, select or adjust a dose, or accept an imaging
method. It does **not** decide whether an occupancy difference is clinically
significant. The inference from engagement to clinical benefit is a judgment reserved
for a qualified human, and this module exists partly to keep that inference visible
rather than implicit.
