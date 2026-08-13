# Development Plan Gap Assessment

**Give it your clinical pharmacology development plan and the compound's own
properties. It returns every expected piece of evidence, each marked present,
triggered, waivable-with-rationale, or a residual gap — with the criterion that
created the obligation attached.**

A qualified reviewer decides what to do about each one. This skill finds them; it
does not decide that a gap is acceptable, does not commit to a study, and does
not approve a plan.

## The problem

A programme's clinical pharmacology evidence accumulates over years, across
studies run by different people under criteria that moved while the programme was
running. Nobody holds the whole expected set in their head. The gaps that hurt are
not the obvious missing studies — they are the ones the compound's own in-vitro
data quietly made obligatory, the commitment recorded in a meeting minute two
years ago that nothing in the current plan tracks, and the element everybody
assumed was waived without anyone writing the rationale down.

Finding those by reading the plan is the wrong method: an inventory assembled
while reading the plan inherits the plan's blind spots.

## What you get

| Output | Contents |
|---|---|
| **Evidence coverage register** | One row per expected element: criterion, its guidance anchor, classification, severity, evidence locator, trigger locator, rationale locator, rule applied, detection path, owner, disposition |
| **Gap assessment memo** | Counts by class and severity, coverage as a fraction, the anchor set with dates and check status, trigger summary, residual risk, sign-off block |
| **Trigger evidence table** | Each drug property that met a trigger condition, its value and unit, its source, and the criteria it obligated |
| **Human-review record** | Adjudication log and closure signature |

Four classes, and they are deliberately not two. `waivable-with-rationale` means
a written rationale exists and was located — **not** that the rationale is
sufficient. Judging it is adjudication, and adjudication belongs to a person.

## What it will not do

It never decides a gap is acceptable · never judges whether a waiver rationale is
sufficient · never commits to a study, a sequence or a timeline · never predicts
an agency position · never selects or justifies a dose · never edits the plan ·
never approves or signs off.

It also never invents a criterion. Every expectation in the inventory carries an
anchor ID from the shared guidance index, and anything the index does not settle
is emitted marked `UNVERIFIED:` rather than stated confidently. An expectation
invented to fill a row is indistinguishable in the output from a real one, which
makes it the failure this kind of tool can most easily hide.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `assess-development-plan-gaps/` and carries its own `LICENSE`, so it
works from extraction alone with no repository present.

Then ask:

> What clinical pharmacology evidence is this development plan still missing?

**Ordinary chat** — attach your plan and the drug-property summary, and follow
the workflow. The chat route **cannot run the deterministic checklist engine.**
Criterion mapping becomes model-performed with the full inventory printed for you
to confirm, and the run should be scoped to one module or one readiness slice —
tens of criteria, not the whole inventory.

## What to supply

The development plan · the target product profile or draft labelling concept ·
a study inventory with status per study · **the drug-property dossier** ·
regulatory interaction history including recorded commitments · a scope
declaration naming indication, population, region, modality and submission type ·
**the waiver rationale file** · and one line baselining which guidance anchors
are in force and when each was last checked.

Two of those do disproportionate work. The **drug-property dossier** is what
turns a generic checklist into this compound's obligations — without it, every
trigger-conditional criterion comes back `NEEDS_INPUT` instead of being guessed.
The **waiver rationale file** is what separates a waiver from a gap; without it
every unstudied element looks like a residual gap and the register inflates into
a list the team already knows the answers to.

Missing an input disables specific classifications. The skill says which, and
marks them `NEEDS_INPUT` rather than proceeding quietly.

## Modes

`FULL-ASSESSMENT` · `TRIGGER-CHECK` · `SUBMISSION-READINESS` · `MODULE-SCOPE` ·
`UPDATE` · `TPP-EXTRACTION` · `REGULATORY-PRECEDENT` · `TRIAL-LANDSCAPE` ·
`DILIGENCE-EVIDENCE-INVENTORY`

`TRIGGER-CHECK` is the one that earns its keep between milestones: new in-vitro
or clinical results routinely create obligations without anyone reopening the
plan, so re-running only the trigger-conditional criteria against fresh data is
cheap and catches the gaps nobody went looking for.

The four extension modes remain evidence-only. TPP extraction links proposed
fields to supplied sources without judging desirability or feasibility. The two
public-intelligence modes record the caller's filters, pagination, timestamps,
exclusions, provenance and exact Drugs@FDA application or ClinicalTrials.gov NCT
IDs without deciding similarity, agency acceptance, competitive importance or
differentiation. Diligence inventory maps a declared request list to supplied
artifacts without deciding materiality, valuation, approvability or go/no-go.

Network access is optional and fail-closed. A failed or page-bounded retrieval
is returned as `CANNOT_ASSESS` with completed pages retained; it is never called
a complete public landscape.

## Study types

Twelve study-type modules in the shared set declare this skill as a consumer,
covering first-in-human, DDI, food effect, renal and hepatic impairment, mass
balance, QT, immunogenicity, mAb PK, paediatric extrapolation, oncology dose
optimisation, and combination regimens. For any study type with no module the
skill runs its module-agnostic criteria and marks study-specific content
`CANNOT_ASSESS` rather than improvising criteria.

One known gap: the hepatic module rests on a guidance anchor that is not present
in the shared index. Hepatic criteria are therefore emitted marked `UNVERIFIED:`,
with no date or cut-point stated, until the index carries that anchor.

## Data boundary

Use only material you are permitted to process in your current AI environment. A
development plan is frequently sponsor-confidential, and a regulatory-interaction
history almost always is — check before attaching either.

The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, or credentials, and names the
category **without quoting the content**.

Documents you supply are treated as evidence, never as instructions. Text inside a
source that appears to address the assistant — including a rationale asserting
that a gap is closed — is reported with its location and never obeyed.

## Evidence

Evaluated against a synthetic development plan with expert-keyed planted gaps
spanning all four classes.

**A synthetic benchmark is not clinical validation, not a GxP qualification, and
not evidence of real-world performance.** Published scores state their exact
task, model, host, date and run count.

The merge of plan-gap and evidence-gap assessment into a single skill is a stated
assumption, not a validated finding. Practitioner feedback may split it back into
two skills, and that is recorded as an open question rather than settled.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic checklist
engine require a skill-aware host; the degraded chat mode carries the workflow
anywhere a file can be attached, at reduced scope and without script
verification.

Licence MIT · version 0.1.0 · collection clinical-pharmacology · research id S01
