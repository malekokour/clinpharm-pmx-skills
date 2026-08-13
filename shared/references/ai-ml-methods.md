---
module: ai-ml-methods
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
anchors: [fda-ai-credibility, ich-m15, ema-ai-reflection]
consumers: [assess-development-plan-gaps, review-model-analysis-deliverable]
---

# Reference — AI and machine-learning methods in drug development

Reference content only. It supplies criteria for evaluating an AI or machine-learning
component inside a submission or an analysis package.

**Why this is a reference and not a skill (PS-D030).** "AI/ML methods" is a field, not a
task: no practitioner utterance selects it, no document class is its input, and it
produces no artifact of its own. The workflows that use these criteria — development-plan
gap assessment, model-deliverable review — are separate skills.

**A note on this file's own subject.** A library of agent skills for clinical pharmacology
is itself an application of these methods. The credibility expectations below apply to
this product as much as to anything it reviews, which is why the status vocabulary
distinguishes a package that exists from one whose gate has passed.

## Design conventions to check

- **Context of use is stated before credibility is assessed.** The same model may be
  low-risk for hypothesis generation and high-risk for a dosing decision. Credibility
  requirements scale with influence on the decision and with the consequence of being
  wrong — a risk-based framework, not a fixed bar.
- **Training, validation and test data are separated**, and the separation is auditable.
  Leakage between them is the most common defect and the hardest to see afterwards.
- **The evaluation set represents the intended population.** Performance on a set that
  excludes the patients the model will be applied to is not evidence about them.
- **Performance is reported with uncertainty and with a denominator**, not as a single
  headline figure.
- **A baseline comparison exists.** A model that does not beat a simple regression, or a
  clinician, has not demonstrated value.
- **Explainability is proportionate to the context of use**, and the mechanism by which
  a prediction is made is described at a level a reviewer can interrogate.
- **Version, data cut, and environment are recorded** so the result can be reproduced.
  A model whose output cannot be regenerated is not evidence.
- **Drift and lifecycle maintenance are planned** where the model persists after
  approval.

## Expected statements in a report

- The context of use and the decision the model influences.
- The risk assessment that set the credibility bar, and its result.
- Data provenance, size, and how training, validation and test sets were separated.
- Performance with uncertainty, on a named evaluation set, against a named baseline.
- Known limitations and the populations where performance is unverified.
- Version, data cut-off, environment, and how to reproduce the result.
- Where the model output was overridden or not followed, and why.

## Mechanical checks this module enables

- Every performance claim carries a denominator and an uncertainty interval.
- The evaluation set is named and distinct from the training set.
- A baseline comparator is stated.
- Model version and data cut-off appear wherever a result is cited.
- Claims about populations outside the evaluation set are flagged as extrapolation.
- The context of use appears alongside any credibility claim.

## Boundaries

This module supplies criteria. It does **not** decide whether a model is credible for a
context of use, accept a performance result, approve a method for regulatory reliance,
or judge whether explainability is adequate. It does **not** select or adjust a dose,
and it does **not** decide whether a model-derived difference is clinically significant.
A model output is evidence for a judgment, never the judgment. Those judgments are
reserved for qualified humans and, where applicable, for the reviewing authority.
