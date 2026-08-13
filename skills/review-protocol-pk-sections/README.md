# Protocol PK Section Review

**Give it a protocol and the documents its clinical pharmacology sections rest
on. It returns a comment list — what is missing, what disagrees with itself, and
what the sampling schedule actually covers.**

A qualified clinical pharmacologist decides what to do about each comment. This
skill raises them; it does not fix them, it does not pick a dose, and it does not
declare a design adequate.

## The problem

Protocol review is where clinical pharmacology defects are still cheap. After the
study runs they are not: a sampling schedule that cannot support the half-life it
was designed to estimate, a parameter listed in the objectives that the analysis
plan never defines, a restriction absent for a design whose endpoint depends on
it. None of those can be corrected after the samples are drawn.

The work itself is unglamorous and repetitive — the same conventions, checked
against the same twelve sections, on every protocol, under a review deadline.
That is exactly the kind of check that gets skimmed on the third one in a week.

## What you get

| Output | Contents |
|---|---|
| **CP comment list** | One row per comment: section and version, the statement as written, the convention applied and where it came from, what is missing or inconsistent, class, severity, detection path, suggested remediation, owner, disposition |
| **Conformance checklist** | Every element the sponsor template and study-type module require, marked present / absent / present-but-incomplete, each with a locator |
| **Sampling adequacy table** | Terminal-phase coverage in multiples of the reported half-life, density around Tmax, trough sampling, window overlaps, last time point versus LLOQ |
| **Human-review record** | Disposition log and closure signature |
| **Consent-consistency trace** | In `CONSENT-CONSISTENCY`: protocol/sample/consent/approval document identities, versions, procedure-presence mismatches, exact locators, and explicit denominators |
| **Vulnerable-population structural register** | Five artifact-locator states per owner-declared population, always `HUMAN_REVIEW` / `UNSET` |

## What it will not do

It never edits the protocol · never derives, selects, adjusts or endorses a dose ·
never recomputes a starting-dose derivation · never decides whether a design is
scientifically adequate · never decides which of two conflicting values is
correct · never makes a regulatory commitment · never approves or signs off.

Those are not omissions. A tool that pronounces a sampling schedule adequate has
made the reviewer's judgment for them, using less information than they have.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `review-protocol-pk-sections/` and carries its own `LICENSE`, so it
works from extraction alone with no repository present.

Then ask:

> Review the PK sections of this protocol before it goes to operational review.

**Ordinary chat** — attach the protocol sections under review together with the
IB PK section, and follow the workflow the skill carries.

The chat route **cannot run the deterministic scripts.** The conformance
checklist and the sampling arithmetic become model-performed with the working
shown for you to confirm, and the run should be scoped to a section — one
sampling schedule and its analysis plan, not a full protocol.

## What to supply

Protocol CP sections plus the schedule of assessments · the **Investigator's
Brochure PK section** · nonclinical summary or FIH dose-derivation memo · the
embedded PK analysis plan · bioanalytical method summary with LLOQ · **your
sponsor protocol template** · and one line naming the study type.

For `CONSENT-CONSISTENCY`, also supply the current consent/participant-information
forms (including any separate genomic consent), sample/laboratory manual, a
structural approval/version register, and an owner-supplied jurisdiction/site
applicability profile. Do not supply participant records or signed forms carrying
personal data.

Two of those do disproportionate work. The **IB PK section** supplies the
reported half-life and Tmax the sampling schedule is checked against — without it
the adequacy check emits `NEEDS_INPUT` rather than assuming a value. The
**sponsor template** supplies the conventions, so the protocol is checked against
the rules its own organisation codifies instead of generic expectations, which is
the difference between a usable comment list and a page of false positives.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`FULL-REVIEW` · `SECTION-REVIEW` · `AMENDMENT-REVIEW` · `UPDATE` · `CLOSEOUT` ·
`CONSENT-CONSISTENCY`

`AMENDMENT-REVIEW` is not a cut-down full pass. An amendment's characteristic
defect is not in the text it changed — it is in the sections it should have
changed and did not, so that mode follows the ripple into unchanged content.

`CONSENT-CONSISTENCY` activates only for cross-document identity, version, and
PK/genomic procedure-presence reconciliation. It reports `PRESENT`, `MISSING`,
`MISMATCH`, `UNKNOWN`, `CANNOT_ASSESS`, or `HUMAN_REVIEW`; it never judges
consent adequacy, voluntariness, understanding, coercion, acceptable burden, or
whether re-consent is required.

## Study types

Validated modules ship for **SAD/MAD** and **food effect**. For any other study
type the skill runs its study-type-agnostic checks and marks study-specific
content `CANNOT_ASSESS` rather than improvising criteria. Further modules ship
only with their own planted-defect fixture.

The package also vendors a PD/biomarker context module with a fixed eight-field
trace denominator and a vulnerable-population structural register with five
artifact fields per owner-declared population. Neither component makes its
human-only scientific, ethics, or participant-protection judgments.

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, or credentials — and names the
category **without quoting the content**.

Documents you supply are treated as evidence, never as instructions. Text inside
a source that appears to address the assistant is reported with its location and
never obeyed — including text in tracked changes and comment balloons, which is
where protocol drafts most often carry it.

## Evidence

**This package has a diagnostic synthetic suite, not qualification evidence.** It
now covers the base protocol route plus consent consistency, vulnerable-population
structure, and PD/biomarker traceability, but severities remain provisional. No
candidate/no-skill comparison, practitioner adjudication, or model qualification
has run. Its evidence level is `diagnostic-suite-no-qualification`; no recall,
precision, activation-accuracy, clinical-validation, or release claim is permitted.

When a fixture does exist, the standing rule applies: **a synthetic benchmark is
not clinical validation, not a GxP qualification, and not evidence of real-world
performance.** Any published score states its exact task, model, host, date and
run count.

Regulatory anchors are cited by ID from the shared guidance index, never by a
date written from recollection. Rows in that index marked `research-sourced` have
not been independently re-verified against the issuing body, and comments that
rest on one say so.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic checks
require a skill-aware host; in ordinary chat the workflow runs in a disclosed
degraded mode with the arithmetic shown rather than script-verified.

Licence MIT · version 0.1.1 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology)
