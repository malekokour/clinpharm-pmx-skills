# Exposure Safety Margin Review

**Give it the documents that state safety margins and the exposures behind them.
It returns which margins never say what they are a ratio of, which compare two
things that cannot be compared, and which do not reconcile with the exposures
they cite.**

A qualified clinical pharmacologist and toxicologist decide what to do about each
one.

## A margin is a ratio with a hidden contract

"12-fold" means nothing on its own. Twelve-fold of what — AUC or Cmax? Which
species, which sex, which study? Total or unbound? At which clinical dose level?

That contract is usually implicit, and a margin whose two sides answer different
questions still looks like a number. The common shapes:

- **metric mismatch** — nonclinical AUC against clinical Cmax
- **binding mismatch** — total on one side, unbound on the other
- **species drift** — most-sensitive species in one document, a different one elsewhere
- **dose-level drift** — computed at one dose, restated against another after a change

None is visible from the ratio.

## What it will never tell you

**Whether a margin is adequate.** That depends on the nature of the toxicity, how
monitorable it is, and whether it reverses — a judgment shared between clinical
pharmacology, toxicology and clinical safety. This skill checks whether the number
means what it says it means.

It also will not reconstruct an unstated basis. A margin that does not name its
species is reported as `basis-not-stated`, never as "presumably rat". Inferring
the contract is exactly how a review invents the thing it was meant to check.

## What you get

| Output | Contents |
|---|---|
| Margin register | Every margin verbatim, its claimed basis, locator, and whether the basis is fully stated |
| Comparability table | Each margin's two sides, classified, with both locators |
| Recomputation table | Stated against recomputed, with deviation and tolerance |
| Basis-drift summary | Margins stated differently across documents, all bases preserved |
| Human-review record | **Two** named owners — CP and toxicology — every disposition `open` |

## The shipped script refuses before it divides

`margin_check.py` checks comparability *first*. If the metrics, binding bases or
units differ, it reports `INCOMPARABLE` and does not compute a ratio.

Dividing two numbers is trivial; the failure worth catching is a margin whose
sides answer different questions, and a script that divided them anyway would
launder that defect into a confident number.

Self-tested 5/5, including both mismatch shapes.

## Status

**`built`, not `released`.** No benchmark run has been published, so no
performance claim should be made about it.

## Related skills

| If you actually want | Use |
|---|---|
| The first-in-human dose argument | `review-fih-dose-rationale` |
| Effects tabulated for benefit-risk | `structure-benefit-risk-effects-table` |
| The IB's PK section as a whole | `check-investigators-brochure-pk-section` |

Licensed MIT.
