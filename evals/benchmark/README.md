# ClinPharm PMx Skills Benchmark

This benchmark compares the same synthetic ClinPharm/PMx task with and without
an AI Working Pack. It is designed to measure source fidelity and boundary
handling, not general model intelligence.

## Fixed protocol

1. Use the three files in `examples/clinpharm-pmx/sources/`.
2. For baseline runs, use [`baseline-prompt.md`](baseline-prompt.md).
3. For context runs, also attach
   `examples/clinpharm-pmx/outputs/AI-Working-Pack-SYN-101.md` and use
   [`context-prompt.md`](context-prompt.md).
4. Keep model, model version if exposed, date, settings, and file set identical.
5. Run each condition at least three times in a fresh conversation.
6. Score blind where practical using [`scoring-rubric.md`](scoring-rubric.md).
7. Record every run in a copy of
   [`results-template.md`](results-template.md).

Do not claim improvement from an example output or a single favorable run. Report
model- and date-specific results with limitations.

## Current status

Three repeated Codex runtime pairs and a condition-label-masked second scoring
pass are complete. Both conditions were strong; the Working Pack condition
consistently improved explicit source-authority traceability by one rubric
point. The second pass agreed on all 48 dimension ratings but was performed by
the same implementation reviewer, so it is not independent. This is a narrow,
dated result, not a cross-provider claim. See
[`results/2026-07-30-codex/SUMMARY.md`](results/2026-07-30-codex/SUMMARY.md)
and [`STATUS.md`](STATUS.md).
