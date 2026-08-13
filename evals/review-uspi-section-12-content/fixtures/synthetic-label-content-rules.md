# SYNTHETIC — Labelling clinical pharmacology content rules and version baseline

> Fully synthetic restatement of a required-content list and phrasing
> conventions, supplied so this fixture is self-contained. This is the **rule
> source** for the quilaxatan draft: conformance is judged against this file, not
> against a guidance document held elsewhere.
>
> Anchors are referenced by ID only — `cfr-201-57-c-13` for required content and
> `fda-labeling-cp` for format and phrasing. No date is written here.

## 1. Required Section 12 content (`cfr-201-57-c-13`)

| # | Required element |
|---|---|
| L1 | 12.1 Mechanism of Action |
| L2 | 12.2 Pharmacodynamics |
| L3 | 12.3 Pharmacokinetics |
| L4 | 12.3 — **Absorption** |
| L5 | 12.3 — **Distribution** |
| L6 | 12.3 — **Elimination**, including metabolism and excretion |
| L7 | 12.3 — **Specific Populations**, wherever the label makes a population-specific statement elsewhere in the document |
| L8 | 12.3 — **Drug Interaction Studies** |

L7 applies here: the draft makes renal and hepatic statements in Sections 8.6 and
8.7, so a Specific Populations subsection is required content, not optional.

**Pediatric pharmacokinetics is not applicable to this product** and its absence
is not a required-content gap.

## 2. Conventional ordering of the 12.3 elements (`fda-labeling-cp`)

**Absorption → Distribution → Elimination → Specific Populations → Drug
Interaction Studies.**

An element presented out of this order is an ordering deviation, reported as a
deviation and never rewritten.

## 3. Excluded phrasing in a pharmacokinetics section

The following are conclusion language and are excluded from Section 12:

- "no clinically meaningful differences"
- "clinically insignificant"
- "well tolerated"
- "comparable efficacy"

A statement that a difference exists is a pharmacokinetic statement. A statement
that the difference does not matter is a conclusion, and belongs to the reviewing
division and the labelling owner, not to Section 12.

## 4. Dispersion, units and precision conventions

| Quantity | Convention |
|---|---|
| Exposure parameters (AUC, Cmax) | **geometric mean (CV%)** |
| Half-life | arithmetic mean, hours |
| Clearance | L/h |
| Ratio statements | point estimate **with its 90% confidence interval** |

`mean (SD)` is **not** the convention for an exposure parameter in Section 12.3.

## 5. Predictive and unsupported qualifiers

A statement that an effect "is expected to be", "is unlikely to be", or "should
not be" something is a prediction. It is permitted only where a supplied source
states the prediction and its basis. Where the supplied source records that a
population or condition **was not evaluated**, a predictive qualifier about it is
an unsupported qualifier.

## 6. Source-version baseline

| Value class | Authoritative source and version |
|---|---|
| Steady-state exposure parameters | CSR QLX-101, Table 14.2.1 |
| Interaction ratio statements | Statistical output, Study QLX-107 |
| Renal population statements | **Population PK Report QLX-PPK-002 v2.0** |
| Hepatic impairment statements | CSR QLX-105, Table 14.2.3 |
| Submission summary reference | Module 2.7.2, version 1.0 |

`QLX-PPK-002 v2.0` supersedes v1.0. A label citing v1.0 is citing a superseded
analysis output, independent of whether the cited number happens to agree.
