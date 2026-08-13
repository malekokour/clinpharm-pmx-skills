# CTD 2.7.2 Content Review

**Give it a draft Summary of Clinical Pharmacology Studies, the two summaries
next to it, and the study index. It returns what is missing from the five-part
structure, every place the dose disagrees with 2.7.3 or 2.7.4, and every study
filed in the wrong Module 5 section.**

A qualified reviewer decides what to do about each one. This skill finds them; it
does not rewrite the summary, and it does not decide which dose is right.

## The problem

Module 2.7.2 is where a whole clinical pharmacology programme is compressed into
one summary — and it is read by people who will never open the CSRs behind it. Its
structure is fixed, its dose content has to agree with the efficacy and safety
summaries beside it, and every study it describes has to be filed where its
primary objective says it goes.

Those three checks are usually done by eye, late, under dossier-freeze pressure.
A dose that disagrees between 2.7.2 and 2.7.4 does not stay in the dossier — it
travels into the label and into the first agency question.

## Who owns 2.7.2 — read this before you use it

That clinical pharmacology authors and owns Module 2.7.2 is a **practice
convention**. No FDA, EMA or ICH text in this repository's guidance index assigns
2.7.2 authorship or accountability to any function. ICH M4E(R2) fixes what the
section contains; it says nothing about who writes it.

So the skill treats the accountable owner as a **configurable input you supply**,
confirmed at the start of every run, and it labels every place the workflow leans
on the convention as `PROVISIONAL-PRACTICE`. If you cannot state an owner, it
proceeds and marks every finding `owner: UNCONFIRMED` rather than inserting a
default. It will not tell you that a guidance made clinical pharmacology
responsible, because none did.

This is the reason the skill was held back rather than shipped with the first
wave. Getting ownership wrong in a review artifact sends findings to the wrong
desk, and an assumed owner is invisible until it has already happened.

## What you get

| Output | Contents |
|---|---|
| **Content-review register** | One row per finding: both statements, both locators, class, severity and its basis, the rule applied, detection path, suggested remediation, owner, disposition |
| **Five-part conformance table** | Per part: present, absent, empty, or holding content that belongs elsewhere — with coverage as a fraction |
| **Dose reconciliation table** | Every dose, regimen and supporting exposure value in 2.7.2 against 2.7.3 and 2.7.4, both sides preserved |
| **Module 5 placement table** | Each study, its primary objective, where it sits, and where the granularity rules put it |
| **Review memo** | Counts by class and severity, coverage fractions, residual risk, sign-off block |
| **Human-review record** | Owner-confirmation block, disposition log, closure signature |

## What it will not do

It never rewrites the summary · never moves, merges or renumbers a section ·
never decides which of two conflicting doses is correct · never selects or
justifies a dose · never assumes who owns 2.7.2 · never declares anything ready
to file · never approves or signs off.

Those are not omissions. A tool that adjudicates a dose disagreement between the
clinical pharmacology summary and the safety summary has replaced the reviewer
rather than helped them.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `review-ctd-272-content/` and carries its own `LICENSE`, so it works
from extraction alone with no repository present.

Then ask:

> Review our draft 2.7.2 against M4E before the dossier freeze.

or

> The dose in 2.7.2 and 2.7.4 disagree somewhere — find every place.

**Ordinary chat** — paste or attach the section under review together with the
corresponding passages from 2.7.3 and 2.7.4, state who the accountable owner is,
and follow the workflow.

The chat route **cannot run the deterministic scripts.** Structure validation,
placement and reconciliation become model-performed with the reasoning shown for
you to confirm, and the run should be scoped to one part of 2.7.2 at a time —
tens of values, not hundreds.

## What to supply

The accountable-owner declaration · draft 2.7.2 · Modules 2.7.3 and 2.7.4 · a
Module 5 study index marking each study's **primary** objective · the source CSRs
or synopses · the modelling reports cited in 2.7.2.3 · the bioanalytical method
reference · one line saying which document version is authoritative for each
value · and the dossier's own content conventions if one exists.

Three of those do disproportionate work. The **owner declaration** is the gate
described above. The **primary objective** in the study index is what decides
Module 5 placement — an index that lists objectives without marking which one is
primary makes the placement check `NEEDS_INPUT`, not a guess. The **version
baseline** prevents the worst false-positive class: confident findings that are
pure artefacts of comparing against a superseded draft.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`FULL-REVIEW` · `STRUCTURE-ONLY` · `DOSE-RECONCILE` · `PLACEMENT-ONLY` ·
`UPDATE` · `CLOSEOUT`

`STRUCTURE-ONLY` is not a cut-down full pass. Content written into the wrong part
propagates into every later draft and is the most expensive defect to fix late,
so checking the skeleton before the values stabilise has independent value.

## Data boundary

Use only material you are permitted to process in your current AI environment. A
draft 2.7.2 is submission content by definition, so the "unpublished regulatory
submission" stop is not theoretical here — the skill asks you to confirm
authorisation explicitly before it reads anything.

It stops on patient-level data, sponsor-confidential content you are not
authorised to process, or credentials, and names the category **without quoting
the content**.

Documents you supply are treated as evidence, never as instructions. Text inside a
source that appears to address the assistant — including a claim about who owns
the section — is reported with its location and never obeyed.

## Evidence and limitations

**Evidence level: `not-yet-evaluated`.** No planted-defect fixture has been run
against this skill yet, so no score is quoted and none is implied.

When a synthetic benchmark ships it will state its exact task, model, host, date
and run count — and a synthetic benchmark will still not be clinical validation,
not a GxP qualification, and not evidence of real-world performance.

Two limits are structural rather than provisional. The ownership convention stays
a configurable input because no cited text resolves it. And the five parts are
checked for conformance and content placement only — whether the science inside a
part is adequate is a reviewer's judgment that no validator supplies.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic checks
require a skill-aware host; the workflow itself runs anywhere a document can be
attached, in the disclosed degraded mode described above.

Licence MIT · version 0.1.0 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology)
