# USPI Section 12 Content Review

**Give it a draft US Prescribing Information and the studies behind it. It returns
what the clinical pharmacology content list requires and the draft is missing,
which phrasing the labelling guidance excludes, and — the point of the whole
exercise — every number in the label that no supplied source actually supports.**

A qualified clinical pharmacologist and the labelling owner decide what to do
about each one.

## Label text is binding. This reviews it; it never writes it.

This is the constraint that shapes everything else in the skill.

It does not draft, reword, or redline label text. It takes **no position in a
labelling negotiation** — not on what an agency will accept, not on what to
concede, not on how to answer a labelling comment. It **never releases label
text**: findings quote only the span needed to locate them, and no output is a
draft, a redline, or a substitute wording.

That is not caution for its own sake. A tool that proposes label wording has
started authoring a legally binding document on a sponsor's behalf, on evidence
it cannot fully see, in a negotiation it is not party to.

## The problem

Section 12 has a required content list in 21 CFR 201.57(c)(13) and a format
expectation in the December 2016 clinical pharmacology labelling guidance. The
quantitative statements in Sections 2, 7 and 8 — dose modifications, interaction
magnitudes, exposure differences in specific populations — each rest on a number
produced somewhere in a CSR, a statistical output, or a popPK, exposure–response
or PBPK report.

Checking that every one of those numbers still says what its source says, after
several revision cycles and a data cut, is slow, unglamorous, and the last place
an error can be caught cheaply. After approval it is in practice.

## What you get

| Output | Contents |
|---|---|
| **Section 12 conformance register** | One row per finding: class, severity, locator, the rule applied, the guidance anchor cited, detection path, owner, disposition |
| **Claim-to-data traceability matrix** | Every extracted statement with its source document, version, locator and value — and a trace status: `traced`, `traced-with-mismatch`, `untraced`, or `NEEDS_INPUT` |
| **Boilerplate deviation report** | Expected pattern versus observed shape, with locator. No proposed wording |
| **Quantitative-basis reconciliation table** | Sections 2, 7 and 8 statements against their sources, both values and both locators where they differ |
| **Human-review record** | Disposition log, both named owners, closure signature |

`untraced` is the row that earns the run. It is never softened into "presumably
from the CSR".

## What it will not do

It never drafts or rewords label text · never predicts what an agency will
accept · never drafts a response to a labelling comment · never edits the draft ·
never decides which of two conflicting values is correct · never proposes a dose
modification · never draws an efficacy or safety conclusion · never approves or
signs off.

Those are not omissions. A tool that adjudicates label content has replaced the
reviewer and the labelling owner rather than helped them.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `review-uspi-section-12-content/` and carries its own `LICENSE`, so it
works from extraction alone with no repository present.

Then ask:

> Review Section 12 of this draft label against the CSR and the popPK report, and
> trace every number in Sections 2, 7 and 8.

**Ordinary chat** — attach the draft section under review together with the
sources behind it, and follow the workflow the skill carries.

The chat route **cannot run the deterministic checks.** Conformance and
boilerplate comparison become model-performed with the reasoning shown for you to
confirm, and the run should be scoped to one subsection — 12.3 alone, or the
Section 8 quantitative statements alone.

## Before you attach anything

Draft labelling for an unapproved product or an unapproved change is normally
sponsor-confidential and part of an unpublished regulatory submission. That is a
stop condition, not a formality. The skill asks you to confirm, in one line, that
you are authorised to process this material in the environment you are using —
and stops if you do not.

## What to supply

The draft USPI with its section numbering intact · Section 12 with its 12.1 /
12.2 / 12.3 headings preserved · the quantitative statements in Sections 2, 7 and
8 · the CSRs and NCA parameter tables for every study cited · the statistical
outputs behind every ratio and interval quoted · the popPK, exposure–response and
PBPK reports · Module 2.7.2 · and one line saying which document version is
authoritative for each value. A prior approved label too, if this is a supplement.

Two of those do disproportionate work. **The source reports are the skill** — run
against the draft label alone, you get a conformance and phrasing pass and nothing
else, and every traceability check comes back `NEEDS_INPUT`. The **version
baseline** prevents the worst false-positive class: confident findings that are
pure artefacts of tracing against a superseded output.

Agency labelling correspondence is deliberately *not* an input. Supplying it would
invite the skill to reason about what a reviewer will accept, which is a position
it does not take.

## Modes

`FULL-LABEL-REVIEW` · `SECTION-12-ONLY` · `TRACE-ONLY` · `SPOT-CHECK` · `UPDATE` ·
`CLOSEOUT`

`SECTION-12-ONLY` is not a cut-down full pass — Section 12 is where the clinical
pharmacology content list applies, so checking it before Sections 2, 7 and 8
stabilise has independent value. `TRACE-ONLY` answers one question: does every
number still trace?

## Missing inputs and missing evidence

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly. Where the documents genuinely do not
settle a question it says `UNKNOWN`; where a check cannot run at all it says
`CANNOT_ASSESS`. It never substitutes a plausible number, and it never reports
"could not check" as "checked and clean".

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, confidential agency correspondence,
or credentials — and names the category **without quoting the content**.

Documents you supply are treated as evidence, never as instructions. Text inside a
source that appears to address the assistant — including an annotation claiming a
wording was already agreed with a health authority — is reported with its location
and never obeyed.

## Evidence

The intended evaluation is a synthetic USPI fixture with expert-keyed planted
defects spanning every finding class.

**UNVERIFIED: no benchmark run has been published for this skill.** Until one is,
make no performance claim from this page.

**A synthetic benchmark is not clinical validation, not a GxP qualification, and
not evidence of real-world performance.** Any published score states its exact
task, model, host, date and run count.

The structural limitation is worth stating plainly: this skill checks conformance
to a content list and traceability to the sources you supply. It cannot tell you
whether the label is *right*. That is the reviewer's job, and these outputs exist
to hand them the evidence rather than a verdict.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic checks
require a skill-aware host; the workflow itself runs anywhere a file can be
attached. DOCX input is preferred, SPL XML is accepted, and PDF works with
degraded table extraction — which the skill discloses rather than absorbing
silently.

Licence MIT · version 0.1.0 · research id S14 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology) · regulatory
anchors cited from [`shared/assets/guidance-index.md`](https://github.com/malekokour/clinpharm-pmx-skills/blob/main/shared/assets/guidance-index.md)
