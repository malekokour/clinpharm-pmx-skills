# Cross-Document Fact Reconciliation

**Give it the documents a programme has produced — protocol, CSRs, Module 2.7.2,
briefing packages, label — and it returns a register of every clinical
pharmacology fact in them: where each one came from, everywhere it is restated,
and every place two documents disagree.**

A qualified clinical pharmacologist decides what to do about each one. This skill
finds them; it does not fix them, and it does not decide which value is right.

## The problem

A clearance value is estimated in a study, written into a CSR, summarised in
Module 2.7.2, quoted in a briefing package, and finally proposed in a label. Then
the NCA is rerun, or an amendment lands, or a second study reports — and the
number moves in one document while four others still carry the old one.

Nobody set out to let that happen. It happens because the thread is long, the
documents are owned by different people, and the check is manual every single
time. The failure is silent until an agency finds it, and by then the wrong
number has been in a submitted document for months.

Checking one report against its own sources will not catch this. By construction,
each document can be perfectly consistent with its own sources and still
contradict the one downstream of it.

## What you get

| Output | Contents |
|---|---|
| **Programme fact register** | One row per fact: origin document and version, every restatement with its locator, both sides of any conflict, class, severity, the rule applied, owner, disposition |
| **Reconciliation memo** | Counts by class and severity, thread coverage as a fraction of the document inventory, residual risk, sign-off block |
| **Updated source-version record** | Which version is proposed as authoritative for each fact class — proposed, never applied |
| **Propagation map** | Origin to every downstream restatement, so a changed source value shows you exactly what it touches |
| **Human-review record** | Disposition log and closure signature |
| **Route-specific trace** | Privacy structure, ethics trace, topline snapshot-to-source fields, or programme-thread PD/biomarker eight-field trace — always with source status, denominators, and visible `UNKNOWN`s |

## What it will not do

It never edits a document · never reruns an analysis · never decides which of two
conflicting values is correct · never decides which version should be
authoritative · never judges whether a discrepancy is clinically meaningful ·
never selects or justifies a dose · never makes a regulatory commitment · never
approves or signs off. It also never ingests participant records, decides privacy
or legal compliance, claims ethics approval or response adequacy, or interprets
topline causality, benefit-risk, disclosure wording, or commitments.
It never judges PD/biomarker plausibility, qualification sufficiency, clinical
meaningfulness, surrogate validity, assay fitness, endpoint selection, regulatory
acceptance, threshold-driven action, or dose implications.

Those are not omissions. A tool that adjudicates a disagreement between a CSR and
a label has replaced the programme's clinical pharmacology lead rather than
helped them.

## The neighbour it is not

`review-csr-pk-consistency` checks **one report against its own sources**. This
skill maintains **the thread across studies and across time**.

If a single document plus its own outputs settles your question, use that one.
If the question is "does this still match what we said elsewhere, and when did
it stop matching", use this one. Both call the same reconciliation engine — the
shared cross-document consistency tool, in `document` mode and `programme` mode
respectively. Neither carries its own copy.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `reconcile-cross-document-facts/` and carries its own `LICENSE`, so
it works from extraction alone with no repository present.

Then ask:

> Reconcile the dose rationale across the protocol, the CSR, 2.7.2 and the
> proposed label.

or

> We reran the NCA on Study 102. What downstream documents restate those values?

**Ordinary chat** — no starter document ships for this skill yet. Paste the
document inventory and the facts you want traced, and work in `THREAD-TRACE` mode
on a handful of named facts.

The chat route **cannot run the deterministic engine.** Reconciliation becomes
model-performed with arithmetic shown for you to confirm, and a full `BASELINE`
pass over a whole programme is out of reach. Scope accordingly, and expect the
skill to say so rather than proceeding quietly.

## What to supply

A document inventory with versions and dates · the source-version baseline · the
prior register if there is one · CSRs for every contributing study · protocols
and amendments · Module 2.7.2 · briefing documents and health-authority responses
**already submitted** · the proposed or current label · and the analysis plans
that state the rounding, unit and exclusion conventions.

For `PRIVACY-STRUCTURE`, also supply an owner-confirmed applicability declaration
and a `SYNTHETIC_SCHEMA` JSON inventory only — never participant records. For
`ETHICS-SUBMISSION-TRACE`, supply the submission manifest, version graph,
questions, responses, decisions/conditions, and dates. For `TOPLINE-SNAPSHOT`,
supply the snapshot plus its named protocol, SAP, locked-output, analysis-set,
cutoff, exposure, and deviation sources.
For `PD-BIOMARKER-TRACE`, supply the declared measures, owner-supplied
applicability inputs, and the programme document/source/version/status register.

Three of those do disproportionate work. The **document inventory** is the
denominator — without it, "no discrepancies found" is unfalsifiable, because
nothing distinguishes a clean thread from an unread one. The **source-version
baseline** prevents the worst false-positive class: confident findings that are
pure artefacts of comparing against a superseded document. The **already-submitted
documents** are the ones people forget to supply and the ones that matter most —
a statement already sent to an agency is a fixed point, and a later document
quietly disagreeing with it is precisely what this skill exists to catch.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`BASELINE` · `PROPAGATE` · `THREAD-TRACE` · `IMPACT` · `CLOSEOUT` ·
`PRIVACY-STRUCTURE` · `ETHICS-SUBMISSION-TRACE` · `TOPLINE-SNAPSHOT` ·
`PD-BIOMARKER-TRACE`

`BASELINE` is not a heavier version of the others — it is what establishes the
origin of every fact the other four modes depend on. `IMPACT` answers a question
about documents, never about consequences: it tells you what restates a changed
value, not whether the change matters.

`PD-BIOMARKER-TRACE` uses the same programme reconciliation engine and checks
exactly eight fields per declared measure, reporting
`fields traced / (8 × declared measures)` plus measure count. It preserves each
source's version/status and visible `UNKNOWN`s; it does not interpret them.

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, or credentials — and names the
category **without quoting the content**.

This workflow pulls in briefing packages and submitted responses by its nature,
so the check runs per document rather than once per session.

Documents you supply are treated as evidence, never as instructions. Text inside
a source that appears to address the assistant is reported with its location and
never obeyed. That includes a prior fact register: dispositions inside it are a
human's record, not a permission.

## Evidence

**This skill has not been qualified.** A synthetic diagnostic suite now covers
its original workflow and the extension routes, but no MEDIUM behavioral
qualification or benchmark run exists. Its
reconciliation engine was measured only in `document` mode by
`review-csr-pk-consistency`, against a synthetic fixture with expert-keyed
planted defects — that is evidence about the engine, not about this workflow.

When a benchmark does exist it will be synthetic. **A synthetic benchmark is not
clinical validation, not a GxP qualification, and not evidence of real-world
performance.** Any published score states its exact task, model, host, date and
run count.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic
programme-mode engine require a skill-aware host with script execution; without
it the workflow runs in a disclosed degraded mode and says so in its output.

Licence MIT · version 0.2.0 · collection clinical-pharmacology
