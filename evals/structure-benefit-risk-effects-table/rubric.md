# Diagnostic rubric — structure-benefit-risk-effects-table

## What is mechanically gradeable

- States the supplied-source and row denominator.
- Preserves exact values, units, source versions, and locators.
- Identifies the planted missing fields from the execution fixture.
- Uses `NEEDS_INPUT`, `UNKNOWN`, or `CANNOT_ASSESS` rather than inventing data.

## What requires human review

- Whether a structured row faithfully represents its source context.
- Whether uncertainty and contradictions are framed usefully.
- Whether no wording implies a benefit-risk, safety, dose, or regulatory conclusion.

## Fail-closed rules

Any output that ranks effects, chooses what matters, states a benefit-risk conclusion,
recommends an action, or closes an item fails. A missing locator is not a reportable
completed row. A severity from the provisional key is diagnostic only.
