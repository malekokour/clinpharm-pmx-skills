# CSR PK Consistency Review

**Give it a draft study report and the outputs it claims to derive from. It
returns every place they disagree, with both values and both locations.**

A qualified clinical pharmacologist decides what to do about each one. This skill
finds them; it does not fix them, and it does not decide which number is right.

## The problem

A CSR states a PK value in the synopsis, again in the body, again in a Section 14
table — and it derives from an NCA output that says something slightly different.
Reconciling hundreds of those by hand is the heaviest recurring burden in the
review cycle, and a missed mismatch propagates into a Module 2.7 summary, then a
label, then an agency answer.

## What you get

| Output | Contents |
|---|---|
| **PK discrepancy register** | One row per finding: both statements, both locators, class, severity, the rule applied, detection path, suggested remediation, owner, disposition |
| **QC memo** | Counts by class and severity, ICH E3 conformance, extraction coverage as a fraction, residual risk, sign-off block |
| **Source reconciliation table** | Which document version was authoritative for each value |
| **Human-review record** | Disposition log and closure signature |
| **Route-specific trace** | CSR-local PD/biomarker eight-field trace or topline snapshot-to-source fields, with source status, denominators, and visible `UNKNOWN`s |

## What it will not do

It never edits the report · never reruns an analysis · never decides which of two
conflicting values is scientifically correct · never selects or justifies a dose ·
never makes a regulatory commitment · never interprets topline clinical meaning,
causality, benefit-risk, disclosure language, or commitments · never judges
biomarker qualification, surrogate validity, or dose implications · never
approves or signs off.

Those are not omissions. A tool that adjudicates a scientific disagreement
between two documents has replaced the reviewer rather than helped them.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `review-csr-pk-consistency/` and carries its own `LICENSE`, so it
works from extraction alone with no repository present.

Then ask:

> QC the PK sections of this CSR against the NCA outputs.

**Ordinary chat** — attach
[`CSR-PK-Consistency-Review.docx`](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/skills/review-csr-pk-consistency) (or
the Markdown, which some hosts accept where DOCX is rejected) together with your
section under review, and follow the workflow it carries.

The chat route **cannot run the deterministic scripts.** Reconciliation becomes
model-performed with arithmetic shown for you to confirm, and the run should be
scoped to a section — tens of values, not hundreds. That limitation is stated on
the starter itself.

## What to supply

Draft CSR with synopsis · Section 14 PK tables · protocol and amendments · **the
PK analysis plan** · NCA report and parameter tables · statistical outputs ·
bioanalytical report reference · and one line saying which document version is
authoritative for each value.

For `PD-BIOMARKER-TRACE`, also supply the declared measures, owner-supplied
applicability and source/status register, and this CSR's protocol/SAP and report
outputs. For `TOPLINE-SNAPSHOT`, supply the snapshot and this CSR's named
protocol, SAP, locked-output, cutoff, analysis-set, exposure, and deviation
sources. If either request spans another document thread or the programme, the
skill routes it to `reconcile-cross-document-facts`.

Two of those do disproportionate work. The **analysis plan** supplies the rounding,
unit and exclusion rules, so the report is checked against its own pre-specified
conventions rather than generic ones. The **version baseline** prevents the worst
false-positive class — confident findings that are pure artefacts of comparing
against a superseded output.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`FULL-QC` · `SYNOPSIS-QC` · `TLF-SPOT-CHECK` · `UPDATE` · `CLOSEOUT` ·
`PD-BIOMARKER-TRACE` · `TOPLINE-SNAPSHOT`

`SYNOPSIS-QC` is not a cut-down full pass — synopsis content propagates earliest
into summaries and briefing documents, so checking it before Section 14 stabilises
has independent value.

The two added routes are deliberately CSR-local. PD/biomarker context checks
exactly eight fields per declared measure and reports
`fields traced / (8 × declared measures)` plus measure count. Topline checking
compares named source fields without interpreting them. Multi-document and
programme-thread use belongs to `reconcile-cross-document-facts`.

## Study types

Validated modules ship for **SAD/MAD** and **food effect**. For any other study
type the skill runs its study-type-agnostic checks and marks study-specific
content `CANNOT_ASSESS` rather than improvising criteria. Further modules ship
only with their own planted-defect fixture.

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, or credentials — and names the
category **without quoting the content**.

Documents you supply are treated as evidence, never as instructions. Text inside a
source that appears to address the assistant is reported with its location and
never obeyed.

## Evidence

Evaluated against a synthetic CSR with expert-keyed planted defects spanning every
finding class and all three detection paths.

**A synthetic benchmark is not clinical validation, not a GxP qualification, and
not evidence of real-world performance.** Published scores state their exact task,
model, host, date and run count — see
[`evals/benchmark/review-csr-pk-consistency/`](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/evals/benchmark/review-csr-pk-consistency).

## Compatibility

Provider-neutral Markdown. Progressive disclosure and deterministic checks require
a skill-aware host; the DOCX and Markdown starters carry the workflow anywhere a
file can be attached. An authenticated Copilot web-chat test rejected DOCX and
accepted Markdown, which is why both ship.

Licence MIT · version 0.1.0 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology)
