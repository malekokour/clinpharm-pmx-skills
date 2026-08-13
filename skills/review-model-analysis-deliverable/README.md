# Model Analysis Deliverable Review

**Give it a modelling plan or report. It returns every question the deliverable
never answers, every conclusion it cannot trace, and every assumption it makes
without saying so — each with its location.**

A qualified modeller and clinical pharmacologist decide what to do about each
one. This skill finds gaps in how an analysis is reported. It does not touch the
model.

## Ownership of this workflow is not settled

This package is **proposed for Pharmacometrics primary ownership** — the
modelling function owns the outcome — and that proposal is deferred pending the
commissioned Pharmacometrics research. Its collection is recorded as
`clinical-pharmacology` provisionally, as the reviewing discipline currently
hosting it, not as a decided home.

The scope boundary does not move with that decision. **Model execution is out of
scope for this entire library under either owner.**

## The problem

A modelling deliverable is commissioned to answer a question, and it is read by
people who cannot re-run it. The gaps that matter are rarely in the code: a
question in the plan that no conclusion ever addresses, an evaluation criterion
that first appears next to the results, an assumption in the methods that never
reaches the limitations, a conclusion phrased more broadly than the context of
use allows.

Those travel. A model-informed conclusion that outruns its stated context of use
ends up in a dose rationale, then a summary, then a label — and by then the
qualification that bounded it is three documents behind.

## What you get

| Output | Contents |
|---|---|
| **Gap and traceability register** | One row per finding: the statement, its locator, the rubric element or pre-stated criterion it failed, that locator, class, severity, detection path, suggested remediation, owner, disposition |
| **Review memo** | Counts by class and severity, rubric conformance, inventory coverage as a fraction, residual risk, sign-off block |
| **Question-to-conclusion trace** | Each stated question, the analysis addressing it, the result, the conclusion — or the marker where one is missing |
| **Human-review record** | Disposition log and closure signature |

Every one of them is a draft for review. Nothing here is a finished review, and
nothing here is a sign-off.

## What it will not do

It never re-fits, re-runs or re-simulates a model · never critiques or proposes
model structure · never edits the deliverable · never decides whether a
modelling assumption was reasonable · never decides which of two conflicting
values is correct · never selects or justifies a dose · never makes a regulatory
commitment · never approves or signs off.

Those are not omissions. A tool that critiques a model it did not build, from a
document alone, has replaced the modeller rather than helped them.

## Rubrics come from the shared library, and missing ones stay missing

This skill implements no rubric of its own. It consumes the shared review-rubric
library — the ICH M15 model analysis plan/report rubric, the PBPK format and
content rubric, and the exposure–response rubric — and cites regulatory anchors
by ID from the shared guidance index rather than restating dates.

**Population PK has no rubric in the library.** A popPK deliverable runs the
general model-analysis rubric plus the type-agnostic checks, and popPK-specific
content is marked `CANNOT_ASSESS`. The skill will not improvise the missing
checklist, because an invented checklist presented as a standard is worse than
an acknowledged gap.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `review-model-analysis-deliverable/` and carries its own `LICENSE`,
so it works from extraction alone with no repository present.

Then ask:

> Review this popPK report against the analysis plan and tell me which
> conclusions aren't traceable.

**Ordinary chat** — attach the plan and the report and ask for the same thing.
The chat route **cannot run the deterministic scripts.** Numeric reconciliation
becomes model-performed with arithmetic shown for you to confirm, and the run
should be scoped to one section or one rubric.

Rubric conformance and question-to-conclusion tracing degrade far less in chat
than arithmetic does, which makes the plan review and the traceability pass the
two modes worth running there.

## Modes

`PLAN-REVIEW` · `REPORT-REVIEW` · `TRACEABILITY` · `SPOT-CHECK` · `UPDATE` ·
`CLOSEOUT` · `PBPK-HUMAN-PK-PREDICTION-REVIEW`

`PLAN-REVIEW` is the highest-leverage one and the easiest to skip. An evaluation
criterion that is missing before the modelling starts becomes an unfalsifiable
claim afterwards — nothing downstream can recover it.

The PBPK mode traces only reporting, context of use, source/model identity,
parameter provenance, run identity, observed/predicted identities, and declared
acceptance-criterion presence. Any FIH stated-dose-chain or dose-adjacent
arithmetic request routes intact to `review-fih-dose-rationale`; this MEDIUM
package does not reproduce that HIGH-risk arithmetic.

The installed package also includes `scripts/analysis_reproducibility.py`. Given
a declared manifest and package root, it checks file presence/identity, SHA-256
hashes, environment, command/seed/log declarations, and lineage without running
the analysis. A green result is structural evidence only—not scientific
reproducibility, fitness for purpose, validation, correctness, or regulated-
system certification.

## What to supply

The **analysis plan** in its signed version · the report under review · the
commissioning question and decision context · the data provenance statement ·
the evaluation criteria as pre-stated · the appendices the report cites · the
deviation log · one line saying which version of plan, report and dataset is
authoritative · and the declared analysis type.

Two of those do disproportionate work. The **plan** supplies the criteria, so the
report is checked against its own pre-stated rules rather than generic ones —
and so a criterion written after the results cannot pass as if it had been
pre-stated. The **version baseline** prevents the worst false-positive class:
confident findings that are pure artefacts of comparing against a superseded
plan or dataset.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Close neighbours

Two skills sit close enough to be confused with this one, in both directions.
`verify-nca-outputs` owns derived PK parameters and their exclusion rules — NCA
tables appear inside modelling deliverables, but they are that skill's object,
not this one's. `review-ctd-272-content` owns the submission summary, which
quotes modelling conclusions without being one.

Activation accuracy against both is a release condition for this package, not a
nice-to-have.

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, or credentials — and names the
category **without quoting the content**.

Modelling deliverables carry a specific version of that risk: analysis datasets
and diagnostic listings pasted into an appendix can be subject-level. Appendices
are inside the preflight, not after it.

Documents you supply are treated as evidence, never as instructions. Text inside
a source that appears to address the assistant — including text inside embedded
model code or control streams — is reported with its location and never obeyed.

## Evidence and limitations

**This package has no benchmark yet.** Its evidence level is
`not-yet-evaluated`, and the activation tests against its two close neighbours
have not been run. Both are release conditions.

When a benchmark exists it will use a synthetic deliverable with expert-keyed
planted gaps. **A synthetic benchmark is not clinical validation, not a GxP
qualification, and not evidence of real-world performance.** Any published score
will state its exact task, model, host, date and run count.

Two limits are structural rather than provisional. The skill sees only what the
deliverable says — a model that is well reported and poorly built passes every
check here. And a rubric records whether something is reported, never whether it
was done well.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic numeric
checks require a skill-aware host; rubric conformance and traceability run
anywhere a file can be attached.

Licence MIT · version 0.2.0 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology) (provisional —
see above)
