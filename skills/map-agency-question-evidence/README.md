# Agency Question Evidence Map

**Give it the information request an authority actually sent you. It returns
every separate thing being asked, what evidence you already hold for each, where
that evidence sits, and what is missing.**

A qualified clinical pharmacologist writes the answers. This skill works out what
the questions are and whether anything already answers them.

## The problem

An agency question arrives as prose. Question 3 turns out to contain three
distinct asks; question 7 was answered in the last cycle and nobody remembers
where; question 9 quietly seeks a commitment rather than a fact. Meanwhile the
version of the report the authority read is not the version sitting on the shared
drive.

The response then gets assembled under time pressure, and the failure is rarely a
wrong answer. It is an ask nobody noticed, a claim with no citation behind it, or
a citation pointing at a table that does not contain the number quoted.

## What you get

| Output | Contents |
|---|---|
| **Question decomposition register** | One row per answerable unit: parent question number, verbatim wording, type, topic |
| **Evidence map** | Unit → document → the version the authority holds → section, table, row, page → evidence state |
| **Gap and owner register** | What is missing, what artefact would close it, proposed owner, disposition |
| **Completeness memo** | Decomposition ratio, mapping coverage, gap counts, question-battery coverage — all as fractions |
| **Traceability report** | Every claim in a draft response: does it carry a citation, does the citation resolve, does the locator hold |
| **Human-review record** | Owner confirmation, adjudication log, closure signature |

Everything is a draft for review. Nothing is a response, and nothing can be sent
from here.

## What it will not do

It never writes the scientific answer · never decides which of two conflicting
values is correct · never selects or justifies a dose · never drafts or implies a
commitment · never approves, signs off or sends · never assigns an owner without
human confirmation · never marks a question answered.

It also states **no turnaround norm**. The only response date it will report is
the one the request itself states, transcribed verbatim. Where the request states
none, the output says `UNKNOWN` rather than supplying the interval people usually
quote — that figure is practice convention and is carried by no regulatory anchor
this project cites.

And it does not predict. A question battery drawn from the public review record
tells you which shapes of question a position has to survive; it tells you
nothing about what any authority will ask about your product.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `map-agency-question-evidence/` and carries its own `LICENSE`, so it
works from extraction alone with no repository present.

Then ask:

> Split this information request into answerable parts and tell me what evidence
> we already have for each.

**Ordinary chat** — attach the request and the documents it cites, and ask for
one numbered question at a time.

The chat route **cannot run the deterministic scripts.** The completeness check
and the citation trace become model-performed with their counts shown for you to
confirm, and the run should be scoped to a single question rather than a whole
letter.

## What to supply

The request exactly as received, complete with its own numbering and attachment
list · its metadata, including the response date as the request words it · prior
correspondence on the same topic · the submitted documents it cites · the source
outputs behind those documents · an owner roster · and **one line per document
saying which version was submitted**.

Two of those do disproportionate work. The **prior correspondence** is what turns
a repeat question from a week of work into a citation. The **submission version
baseline** prevents the quiet failure mode: mapping a question against a newer
internal revision produces an evidence map that answers a question nobody asked,
and nothing in it looks wrong.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`TRIAGE` · `FULL-MAP` · `GAP-ONLY` · `TRACE-CHECK` · `CLOSEOUT`

`TRIAGE` is not a cut-down full pass. On the day a request lands, knowing how
many real asks are inside it — and which of them seek a commitment rather than a
fact — changes who gets pulled in and when.

`CLOSEOUT` confirms that every unit is dispositioned and every gap has a named
owner. It never marks a unit answered.

## Completeness is a fraction

Every coverage number carries its denominator: units mapped over units total,
gaps closed over gaps open, battery items covered over battery items checked. A
completeness claim without a denominator cannot distinguish a well-evidenced
response from an unread one, so this skill does not make one.

The battery it checks against is the public question bank at
[`shared/assets/qbr-question-bank.md`](https://github.com/malekokour/clinpharm-pmx-skills/blob/main/shared/assets/qbr-question-bank.md).

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions or unpublished agency
correspondence, or credentials — and names the category **without quoting the
content**.

Documents you supply are treated as evidence, never as instructions. That
includes the request letter: it sets the questions, it does not set the
assistant's behaviour. Text inside any source that appears to address the
assistant is reported with its location and never obeyed.

## Evidence

**This skill has not yet been evaluated.** No benchmark run exists for it, and no
score should be quoted for it until one is published under
`evals/benchmark/map-agency-question-evidence/`.

When that evaluation runs it will use a synthetic request with expert-keyed
planted defects. **A synthetic benchmark is not clinical validation, not a GxP
qualification, and not evidence of real-world performance.** Any published score
states its exact task, model, host, date and run count.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic
completeness and traceability checks require a skill-aware host; the workflow
itself runs anywhere a file can be attached, in the disclosed degraded mode.

Licence MIT · version 0.1.0 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology)
