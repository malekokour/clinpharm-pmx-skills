# Human PK Prediction Review

**Give it a PBPK report, an IVIVE memo or an allometric scaling analysis. It returns
which assumptions the prediction actually depends on but never states, which inputs
are predicted while being presented as measured, and whether the platform
qualification it cites covers the use it is being put to.**

A qualified pharmacometrician or clinical pharmacologist decides what to do about
each one.

## A prediction is an argument, not a measurement

There is no human data yet. That is the whole point of the deliverable, and it
changes what a review can even mean.

For an analysis of observed data you can ask whether the model fits. For a
prediction you cannot. What you *can* ask is whether the argument is complete:
does every number in the result trace to a stated input, is every assumption the
calculation depends on actually written down, and does the qualification evidence
cover this compound rather than some other one.

This skill checks the argument. **It never decides whether the prediction is
right** — that is the reviewer's judgment and it needs biology this tool does not
have.

## The finding it exists to produce

An **operative-but-undeclared assumption**: something the result depends on that
appears nowhere in the methods. A scaling exponent that shows up only in the
answer. A fraction unbound taken from a different species than the text says. A
protein-binding correction applied silently.

None of these is necessarily wrong. Several are standard practice. But a reviewer
who does not know they are there cannot weigh them, and a regulator who finds one
later will ask why it was not stated.

## What you get

| Output | Contents |
|---|---|
| Assumption register | Every assumption as declared-and-used, declared-not-used, or **operative-not-declared** |
| Input traceability matrix | Each parameter against its inputs, with a measured-or-predicted flag |
| Recomputation table | Every scaling relation that could be recomputed, with deviation against tolerance |
| Qualification scope note | The cited package against this use — including `scope-not-stated`, which is common |
| Human-review record | Named owner; every disposition arrives `open` |

## What it will not do

Build or refit a model. Supply an input the deliverable does not state — a missing
fraction unbound is `NEEDS_INPUT`, never 0.05 because that is typical. Decide
whether a prediction is plausible. Select a first-in-human dose.

Supplying a plausible input would turn a review into an analysis, and the output
would then contain a number nobody claimed.

## Status

**`built`, not `released`.** No benchmark run has been published, so no
performance claim should be made about it.

## Related skills

| If you actually want | Use |
|---|---|
| An analysis of observed clinical data | `review-model-analysis-deliverable` |
| The first-in-human dose argument | `review-fih-dose-rationale` |
| Assay validation behind the in vitro inputs | `review-bioanalytical-report` |

Licensed MIT.
