# Held pending adjudication — not part of the release gate

`build-work-context` is the repository's **one `released` package**. This directory
holds an execution-layer fixture, expert key and case authored for it on
2026-08-06, which are **deliberately not wired into the suite**.

## Why they are held rather than shipped

`validate_repo` refused the combination, correctly:

```
- build-work-context: status 'released' but its expert key's severities are still
  'provisional' — no promotion may rest on a denominator that has not been adjudicated
```

The rule is right and the situation it caught is real. `build-work-context` earned
`released` against its original seven cases. This material adds a defect-detection
claim that has **never been run and whose severities have never been adjudicated**.
Leaving it in the live suite would make the package's `released` status broader than
its evidence — and `released` carrying an `evidence_gap` is separately forbidden.

## Decision taken 2026-08-06 — the package stays `released`

This was left open once as an owner decision. On inspection it is not one, and
deferring it was wrong.

`build-work-context` earned `released` against the **nine cases in its live suite**,
and those are untouched. This material was never part of that gate — it is held here
precisely so it isn't. Adding unevaluated material beside a package cannot
retroactively invalidate evidence the package already earned, and `validate_repo`
agrees: the tree passes with the material held.

So: **the package remains `released`, and this material remains held.** Nothing about
its public claim changes, and nothing is misrepresented in either direction.

The held case *was* run on 2026-08-06 and scored **2/4 Critical, 1/4 Major, 0/1
Minor** against a provisional key. That result is **input to a future adjudication,
not a gate outcome** — it cannot promote the package (the key is `provisional`, which
the validator hard-blocks) and it cannot demote it (the case is not part of the
release gate). Recorded here so the number is not later mistaken for either.

What genuinely remains an owner decision is narrower than "adjudicate or downgrade":



1. **Adjudicate these severities and wire the case in.** The `released` claim then
   genuinely widens to cover defect detection, which it does not today.
2. **Leave it held indefinitely.** Also legitimate — the package's claim is honest
   without it.

Either way the package's current status is correct, which is why the decision does
not block anything. The material is preserved intact, the released package's evidence is exactly
what it was when the gate passed, and nothing is misrepresented in either direction.

The `_` prefix follows this repository's convention for provenance held outside the
live tree, and is why the enumeration and key-status checks skip it.

## What is here

- `EXPERT-KEY.md` — **12** planted defects, `severity_status: provisional`
- `10-execution-planted-defects.yaml` — the execution case, which asserts **9**
  of the 12 mechanically and covers the remaining three (D5, D9, D12) in its
  judged assertions. The earlier count of 9 here read the case's defect
  assertions and reported them as the key's planted defects; the two numbers
  are different quantities and only the key fixes the recall denominator
- `planted-*.md` — the synthetic source documents the defects live in

Grounding was verified before the move: every `observed`/`expected` value appears
verbatim in the fixture documents.
