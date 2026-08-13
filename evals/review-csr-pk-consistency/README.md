# Evaluation suite — review-csr-pk-consistency

Layout per the project's evaluation-suite decision (PS-D028): `suite.yaml`,
one file per case under `cases/`, `fixtures/`, `rubric.md`, and this README.
Suite version 0.1.0.

## What this suite proves

| Layer | Cases |
|---|---:|
| activation | 2 |
| execution | 7 |
| portability | 1 |
| safety | 4 |
| **total** | **14** |

**62 assertions — 10 mechanical, 52 judged.**

Mechanical assertions are decided by searching `outputs/response.md`; a miss is
unambiguous and a script-path miss is a script bug. Judged assertions are scored
by a reviewer against [`rubric.md`](rubric.md) and must carry a quotation.

Most assertions are judged today. That is deliberate rather than unfinished:
`_Protocol.md` step 6 draws objective assertions **after** inspecting initial
outputs, so converting them before any run exists would be fitting assertions to
a guess about phrasing.

## Thresholds

| | |
|---|---|
| recall | declared in P04; no threshold is claimed before a run |
| precision | declared in P04; no threshold is claimed before a run |
| missed Critical allowed | 0 |

**No threshold is claimed before a run.** A number here would be a target, and
writing a target where a measurement belongs is how `built` becomes `released`
without evidence.

## Fixtures

11 file(s): `EXPERT-KEY.md`, `SECONDARY-CONSUMER-KEY.md`, `injected-source.md`, `synthetic-analysis-plan.md`, `synthetic-csr-body.md`, `synthetic-csr-pd-biomarker-trace.md`, `synthetic-csr-synopsis.md`, `synthetic-nca-output.md`, `synthetic-protocol.md`, `synthetic-tlf.md`, `synthetic-topline-route-selection.md`
The expert key is never supplied to the model under evaluation.

Cases 13 and 14 use the provisional secondary-consumer key. They prove the
CSR-local PD loading contract and the local-versus-programme topline routing
contract, not MEDIUM behavioral qualification.

## Running it

```bash
python3 scripts/eval_workspace.py stage evals/review-csr-pk-consistency --workspace <ws> --runs 3
# executor fills each run's outputs/response.md, outputs/metrics.json, timing.json
python3 scripts/eval_workspace.py check <ws>
python3 scripts/eval_grade.py <ws>/eval-<case>/with_skill/run-1 \
    --case evals/review-csr-pk-consistency/cases/<case>.yaml --write
python3 scripts/eval_benchmark.py <ws> --skill-name review-csr-pk-consistency
```

Staging creates both conditions together and records a provenance file per run
(case hash, fixture hashes, whether the skill was present), so a run cannot
later be confused about which condition produced it.
