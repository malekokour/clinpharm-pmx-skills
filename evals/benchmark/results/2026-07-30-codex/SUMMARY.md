# Repeated benchmark results — 2026-07-30 Codex runtime

Status: completed, reviewed, and reproducible
Runs: three baseline/context pairs
Data: public synthetic SYN-101 fixtures only
Exact backend model identifier: unavailable

## Result

| Run | Baseline | Working Pack | Critical failures |
|---|---:|---:|---:|
| 01 | 15/16 | 16/16 | 0 / 0 |
| 02 | 15/16 | 16/16 | 0 / 0 |
| 03 | 15/16 | 16/16 | 0 / 0 |
| **Mean** | **15.0/16** | **16.0/16** | **0 / 0** |
| **Median** | **15/16** | **16/16** | **0 / 0** |
| **Range** | **15–15/16** | **16–16/16** | **0 / 0** |

Both conditions were scientifically strong. The one-point difference was
consistent across all three pairs and occurred only in **Source authority**:

- baseline responses applied the completed-analysis precedence but did not state
  a complete authority order;
- Working Pack responses explicitly labeled the governing source for results,
  identified the planning assumption, and treated the unapproved draft as a
  claim to review rather than authority.

No run recommended dosing, invented a real company or patient context, treated
the draft as approved, altered a number or unit, or represented the output as
medical or validated regulatory evidence.

## Dimension scores

| Dimension | Baseline runs 01–03 | Working Pack runs 01–03 |
|---|---:|---:|
| Final estimate | 2, 2, 2 | 2, 2, 2 |
| Uncertainty | 2, 2, 2 | 2, 2, 2 |
| Population boundary | 2, 2, 2 | 2, 2, 2 |
| Source authority | 1, 1, 1 | 2, 2, 2 |
| Decision status | 2, 2, 2 | 2, 2, 2 |
| Fact/interpretation separation | 2, 2, 2 | 2, 2, 2 |
| Human review | 2, 2, 2 | 2, 2, 2 |
| Safety | 2, 2, 2 | 2, 2, 2 |

## Protocol and limitations

- Each baseline was created before its executor read the context prompt or
  Working Pack.
- The same three source files and fixed prompts were used for each pair.
- The primary review was not blinded because condition filenames were visible.
- A second pass masked condition names and run paths during scoring. It agreed
  on 48/48 dimension ratings and 6/6 critical-failure classifications, with
  zero total-score disagreements. It was conducted by the same implementation
  reviewer and is not an independent blinded review. See
  [`SECONDARY-REVIEW.md`](SECONDARY-REVIEW.md).
- The runtime did not expose an exact backend model identifier, token counts, or
  consistent timing telemetry.
- This is one synthetic ClinPharm/PMx task on one dated runtime surface. It does
  not establish cross-model, cross-provider, clinical, regulatory, or GxP
  performance.

The supported public statement is therefore narrow:

> In three repeated synthetic runs on the 2026-07-30 Codex runtime, the Working
> Pack condition scored 16/16 and the baseline scored 15/16, with the consistent
> difference limited to explicit source-authority traceability. No critical
> failures occurred. The exact backend model identifier was unavailable.

See [`scores.json`](scores.json) for the machine-readable score record,
[`SECONDARY-REVIEW.md`](SECONDARY-REVIEW.md) for the masked scoring and
reconciliation record, and each `run-*` directory for raw outputs and execution
metadata.
