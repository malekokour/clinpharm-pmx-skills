# Eval suite — review-adc-analyte-strategy

Eleven diagnostic cases, authored with the package under plan packet P07 (gap
wave B) on 2026-08-11.

**Diagnostic, not qualifying.** No expert-keyed fixture, no paired runs, no
holdout, no practitioner review. The package stays `built`.

## Why the weighting

The finding this package exists for is **definition drift** — the same analyte
name carrying different definitions in different documents. The execution cases
exercise it directly, including the case that matters most: two documents that
agree numerically while disagreeing about what was measured.

The safety cases target the three ways a response could destroy that finding —
harmonising the definitions, recommending an analyte, or judging biological
reasonableness.
