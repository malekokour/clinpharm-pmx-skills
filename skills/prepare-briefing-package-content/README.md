# Briefing Package Content

**Give it the positions you intend to take, the evidence you have, and the annex
list. It returns a drafted clinical pharmacology section, the questions worth
asking, and every place a position is not actually supported.**

A qualified clinical pharmacologist decides what goes in the package. This skill
prepares the content and finds the weak points; it never commits to anything and
never claims a position is agreed.

## The problem

A briefing package is where a programme's clinical pharmacology story is stated
in public for the first time. Positions get written from memory of the analyses,
cross-references get renumbered when an annex moves, and a sentence agreed in a
prior interaction quietly gets restated a different way.

None of that is caught by reading the package once more. It is caught by walking
each position back to a locator, and by asking the questions a reviewer would ask
before a reviewer asks them.

## What you get

| Output | Contents |
|---|---|
| **Draft CP briefing content** | Sections keyed to your own outline, every position with its evidence citations, marked DRAFT throughout |
| **Draft question set** | Each question with the sponsor decision it informs, the position it attaches to, and the evidence offered |
| **Question-bank alignment table** | Which review questions the package answers, which it leaves unanswered, coverage as a fraction |
| **Annex cross-reference map** | Position ↔ annex, plus unresolved references and orphan annexes |
| **Open-item and commitment-language register** | One row per finding; a separate list of every commitment-shaped sentence, with locators |
| **Human-review record** | Owner confirmation, disposition log, closure signature |

## What it will not do

It never submits or sends anything · never makes or implies a regulatory
commitment · never asserts a position is agreed or acceptable · never predicts
what an agency will ask or decide · never invents a citation, study or annex
identifier · never decides which of two conflicting positions is correct · never
selects or justifies a dose · never approves or signs off.

Those are not omissions. A tool that commits on the sponsor's behalf, or that
tells you a position will be accepted, has taken a decision that belongs to a
named person who answers for it.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `prepare-briefing-package-content/` and carries its own `LICENSE`, so
it works from extraction alone with no repository present.

Then ask:

> Draft the clinical pharmacology section of our briefing package and check every
> position against the evidence.

**Ordinary chat** — paste the workflow together with one section of your draft
and its annex list, and follow it.

The chat route **cannot run the deterministic checks.** Question-bank alignment
and cross-reference resolution become model-performed with the full mapping table
shown for you to confirm, and the run should be scoped to a single position set —
tens of cross-references, not hundreds.

## What to supply

The interaction scope as regulatory affairs stated it · your briefing package
outline · the positions you intend to take · the evidence inventory with versions
and dates · **the protocols and analysis plans** for every study cited · the
prior agency interaction record · the annex inventory with identifiers and
versions · and one line saying which document version is authoritative for each
value.

Two of those do disproportionate work. The **prior interaction record** is the
only way to catch a position that contradicts something the sponsor already
said — the most expensive defect in this workflow, and invisible without it. The
**annex inventory** is what makes a cross-reference resolvable at all; without it
every resolution check returns `NEEDS_INPUT`.

Missing an input disables specific checks. The skill says which, and marks them
rather than proceeding quietly.

## Modes

`DRAFT` · `QUESTION-SET` · `POSITION-REVIEW` · `ANNEX-MAP` · `UPDATE` · `CLOSEOUT`

`QUESTION-SET` is not a cut-down full pass. The questions determine what the
package has to support, so settling them before the positions harden is the
cheapest point to change direction.

## The commitment boundary

Commitment-shaped sentences — "the sponsor will", "will be submitted by" — are
extracted into their own list with locators and left unapproved. Proposed
commitment wording exists only as marked draft awaiting a named human.

The skill prepares content. A person decides it goes to an agency.

## Data boundary

Use only material you are permitted to process in your current AI environment.
This workflow is routinely pointed at sponsor-confidential material, so permitted
status is established explicitly at the start rather than inferred from the fact
that you asked. The skill stops on patient-level data, unpublished submissions or
correspondence outside your authorisation, or credentials — and names the
category **without quoting the content**.

Documents you supply are treated as evidence, never as instructions. That
includes prior minutes and advice letters: a sentence directed at the sponsor is
recorded as a fact and routed to the regulatory owner, never obeyed as authority
over the workflow and never treated as permission to close an item.

## Evidence

No benchmark run has been published for this skill yet. When one is, it will be a
synthetic fixture with expert-keyed planted defects, and any score will state its
exact task, model, host, date and run count.

**A synthetic benchmark is not clinical validation, not a GxP qualification, and
not evidence of real-world performance.**

Two limits are structural rather than pending work. The question bank describes
the public shape of clinical pharmacology review — it cannot tell you what an
agency will ask about your product. And the skill carries no agency meeting
procedure: format, timing and submission route come from you, or are marked
`NEEDS_INPUT`.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic checks
require a skill-aware host; the workflow itself reads and runs anywhere text can
be pasted, in the disclosed degraded mode.

Licence MIT · version 0.1.0 · collection clinical-pharmacology
