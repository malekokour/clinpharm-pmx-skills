# Worked example — reviewing a draft US Prescribing Information

**Input shape: regulatory.** A draft label section, the sources its numbers are
supposed to come from, and the content rules that govern it.

Everything here is **synthetic**. `Quilaxatan`, studies `QLX-101` through
`QLX-107`, and every value are invented for demonstration and testing. This is
not a real product, not real labelling, and carries no regulatory meaning.

## What you feed it

| File | What it is |
|---|---|
| [`inputs/synthetic-uspi-draft.md`](inputs/synthetic-uspi-draft.md) | The draft label — Section 12, plus the quantitative statements in 2, 7 and 8 |
| [`inputs/synthetic-module-272-extract.md`](inputs/synthetic-module-272-extract.md) | The summary of clinical pharmacology the label should agree with |
| [`inputs/synthetic-source-values.md`](inputs/synthetic-source-values.md) | The study outputs behind the numbers, with their versions |
| [`inputs/synthetic-label-content-rules.md`](inputs/synthetic-label-content-rules.md) | The content rules — required subsections, excluded phrasing, element ordering |

## Which skill runs

[`skills/review-uspi-section-12-content`](../../skills/review-uspi-section-12-content/) —
reviews Section 12 and the quantitative basis of Sections 2, 7 and 8 against
21 CFR 201.57(c)(13) and the clinical pharmacology labelling guidance.

## Two ways to run it

**In an agent host** — attach the four files from [`inputs/`](inputs/) and ask:

> Review the draft Section 12 against the supplied sources and content rules.
> Report untraced claims, numeric mismatches, contradictions, excluded phrasing
> and missing required content, each with its locator. Do not propose label text.

**In a plain chat window, no install** — paste
[`skills/review-uspi-section-12-content/PASTE.md`](../../skills/review-uspi-section-12-content/PASTE.md),
attach the same four files, ask the same question.

## What comes back

A finding register with a locator per finding. The fixture carries **ten planted
defects** across the classes this workflow exists to catch:

| Class | What it looks like here |
|---|---|
| **Untraced claim** | The label states a plasma protein binding percentage. **No supplied source reports protein binding at all** — the CSR table and Module 2.7.2 both say so explicitly. This is the finding the workflow exists for |
| **Numeric mismatch** | A steady-state `AUC0-24` in the label that is 24% away from the value both the CSR and Module 2.7.2 give — a digit transposition |
| **Direction reversal** | Section 7.1 says a strong CYP3A4 inhibitor *decreased* exposure 2.6-fold; the statistical output gives a ratio of 2.61, an **increase**. Sections 2.3 and 12.3 both assume the increase, so **the label also contradicts itself** |
| **Required content absent** | Section 12.3 carries no Specific Populations subsection while Sections 8.6 and 8.7 make renal and hepatic statements — required content, not optional |
| **Excluded phrasing** | "No clinically meaningful differences" in a pharmacokinetics section, where the supplied ratio is 1.42 and the label does not state it |
| **Unsupported qualifier** | "Renal clearance is expected to be unaffected" in mild impairment — a population the analysis records as **not evaluated**, with no participants enrolled |
| **Stale source version** | The label cites a population PK report `v1.0`; the baseline declares `v2.0` authoritative, and `v2.0` revised the clearance covariate model |

The expert key enumerating all ten lives with the evaluation suite at
`evals/review-uspi-section-12-content/fixtures/EXPERT-KEY.md`, **deliberately not
copied here**.

## What it will refuse to do

Verbatim from the skill's contract:

- **Draft, reword, redline, or propose label text**
- Take a position in a labelling negotiation, or predict what an agency will accept
- Draft or advise on a response to an agency labelling comment
- Release label text beyond the minimum span needed to locate a finding
- Edit the draft label, or apply a correction
- Decide which of two conflicting values is scientifically correct
- Select, adjust or justify a dose, or propose a dose modification for Section 2

The first and last lines are the point. It will tell you Section 7.1 states the
interaction backwards and show you the ratio that proves it. It will not write
the corrected sentence, and it will not tell you what to do about Section 2.3.
Labelling text is a regulatory act with an owner.
