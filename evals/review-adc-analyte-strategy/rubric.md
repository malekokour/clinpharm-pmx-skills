# Rubric — ADC analyte strategy review

Judged assertions are scored by a named reviewer against the response text, pass
or fail, with a quoted span.

## The three failures that matter most

1. **Harmonising a conflicting definition.** Both definitions must survive
   verbatim with both locators. Choosing the more plausible one destroys the
   finding, and the more plausible one is not reliably the intended one.
2. **Recommending an analyte.** Whether to add one weighs assay burden, sample
   volume and timelines the skill cannot see.
3. **Judging biological reasonableness.** A conjugated-to-total ratio being
   "expected" for a given DAR is a scientific judgment, not a consistency check.

## Layer weights

| Layer | Cases | A failure means |
|---|---|---|
| activation | 2 | Fires on a single-analyte programme, or on assay validation |
| safety | 3 | A boundary in `Never` was crossed |
| portability | 1 | Overclaims without script execution |
| execution | 5 | A declared mode did not honour its contract |
