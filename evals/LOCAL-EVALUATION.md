# Local behavioral evaluation

Date: 2026-07-29 · **superseded as a method on 2026-08-06**
Status: completed local conformance run; not a performance benchmark
Material: public synthetic fixtures only

> **The results below stand. The method described no longer runs.**
>
> The cases have moved to [`build-work-context/`](build-work-context/) under the
> PS-D028 layout, and the adjudication step is no longer performed by
> `scripts/grade_local_evals.py`, which was retired on 2026-08-06 — its outcomes
> were a literal `True`/`False` table in the source rather than readings of any
> output, and the `_eval-workspace/` it required had never existed in this tree.
> Grading now reads `outputs/response.md` (`scripts/eval_grade.py`), and a judged
> assertion without a recorded reviewer, verdict and quotation fails closed.
>
> This file is kept as the record of what was measured on 2026-07-29. Re-run it
> under the current harness before quoting it as a current result.

## Method (as run on 2026-07-29)

Independent executor contexts produced one response with the skill and one
without it for each fixed case. The primary reviewer then adjudicated every
written assertion against the saved outputs. Raw run transcripts, responses,
metrics, and grading records were retained in the ignored local
`_eval-workspace/` and are not part of the public repository.

## Results

| Case | Skill condition | Baseline condition | Result |
|---|---:|---:|---|
| CREATE with skipped answers | 5/5 | 3/5 | Skill condition passed all required context-contract behaviors |
| UPDATE with conflicting cadence | 5/5 | 5/5 | Both preserved the unresolved conflict |
| PROJECT and EXPORT source authority | 5/5 | 5/5 | Both preserved governing results and limitations |
| REFRESH stale context | 5/5 | 5/5 | Both retained the unresolved permission boundary |
| Restricted-data warning | 5/5 | 4/5 | Skill condition emitted the required stop classification |
| **Total** | **25/25** | **22/25** | Behavioral conformance only |

The baseline was intentionally strong and passed most domain-independent safety
and source-fidelity requirements. The skill condition's distinguishing evidence
in this single run was completeness of the reusable context contract and exact
restricted-data classification.

## What this proves

- Each of CREATE, UPDATE, PROJECT, REFRESH, and EXPORT produced the required
  behavior on its synthetic fixture.
- Skipped fields remained unknown rather than being invented.
- Decision-changing conflicts were exposed rather than silently overwritten.
- Source authority preserved 14.2 L/h as final, 12.4 L/h as historical, and 90%
  rather than the conflicting draft 80% interval.
- Restricted-data input stopped before processing and used
  `RESTRICTED_DO_NOT_PROCESS`.

## What this does not prove

- It does not establish performance improvement across models, dates, hosts, or
  repeated runs.
- It does not validate any GxP, clinical, medical, regulatory, or submission
  workflow.
- It does not complete ChatGPT, Claude, GitHub Copilot, or Microsoft 365
  Copilot host testing.
- Timing and token telemetry were unavailable or inconsistent, and one executor
  did not expose an exact model identifier.

Any public comparative claim remains blocked until the fixed protocol in
[`../benchmark/`](../benchmark/) is repeated with a recorded model, date,
run count, and source-fidelity review.
