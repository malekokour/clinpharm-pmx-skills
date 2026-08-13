# ADC Analyte Strategy Review

**Give it the analyte definitions, the exposure questions and the reported
parameters for an antibody-drug conjugate. It returns where the same analyte name
means different things in different documents, which stated questions the analyte
set cannot answer as planned, and where reported values contradict each other.**

A qualified clinical pharmacologist decides what to do about each one.

## The failure this exists for

It is not a wrong number. It is **the same word meaning different things**.

"Total antibody", "conjugated antibody", "ADC", "total payload", "free payload" —
these are defined per programme. A protocol, a bioanalytical plan and a CSR can
each use one of them differently while every individual document reads perfectly
well. Nobody notices until someone compares two numbers believing they measure
the same thing.

That is why definition drift **between two reporting documents** is Critical here,
while drift against a superseded IB is Major. The severity tracks who is likely
to compare what.

## What you get

| Output | Contents |
|---|---|
| Analyte definition register | Every analyte, verbatim definition, locator, per document |
| Question-to-analyte coverage matrix | Each stated question against the analytes that bear on it |
| Cross-analyte consistency table | Containment ordering and unit checks with both locators |
| Drift summary | Every conflicting definition preserved in full, none resolved |
| Human-review record | Named owner; every disposition arrives `open` |

## The input people forget

**The programme's exposure questions.** "Is this analyte set adequate?" has no
answer in the abstract — only against the questions the programme has committed
to. Without them the skill marks coverage `NEEDS_INPUT` rather than assessing
adequacy against questions it invented.

## What it will not do

Select or recommend an analyte strategy. Decide whether an analyte is
scientifically necessary. Harmonise two conflicting definitions — both are
recorded verbatim with both locators, because the more plausible one is not
reliably the intended one. Judge whether a ratio or DAR shift is biologically
reasonable.

The consistency script checks **ordering and units**, which are properties of the
numbers. It does not know what a reasonable conjugated-to-total ratio looks like,
and it is built so it cannot pretend to.

## Status

**`built`, not `released`.** No benchmark run has been published, so no
performance claim should be made about it.

## Related skills

| If you actually want | Use |
|---|---|
| Assay validation and method performance | `review-bioanalytical-report` |
| The CSR's PK content as a whole | `review-csr-pk-consistency` |
| Protocol PK sections | `review-protocol-pk-sections` |
| Parameter derivation | `verify-nca-outputs` |

Licensed MIT.
