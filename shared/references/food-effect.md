---
module: food-effect
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [fda-food-effect, fda-ara-gastric-ph]
consumers: [review-csr-pk-consistency, verify-nca-outputs, review-protocol-pk-sections, review-uspi-section-12-content, assess-development-plan-gaps]
---

# Study-type module — food effect

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

## ⚠️ This module was corrected on 2026-08-05

The source research cited the **June 2022** guidance and flagged a possible
Revision 1 as resting on "one low-authority source", instructing the module to
carry a re-verify flag.

Verified against FDA's own guidance page 2026-08-05: **Revision 1 was issued
May 2026.** The research's caution was wrong, and the difference is substantive,
not cosmetic.

**Cite Revision 1 (May 2026).** Any document reviewed against the June 2022
criteria alone should be flagged for re-review.

## What Revision 1 changed

| Change | Consequence for review |
|---|---|
| Dedicated section on **pilot** food-effect assessments | A pilot study is now an anticipated design; its absence is not automatically a gap, and its presence needs its own adequacy assessment |
| **Defined composition of a low-fat meal** | A "low-fat meal" claim without stated composition is now checkable against a definition rather than left to convention |
| Assessment at the **clinically recommended dose** | A food-effect study conducted only at a non-recommended dose is a findable gap |

## Design conventions to check

- Randomised, crossover where feasible; adequate washout stated.
- High-fat, high-calorie meal composition stated, and matching the guidance
  definition. Same for a low-fat arm where one exists.
- Dosing relative to the meal explicitly timed.
- Study conducted at the clinically recommended dose, or a justification present.
- Primary comparison pre-specified: fed versus fasted, on Cmax and AUC.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Comparison | Geometric mean ratio, fed / fasted |
| Precision | 90% confidence interval |
| Direction | Explicit increase or decrease, matching the ratio |
| Parameters | Cmax and AUC at minimum; Tmax where absorption rate matters |
| Conclusion | An administration instruction, or an explicit statement that no restriction follows |

## Mechanical checks this module enables

1. **Direction versus ratio.** A stated "decrease" with a ratio above 1.00 is a
   contradiction between two reported facts. Critical: direction reversals
   propagate into labelling.
2. **CI brackets the point estimate.** Delegated to T03.
3. **Ratio recomputes** from the fed and fasted means where both are reported.
4. **The label instruction follows the finding.** "Take without regard to food"
   alongside a materially non-unity ratio is an unsupported claim.
5. **Meal composition stated** where a meal type is named.

## Boundaries

This module does not decide whether a food effect is **clinically significant**,
does not select an administration instruction, does not **select, adjust or
justify a dose**, and does not determine whether a waiver is justified. It
supplies criteria; a qualified reviewer applies judgment.

Acid-reducing-agent interactions are a **separate** assessment under
`fda-ara-gastric-ph` — final since 2023-03-13, not a draft as the source
research recorded. Do not conflate pH-dependent solubility with a food effect.
