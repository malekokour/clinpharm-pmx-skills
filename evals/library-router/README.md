# Library router — selection cases

What this directory holds and, just as importantly, what it does not.

## What it is

`selection-cases.json` is a set of deterministic cases for
[`scripts/library_router.py`](../../scripts/library_router.py). Each case gives
an utterance and a settings profile, and states what the router must return:
a package identifier, an `ask`, or a `refuse`.

Run them:

```bash
python3 scripts/check_router_selection.py --verbose
```

They also run inside `make check`, so a scoring change that breaks selection
fails the build.

## What it is not

There is deliberately **no `suite.yaml` here**, and this is not an oversight.

A `suite.yaml` declares a PS-D028 evaluation: model runs, graded against a
rubric, with recall and precision thresholds. `library-router` has not had one
of those, and writing the file would announce evidence that does not exist.
[`scripts/validate_repo.py`](../../scripts/validate_repo.py) requires a suite of
`released` packages only; `library-router` is `built`, so the absence is the
honest state and the validator agrees.

The distinction matters because the two answer different questions:

| Question | Answered by | Needs a model? |
|---|---|---|
| Are the eval suites well formed? | `scripts/eval_suite_check.py` | No |
| Do the declared scopes partition? | `scripts/check_routing.py` | No |
| **Which package does the router return?** | **`scripts/check_router_selection.py`** | **No** |
| Does the skill do its job well? | a PS-D028 suite (not yet written) | Yes |

Only the last one is missing, and `library-router`'s `evidence_gap` in
[`collections/utilities/collection.json`](../../collections/utilities/collection.json)
says so.

## What the numbers mean

The runner prints denominators rather than adjectives:

```
Router selection: 42 case(s) across 7 profile(s), registry of 22 package(s)
  top-1 accuracy (SINGLE class): 21/21 = 100%
```

`21/21` is every package in the registry except `library-router` itself — one
unambiguous request each. It is **not** a claim about arbitrary user phrasing.
Each utterance was authored to be clearly about one package; the honest reading
is *"when a request names one package plainly, the router finds it"*, and the
`AMBIGUOUS` / `MULTI` cases exist because plainly-named is not the only kind of
request that arrives.

## Profiles

Cases run against the shipped defaults plus six overlays, because several of the
things worth checking are properties of *configuration* rather than of scoring:

- `shipped` — recommend-and-confirm, no auto-select, `released` only. Under this
  profile every `SINGLE` request correctly returns `ask`, which is why the
  accuracy figure above is measured under `auto`.
- `auto_released_only` — the status guard: a `built` package is identified but
  not auto-run.
- `manual_only`, `auto_csr_disabled`, `force_ddi`, `force_ddi_disabled` —
  operator preferences, including two contradictory configurations that must
  fail closed.

## Proving the gate can fail

A gate nobody has watched go red is untested. Change any `expect.chosen` to a
different package id and re-run: the case reports the expected and observed
value and the runner exits 1. Restore the file for green.

The run that was actually performed, with its output, is recorded under
`_ADMIN/2-Dev/1-Evidence/` in the private workspace.

## Cases that record a defect

Two cases exist because they caught something:

- **`SEL-TOP1-19`** — `review ctd 2.7.2 content`. The prose section number
  tokenised to three one-character fragments and was discarded, so the request
  scored no better on its own package than on three siblings whose identifiers
  also end in `content`.
- **`SEL-REFUSE-06` / `SEL-REFUSE-07`** — `force_skill` was read *before*
  classification, so an operator who had pinned a skill could turn a
  dose-selection or out-of-scope request into a routed one. That contradicted
  [`skills/library-router/SKILL.md`](../../skills/library-router/SKILL.md),
  which states that preferences cannot bypass refuse paths. The ordering was
  corrected; these two cases hold it.
