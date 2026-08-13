# Worked example — verifying an NCA report against its dataset

**Input shape: numeric / dataset.** A non-compartmental analysis report, the
parameter dataset it was built from, the analysis plan that governs it, and the
exclusion log.

Everything here is **synthetic**. `SYN-101` through `SYN-108`, the compound, the
values, and the study are invented for demonstration and testing. They are not
clinical evidence and carry no dosing implication.

## What you feed it

| File | What it is |
|---|---|
| [`inputs/synthetic-nca-report.md`](inputs/synthetic-nca-report.md) | The reported results — Table 3 per-subject parameters, Table 5 summary statistics |
| [`inputs/synthetic-parameter-dataset.txt`](inputs/synthetic-parameter-dataset.txt) | The dataset the report is supposed to trace to |
| [`inputs/synthetic-pk-analysis-plan.md`](inputs/synthetic-pk-analysis-plan.md) | The governing plan — acceptance criteria, exclusion rules, BLQ handling, which summary statistic applies |
| [`inputs/synthetic-exclusion-and-run-log.md`](inputs/synthetic-exclusion-and-run-log.md) | Which profiles were excluded, why, and against which dataset version |

## Which skill runs

[`skills/verify-nca-outputs`](../../skills/verify-nca-outputs/) — the reviewer
side of the NCA dual-control pattern.

## Two ways to run it

**In an agent host** — install the library, attach the four files from
[`inputs/`](inputs/), and ask:

> Verify the NCA report against the parameter dataset and the analysis plan.
> Report every traceability, unit, rule-conformance and summary-statistic finding
> with its locator. Do not re-derive anything.

**In a plain chat window, no install** — paste
[`skills/verify-nca-outputs/PASTE.md`](../../skills/verify-nca-outputs/PASTE.md)
into any chat, attach the same four files, and ask the same question.

## What comes back

A finding register with a locator per finding. The fixture has **ten planted
defects** and a competent run surfaces them as findings, not as conclusions:

| Class | What it looks like here |
|---|---|
| **Traceability** | Table 3 reports `AUC0-inf 2420` for `SYN-104` where the dataset says `2240` — 8% apart against a 0.5% plan tolerance, and the reported `CL/F` corresponds to the dataset value, not the reported one |
| **Unit inconsistency** | One row gives `CL/F` in `mL/h` where every other row and the plan say `L/h` — a 1000-fold swap |
| **Rule conformance** | A profile excluded for "outlying exposure" when the plan's exclusion criteria are exhaustive and explicitly exclude exposure magnitude; another profile that **meets** an exclusion criterion and was retained |
| **Summary statistic** | An `AUC0-inf` row headed "geometric mean" whose footnote says it was computed arithmetically; an `n = 8` where the exclusion log says seven profiles contributed |
| **Provenance** | The report cites dataset `v1.0`; the run baseline declares `v2.0` authoritative, and `v2.0` re-fitted three terminal-phase regressions |

The expert key that enumerates all ten lives with the evaluation suite at
`evals/verify-nca-outputs/fixtures/EXPERT-KEY.md`. **It is deliberately not
copied here** — an example that ships its own answer key tests nothing.

## What it will refuse to do

Verbatim from the skill's contract:

- Rerun the NCA, or re-derive any parameter from concentration data
- Edit the parameter dataset, the exclusion log, or the NCA report
- Add, remove, or re-justify an exclusion
- **Decide which of two conflicting values is scientifically correct**
- Select, adjust or justify a dose
- Draw an efficacy or safety conclusion
- Interpret a PK finding as a safety signal

That fourth line is the one that matters. The skill's job is to tell you `2420`
and `2240` disagree and show you where each came from. Which one is right is a
pharmacokineticist's call, and the tool does not make it.
