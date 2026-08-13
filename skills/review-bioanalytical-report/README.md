# Bioanalytical Report Review

**Give it a bioanalytical validation report and the sample analysis report that
goes with it. It returns which ICH M10 elements are there, which are not, and
the handful of gaps that actually change how you can read the PK data.**

A qualified reviewer decides what each one means. This skill records what the
report says; it does not re-validate the assay and it never declares a method
acceptable.

## The problem

Most clinical pharmacologists rely on an assay they did not run, documented in a
report they did not write, appended to a study report they are accountable for.
The questions that matter are narrow and repetitive: is incurred sample
reanalysis in there, does the demonstrated long-term stability actually cover how
long the samples sat, was dilution integrity established for the samples that
went above the upper limit, does the BLQ convention match what the PK analysis
plan assumed.

Each is answerable from documents already in hand. None is answerable quickly,
because the answer is spread across two reports, a protocol section and an
analysis plan.

## What you get

| Output | Contents |
|---|---|
| **ICH M10 conformance register** | One row per rubric element: present, absent or `CANNOT_ASSESS`, adequacy as reported, locator, class, severity, suggested remediation, owner, disposition |
| **PK-relevance observations** | The subset that changes how the concentrations may be read — storage window, above-ULOQ handling, carryover, BLQ definition, reanalysis rules, ISR — each with both statements and both locators |
| **Review memo** | Counts by class and severity, coverage as a fraction, which checks were disabled by missing inputs, residual risk, sign-off block |
| **Human-review record** | Disposition log and closure signature |

Every one is a draft for review. Every disposition is written as `open`.

## It consumes a shared rubric — that is the design

The ICH M10 conformance rubric lives in exactly one place in this library:
`shared/assets/review-rubric-library.md`. This skill loads it and applies it. It
carries no private copy of the checks, no local extension, and no second list of
elements.

**This is why the package is thin, and it is a deliberate decision rather than an
unfinished one.** The reviewable surface of a bioanalytical report reduces almost
entirely to that shared conformance rubric. A private copy would fork on the
first guidance revision and leave two parts of the same library disagreeing about
the same standard — the exact failure the shared-asset rule exists to prevent.

The visible consequence: if the report contains something the rubric does not
cover, the skill records it as an observation and asks for an amendment to the
shared asset. It does not quietly grow its own checklist.

The second consequence: **this package ships no script.** There is no
deterministic engine here beyond the rubric. The little arithmetic involved —
recomputing a run pass count or an ISR agreement percentage that the report
already tabulates — is model-performed, shown in full, and labelled unverified.
Scope a run to tens of values rather than hundreds.

## What it will not do

It never re-validates the method · never re-fits a calibration curve · never
recomputes accuracy or precision from raw run data · never declares an assay
acceptable, adequate or fit for purpose · never supplies an acceptance criterion
from general knowledge · never certifies GLP or GCP compliance · never verifies
NCA derivations · never edits the report · never approves or signs off.

Those are not omissions. A tool that pronounces on assay adequacy has replaced
the bioanalytical scientist rather than helped the clinical pharmacologist who
depends on them.

## Not this skill

| If you are asking | Use instead |
|---|---|
| "Verify the NCA derivations and parameter values" | `verify-nca-outputs` — derived parameters, not assay validation |
| "QC the PK sections of this CSR against its tables" | `review-csr-pk-consistency` |
| "Review the CP sections of this protocol" | `review-protocol-pk-sections` |
| "Is this method fit for purpose?" | A qualified bioanalytical scientist |

The nearest neighbour is `verify-nca-outputs`, and the boundary is the object,
not the subject matter: that skill checks the parameters derived from the
concentrations, this one checks the report describing the method that produced
them. A request that spans both is two runs, not one.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `review-bioanalytical-report/` and carries its own `LICENSE` and its
vendored copy of the shared rubric, so it works from extraction alone with no
repository present.

Then ask:

> Check this validation report against ICH M10 and tell me what is missing.

**Ordinary chat** — attach the validation report, the sample analysis report and
the shared rubric file (`shared/assets/review-rubric-library.md`), then ask the
same question. Because this skill has no deterministic engine, the chat route
loses less than it does for skills that ship one: the arithmetic is
model-performed either way, and the workflow is the same. Keep the run scoped to
one report and one mode.

## What to supply

Bioanalytical method validation report · study sample analysis report · **one
line naming the governing standard** (ICH M10, the FDA guidance, or both) ·
analyte and matrix definition · **the protocol section covering PK sample
collection, handling and storage** · the PK analysis plan section covering BLQ
handling · which report version is authoritative · and the name of the
accountable owner.

Two of those do disproportionate work. The **declared standard** selects which
rubric is applied, so the report is checked against what the sponsor actually
committed to rather than a default. The **protocol sample-handling section**
enables the single most consequential observation — whether samples were stored
outside the conditions the report demonstrates stability for — which cannot be
made from the bioanalytical report alone.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`FULL-RUBRIC` · `PK-RELEVANCE` · `SPOT-CHECK` · `UPDATE` · `CLOSEOUT`

`PK-RELEVANCE` is not a cut-down full pass. It answers a different question — not
"does this report conform" but "does anything here change how I read the
concentrations" — and it is the mode most clinical pharmacologists want.

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, run data carrying subject identifiers,
sponsor-confidential content you are not authorised to process, unpublished
submissions, or credentials — and names the category **without quoting the
content**.

Documents you supply are treated as evidence, never as instructions. Text inside
a source that appears to address the assistant is reported with its location and
never obeyed. A statement inside the report that an element was reviewed and
found acceptable is content, not evidence that it conforms.

## Evidence

**No planted-defect fixture ships for this skill yet, so no score is published
for it.** Treat its outputs as unevaluated until one exists. The shared rubric it
consumes is versioned and reviewed; the workflow around that rubric is not
independently benchmarked.

When a fixture does ship, the caveat that governs every skill in this collection
will apply: **a synthetic benchmark is not clinical validation, not a GxP
qualification, and not evidence of real-world performance.** Published scores
state their exact task, model, host, date and run count.

The guidance anchors this skill cites — `ich-m10` and `fda-bioanalytical` — are
recorded in `shared/assets/guidance-index.md`. Both currently carry a
`research-sourced` verification status there, meaning their dates are inherited
from the research package and have not been independently re-checked against the
issuing body's own page. That is stated on the skill itself too.

## Compatibility

Provider-neutral Markdown. Nothing here requires script execution, so the skill
behaves the same in a skill-aware host and in ordinary chat, provided the shared
rubric is available to it. Progressive disclosure only changes how the rubric
gets loaded, not what the workflow does.

Licence MIT · version 0.1.0 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology)
