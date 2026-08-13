---
module: combination-regimen-pk
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [ich-m12, ich-e4, fda-labeling-cp]
consumers: [review-csr-pk-consistency, verify-nca-outputs, review-protocol-pk-sections, review-ddi-evidence, review-uspi-section-12-content, assess-development-plan-gaps]
---

# Study-type module — combination-regimen pharmacokinetics

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

## ⚠️ This module rests on practice convention — PROVISIONAL

The guidance index carries **no anchor specific to combination-regimen PK**. The
anchors above are the nearest applicable: `ich-m12` for the interaction between
components, `ich-e4` for dose-response, `fda-labeling-cp` for the write-up.
Everything below is therefore **PROVISIONAL** — common practice, not a cited
requirement, never to be presented as a regulatory criterion. **Unverified and
deliberately left blank:** whether any body has issued combination-specific
clinical-pharmacology guidance, and if so its date, section numbering, and any
no-effect or acceptance criteria. Verify before a consuming skill cites a
requirement; do not fill the gap by analogy to the DDI anchors.

## Design conventions to check — PROVISIONAL

- Each component's contribution to observed exposure is **separable by design**:
  a monotherapy reference arm or period per component, or its absence justified.
- Both directions addressed where both matter — A on B and B on A are two
  questions, not one.
- Dosing sequence and timing explicit: co-administered or staggered, by how much.
- Sampling adequate for the **slower** component's terminal phase, not the faster.
- Steady-state status stated per component; components with different half-lives
  do not reach steady state together.
- Fixed-dose combinations: bioavailability comparison against a free-combination
  reference, or interaction assessment — stated, not implied; the arms differ.
- Formulation, strength and lot identified per component, so an exposure change
  is not silently attributable to a formulation change.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Comparison | Geometric mean ratio, combination / component alone, per component and per direction |
| Precision | 90% confidence interval on each ratio |
| Reference | The exact reference arm named — monotherapy, free combination, or historical |
| Parameters | Cmax and AUC per component at minimum; Ctrough where the regimen is chronic |
| Attribution | Which component's exposure changed, and against which reference |
| Steady state | Stated per component, with the supporting data identified |
| Conclusion | A dosing statement per component, or an explicit statement that none follows |

## Mechanical checks this module enables

1. **Every exposure-change claim names its reference arm.** "Exposure increased"
   with no stated comparator is an unresolvable attribution, not a finding.
2. **Ratio recomputes** per component from the combination and reference means
   where both are reported. Delegated to T03 `pk_plausibility`.
3. **CI brackets the point estimate** for each ratio. Delegated to T03.
4. **Direction versus ratio.** A stated "decrease" with a ratio above 1.00 is a
   contradiction between two reported facts; reversals propagate into labelling.
5. **Per-component coverage complete.** N components, fewer than N reported
   ratios, no stated reason — an absent required element.
6. **Both directions present or explicitly scoped out.** A bidirectional
   assessment reporting one direction is an internal inconsistency.
7. **Parameter definitions match across components.** AUC0-inf against AUCtau is
   a definitional mismatch, not a comparison.
8. **Cross-document agreement** of each ratio, CI and reference arm across CSR,
   2.7.2 and label. Delegated to T05 `cross_document_consistency`.
9. **Steady-state claim per component has supporting pre-dose data**, over a
   sampling duration that supports the longer-half-life component.
10. **The dosing statement follows the reported finding.** "No dose adjustment
    required" beside a materially non-unity ratio is two sentences disagreeing.

## Boundaries

This module does not decide whether an interaction between components is
*clinically* significant, does not select or adjust a dose, does not judge
whether a monotherapy arm was feasible, does not evaluate combination efficacy
or safety, does not determine whether an assessment can be waived, and makes no
regulatory commitment or approval. It supplies criteria and finds mechanical
disagreements; a qualified reviewer applies judgment.

Interaction with a co-medication **outside the intended regimen** is a separate
assessment under `ich-m12` — never recorded as a combination-regimen finding.
