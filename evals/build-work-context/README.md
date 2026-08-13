# Evaluation suite — build-work-context

Layout per the project's evaluation-suite decision (PS-D028): `suite.yaml`,
one file per case under `cases/`, `fixtures/`, `rubric.md`, and this README.
Suite version 0.1.0.

## What this suite proves

| Layer | Cases |
|---|---:|
| execution | 4 |
| activation | 2 |
| portability | 1 |
| safety | 2 |
| **total** | **9** |

**44 assertions — 1 mechanical, 43 judged.**

An execution-layer fixture, expert key and case were authored for this package on
2026-08-06 and are **held out of the suite** at
[`_pending-adjudication/`](_pending-adjudication/README.md). They are not counted
above and make no claim about this package, because wiring a `provisional` expert
key into the repository's one `released` suite would widen its claim past its
evidence.

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

5 file(s): `prompt-injection-source.md`, `stale-context.md`, `unsupported-docx-host.md`, `update-existing-context.md`, `update-new-note.md`


## Running it

```bash
python3 scripts/eval_workspace.py stage evals/build-work-context --workspace <ws> --runs 3
# executor fills each run's outputs/response.md, outputs/metrics.json, timing.json
python3 scripts/eval_workspace.py check <ws>
python3 scripts/eval_grade.py <ws>/eval-<case>/with_skill/run-1 \
    --case evals/build-work-context/cases/<case>.yaml --write
python3 scripts/eval_benchmark.py <ws> --skill-name build-work-context
```

Staging creates both conditions together and records a provenance file per run
(case hash, fixture hashes, whether the skill was present), so a run cannot
later be confused about which condition produced it.
