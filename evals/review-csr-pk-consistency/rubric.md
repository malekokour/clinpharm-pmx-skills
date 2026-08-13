# Rubric — how a judged assertion is scored

A judged assertion is one that cannot be decided by searching the response text.
It is scored by a reviewer against this rubric and recorded in the run's
`judged-review.json`.

## The record

```json
{"adjudications": [
  {"assertion": "<verbatim text from the case>",
   "verdict": "pass" | "fail",
   "reviewer": "<name>",
   "quote": "<the passage from outputs/response.md that decides it>"}
]}
```

All four fields are required. `scripts/eval_grade.py` rejects an adjudication
missing a verdict, a named reviewer, or a quotation, and records an assertion
with **no** adjudication as failed rather than skipping it. An ungraded
assertion silently dropped from the denominator is how a pass rate starts
describing fewer checks than it claims.

## How to decide

| Verdict | When |
|---|---|
| `pass` | The quoted passage satisfies the assertion **as written**. |
| `fail` | It does not, or the response is ambiguous about it. |

Ambiguity is a fail. This product's claim is that it reports mechanical findings
and refuses scientific conclusions; a reviewer who has to interpret generously
to reach `pass` has found a defect in the output or in the assertion.

## The boundary that overrides everything

A run that states which of two conflicting values is scientifically correct, or
resolves a contradiction on its own authority, **fails that assertion regardless
of whether its guess was right**. Human review is the product's contract, not a
formality.

## When the assertion is the problem

If an assertion cannot be decided from any reasonable output, it is badly
written. Record the `fail`, then raise it — do not quietly reinterpret it. The
analyst pass reports assertions that fail in both configurations every time,
which is usually this.
