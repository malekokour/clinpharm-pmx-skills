# Selection service levels

What the router promises, how it is measured, and what happens when it misses. Selection
quality is evidenced **separately** from skill quality: a correct skill that never
activates is still a product failure, and a router that activates confidently on the
wrong package is worse than one that asks.

## The indicators

Measured over the selection suite — 167 top-1 cases, one per job-model row, plus 64
wrong-branch traps, one per subdomain.

| Indicator | What it counts | Target | Why this number |
|---|---|---|---|
| **Top-1 accuracy** | Correct package returned first, on unambiguous cases | ≥ 90% | Below this, users stop trusting the first answer and browse instead — at which point the router is decoration |
| **Wrong-branch rate** | Narrowed to the wrong subdomain | ≤ 2% | The failure users cannot detect. A plausible skill from the wrong branch reads as an answer |
| **Ask rate on ambiguous pairs** | Asked rather than guessed, where two neighbours are genuinely close | ≥ 80% | Asking is the correct behaviour here; a low rate means the router is guessing on ties |
| **Ask rate on clear cases** | Asked when it should not have | ≤ 10% | Ask-fatigue. A router that asks constantly is not a router |
| **Refusal correctness** | Human-only and boundary rows refused with the role named | **100%** | Not a target. A missed refusal is a safety defect, not a quality metric |
| **Alias double-activation** | An utterance activating both an old and a new id | **0** | Structural. Any occurrence is a defect in the alias map |

## Why refusal is 100% and nothing else is

Every other indicator trades off against another. Refusal does not: a skill that answers
a question reserved for a qualified human has crossed the product's only invariant. It
is measured as a count of failures, never as a rate, and a single failure blocks release.

## Error budget

For the rate-based indicators, `(100% − target)` is the budget for a release cycle.

| Budget remaining | Posture |
|---|---|
| > 50% | Ship; keep authoring |
| 25–50% | Increased review on new descriptions and neighbour tables |
| 10–25% | Freeze new packages; fix selection first |
| < 10% | Stop. The catalogue is growing faster than it can be told apart |

Budget is consumed by **adding packages**, not only by regressions — every new
description is a new opportunity for collision. That is deliberate: it makes the cost of
breadth visible while it is being incurred.

## What is measured, and what is not

**Measured:** which package the router returns, whether it asked, whether it refused,
which branch it narrowed to, and the margin between the top two candidates.

**Not measured here:** whether the returned skill produced a good answer. That is the
per-skill evaluation gate and it carries its own thresholds. Conflating the two is how a
library reports selection success while shipping poor reviews.

## When an indicator misses

1. **Do not widen the gate.** A threshold lowered to accommodate a result is no longer a
   threshold.
2. Read the confusion matrix, not the headline. Selection failures cluster — usually two
   descriptions that each cover a job the other also claims.
3. The usual fix is a **description or a split**, not a scoring change. If two packages
   collide because they genuinely do the same job, the separability tests say merge; if
   they do different jobs and read alike, the descriptions are wrong.
4. Record the fix and re-run the whole suite, not the failing case.

## Traces

Every selection persists a trace: the utterance class, the branch narrowed to, the
candidate ids with scores, the decision, and a reason code. Traces are what make the
confusion matrix possible.

**Traces never contain raw user prompts in committed evidence.** The schema is at
`evals/_traces/schema.json`, and the utterance is recorded as a case identifier rather
than its text.

## Publication

The confusion matrix ships publicly with denominators. A selection claim without a
denominator is unfalsifiable, which is the same standard applied to every other count in
this product.
