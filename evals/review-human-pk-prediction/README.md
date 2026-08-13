# Eval suite — review-human-pk-prediction

Eleven diagnostic cases, authored with the package under plan packet P08 (gap
wave C, PMx track start) on 2026-08-11.

**Diagnostic, not qualifying.** No expert-keyed fixture, no paired runs, no
holdout, no practitioner review. `thresholds.state` is `diagnostic`, recall and
precision are explicitly not claimed, and the package stays `built`.

## Why the weighting

The expensive error for this package is not a missed finding. It is **inventing
an input**: a prediction review that supplies a plausible fraction unbound has
silently become an analysis, and its output now contains a number the deliverable
never claimed. Three safety cases target that and the two adjacent boundaries
(judging correctness, selecting a dose).

The activation cases separate it from `review-model-analysis-deliverable`, which
reviews an analysis of *observed* data — the nearest neighbour and the easiest
confusion.

One execution case per declared mode, as the repository contract requires.
