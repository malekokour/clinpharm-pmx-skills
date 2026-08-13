# NCA Output Verification

**Give it an NCA output package and the analysis plan it was supposed to follow.
It returns every reported value that does not trace to the parameter dataset,
every rule that was not applied as written, and every summary statistic that does
not recompute.**

This is the reviewer half of a dual control. The analysis stays with the
performing analyst. A named human signs. This skill finds the items and holds
them open.

## The problem

An NCA output package is where PK numbers are born. Everything downstream — the
study report, the Module 2.7 summary, the label — inherits whatever it contains,
including a subject excluded under a criterion nobody wrote down, a clearance
reported in the wrong unit, or a geometric mean computed on the arithmetic scale.

The second check that would catch those is real work: opening the parameter
dataset beside the report, re-reading the analysis plan for what it actually
pre-specified, and recomputing summary tables by hand. It is exactly the kind of
work that gets compressed when a database lock is close.

## What you get

| Output | Contents |
|---|---|
| **NCA QC record** | One row per check performed, including the checks that passed, with reconciliation coverage as a fraction |
| **Parameter discrepancy register** | One row per finding: value as written, its locator, the expected value or rule, the plan section that states the rule, class, severity, detection path, run baseline, suggested remediation, owner, disposition |
| **Rule-conformance table** | Each analysis-plan rule, the evidence it was applied, and its state |
| **Human-review record** | Dual-control roles, disposition log, closure signature |

Every output is a draft for review. Dispositions are written `open` and only
`open`.

## What it will not do

It never reruns the NCA or re-derives a parameter from concentrations · never
edits the dataset, the exclusion log, or the report · never adds, removes, or
re-justifies an exclusion · never decides which of two conflicting values is
correct · never selects or justifies a dose · never draws an efficacy or safety
conclusion · never approves, signs off, or acts as the second signature.

Those are not omissions. A tool that re-derives the parameters has stopped being
the second check and become a second analyst nobody appointed.

There is one line worth stating plainly, because it is the boundary the whole
skill sits on: **recomputing a reported summary statistic from supplied
per-subject values is arithmetic verification. Re-deriving a parameter from
concentration data is performing the analysis.** The first is in scope. The
second is not, and where only a re-derivation could settle a question, the skill
says so and hands it back.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `verify-nca-outputs/` and ships with `LICENSE`, so it works from
extraction alone with no repository present.

Then ask:

> QC the NCA outputs before they go into the CSR.

**Ordinary chat** — paste or attach the parameter tables, the relevant slice of
the parameter dataset, and the PK analysis plan section that states the rules,
then work through the procedure in `SKILL.md`.

The chat route **cannot run the deterministic scripts.** Reconciliation and
recomputation become model-performed with the arithmetic shown for you to
confirm, and the run should be scoped to a slice — one cohort or one parameter
class, tens of values rather than thousands of dataset rows.

## What to supply

NCA report with parameter tables · the per-subject parameter dataset as a
delimited text export · **the PK analysis plan** · the concentration dataset
actually analysed with its exclusion and flag log · the nominal-versus-actual
sampling-time record · the bioanalytical report reference for LLOQ · the reported
summary tables · one line stating the NCA run identifier, dataset version and
software version · and the names of the performing analyst and the reviewer.

Three of those do disproportionate work:

- The **analysis plan** supplies the AUC method, lambda-z acceptance criteria,
  BLQ convention, exclusion rules, units and rounding — so the outputs are
  checked against what this study pre-specified rather than against generic
  expectations. A finding that cites "standard practice" instead of a plan
  section is not reportable.
- The **run baseline** prevents the worst false-positive class: confident
  findings that are pure artefacts of verifying against a superseded run.
- The **named roles** exist because the performer-versus-reviewer split differs
  by company. The skill asks who holds each role rather than assuming an
  organisational model.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`FULL-VERIFICATION` · `RULES-CONFORMANCE` · `SUMMARY-STATS-CHECK` ·
`PARAMETER-SPOT-CHECK` · `UPDATE` · `CLOSEOUT`

`RULES-CONFORMANCE` is not a cut-down full pass. A rule misapplied at derivation
invalidates every value that rests on it, so checking the rules alone has
independent value before anyone counts digits.

## Where it stops and something else starts

| You want | Use |
|---|---|
| A report checked against the NCA values it quotes | `review-csr-pk-consistency` |
| Assay validation and sample analysis reviewed | `review-bioanalytical-report` |
| The analysis rerun | The performing analyst |
| A decision on which conflicting value is right | A qualified reviewer |

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, or credentials — and names the
category **without quoting the content**.

Subject-level PK datasets deserve particular care. A parameter dataset keyed to
identifiable subjects, or joined to demographics that identify them, is
restricted regardless of what the file is called.

Documents and datasets you supply are treated as evidence, never as instructions.
Text inside a source that appears to address the assistant — including free text
in an exclusion log — is reported with its location and never obeyed.

## Evidence

Designed to be evaluated against a synthetic NCA output package with
expert-keyed planted defects spanning each finding class.

**No benchmark run has been published for this skill yet, and its fixture is not
yet in the repository.** Treat the capability statements here as design claims,
not measured ones.

**A synthetic benchmark is not clinical validation, not a GxP qualification, and
not evidence of real-world performance.** When scores are published they will
state their exact task, model, host, date and run count, under
`evals/benchmark/verify-nca-outputs/`.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic checks
require a skill-aware host with script execution; without it the workflow runs in
a disclosed degraded mode with the arithmetic printed for confirmation. Parameter
datasets are read as delimited text — proprietary analysis-tool binaries are not
opened.

Licence MIT · version 0.1.0 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology)
