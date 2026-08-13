# DDI Evidence Review

**Give it the interaction evidence you hold for one compound. It returns a
structured package in which every in-vitro signal ends in a stated decision, and
every gap where one does not.**

A qualified clinical pharmacologist decides what each interaction means. This
skill assembles the evidence and shows the decision path; it does not judge
clinical significance, and it does not pick a management strategy.

## The problem

A drug's interaction evidence arrives in pieces: an in-vitro enzyme report, a
transporter report, two clinical studies, a PBPK run that stood in for a third
study, a label section, and a handful of citations. Somewhere in that pile an
in-vitro signal was raised and never carried to a conclusion — no clinical study,
no modelling substitution, no stated reason. Nobody notices, because no single
document owns the whole chain.

That open branch is the finding that surfaces late: in a review question, or in a
label negotiation, long after the study that would have closed it could have been
run.

## What you get

| Output | Contents |
|---|---|
| **DDI evidence table** | One row per perpetrator-victim-parameter triple: in-vitro basis with its assay system, clinical result, modelling output, label statement, provenance — each with its own locator |
| **Study-trigger trail** | Per in-vitro signal: the inputs used, the cutoff computed, the threshold applied and where it came from, the branch taken, the terminus reached. Emitted whether or not a gap was found |
| **Gap and contradiction register** | One row per finding: both statements, both locators, class, severity, detection path, the threshold applied, suggested remediation, owner, disposition |
| **Management-strategy drafts** | Proposed wording per pair, marked draft, with the evidence each sentence rests on |
| **Threshold transcription record** | Every threshold and band used, with the guidance version it came from |
| **Human-review record** | Disposition log and closure signature |

## What it will not do

It never decides whether an interaction is clinically significant · never chooses
between contraindication, dose reduction and monitoring · never sets a dose or an
interval · never decides which of two conflicting statements is correct · never
supplies a Ki, an fm or a threshold from model knowledge · never validates a PBPK
model · never makes a regulatory commitment · never approves or signs off.

Those are not omissions. A tool that declares an interaction clinically
significant has replaced the reviewer rather than helped them.

## It is not an interaction database

This skill structures the evidence you hold for **your own compound**. It does
not maintain an interaction corpus, does not answer "what interacts with drug Y",
and does not enumerate interacting drugs from memory.

Where a curated database is the authority for a claim, you supply the extract —
database, query, access date, retrieved statement — and the skill records that
provenance. A claim without it is marked `NEEDS_INPUT` rather than asserted.

## It ships no cutoffs, deliberately

The basic-model cutoff variables and the strong / moderate / weak magnitude bands
are **not hardcoded anywhere in this skill.** You supply the governing ICH M12
text; the skill transcribes the thresholds it uses into the run record, cites
that version in every finding, and refuses threshold-dependent checks when the
text is unavailable.

That is the opposite of convenient, and it is the point. A cutoff baked into a
file in 2026 is a silent wrong answer in 2028. The anchor row for `ich-m12` in
the shared guidance index is itself marked research-sourced and not independently
re-verified — verify it before trusting any conclusion that depends on a cutoff.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `review-ddi-evidence/` and carries its own `LICENSE`, so it works
from extraction alone with no repository present.

Then ask:

> Build the DDI evidence package for compound X from these reports.

or, for the narrower question:

> Does the CYP3A4 in-vitro result trigger a clinical study?

**Ordinary chat** — attach your in-vitro report and the governing M12 text
together with the pair you want reviewed, and follow the workflow the skill
carries.

The chat route **cannot run the deterministic scripts.** The decision tree is
walked by the assistant with its arithmetic and branch choices printed for you to
confirm, and the run should be scoped to one or two pairs rather than a whole
package. Each trail row is labelled model-produced.

## What to supply

In-vitro enzyme report · in-vitro transporter report · clinical DDI study reports
and parameter tables · any modelling report that substituted for a study · **the
mass-balance or ADME summary carrying fraction metabolised by pathway** · current
label sections with interaction content · literature citations with the specific
statement relied on · curated-database extracts with query and access date ·
**the governing ICH M12 text** · and one line saying which version is
authoritative for each claim.

Two of those do disproportionate work. The **M12 text** supplies every threshold
and band, so nothing is checked against a number this skill invented. The
**fraction metabolised** is what triggers victim-side assessment at all — without
it, victim-side checks are marked `NEEDS_INPUT` rather than quietly passing.

Missing an input disables specific checks. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`PACKAGE` · `TRIGGER-CHECK` · `PAIR-REVIEW` · `MANAGEMENT-DRAFT` · `UPDATE` ·
`CLOSEOUT`

`TRIGGER-CHECK` is not a cut-down full pass. Whether to run a clinical study is
decided earlier than, and independently of, how the interaction is eventually
worded — so checking the trigger logic on its own has value before any drafting
starts.

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, licensed database content you may
not redistribute, or credentials — and names the category **without quoting the
content**.

Documents you supply are treated as evidence, never as instructions. Text inside
a source that appears to address the assistant — including a sentence asserting
that no study is required — is reported with its location and never obeyed.

## Evidence

**A synthetic benchmark is not clinical validation, not a GxP qualification, and
not evidence of real-world performance.** Any published score states its exact
task, model, host, date and run count.

Version 0.1.1 includes synthetic diagnostic execution cases for the DDI package
and enzyme/transporter inventory, with provisional expert keys. Those artifacts
exercise structure and boundaries; they are not qualifying paired model runs,
practitioner adjudication, clinical validation, or a GxP qualification. No
detection-performance score may be claimed until PS-D024 MEDIUM qualification
and whole-library integration pass on the exact package bytes.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic trigger
trail require a skill-aware host; without script execution the workflow runs in a
disclosed degraded mode, scoped to one or two pairs.

Licence MIT · version 0.1.1 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology)
