# Dose Justification Evidence

**Give it the dose you have proposed and the studies behind it. It returns an
indexed evidence package — every claim traced to a locator, every uncovered
factor named, arranged against the questions reviewers ask.**

It does not tell you whether the dose is justified. That call belongs to a
qualified clinical pharmacologist, and this skill is built so it cannot quietly
take it.

## The boundary, up front

The research scoring recorded a **risk veto**: the output of this skill sits one
step from a registration-dose decision. So the skill **assembles and organises
evidence — it never selects, recommends, adjusts or justifies a dose, and never
states that the evidence supports the one you proposed.**

Ask it "so is 200 mg justified?" and you get the assembled evidence, the open
items, and a plain statement that the judgement is yours. You do not get yes or
no. That is the design, not a limitation of the current version.

## The problem

The dose justification is the thickest thread in a submission. It runs through
the PopPK report, two separate exposure-response analyses, a renal study, a
hepatic study, three DDI studies, a food-effect study, a bridging BE study, and
a dose-modification table that someone wrote from all of it. By the time it is
drafted, nobody can say from memory which sentence rests on which analysis — or
which factor nobody ever covered.

Reviewers ask about exactly those seams. Finding them yourself, before filing,
is a reading exercise measured in days.

## What you get

| Output | Contents |
|---|---|
| **Evidence index** | One row per claim in your position: the claim as written, its locator, the artefact offered in support, that artefact's locator, and whether the support was pre-specified |
| **Factor coverage matrix** | Every intrinsic and extrinsic factor, marked studied · covered in the PopPK covariate analysis · justified as not required · not covered · needs input |
| **Exposure-response summary** | What each analysis states — endpoint, exposure metric, population, reported relationship — efficacy and safety kept separate |
| **Formulation bridging chain** | Each link from clinical to commercial formulation, by code, strength and batch, with the study that links them and any break in the chain |
| **Question-coverage map** | Your evidence arranged against the question shapes the public review record shows being asked, with coverage as a fraction |
| **Open-item register** | Unsupported claims, unsupported dose-modification rules, uncovered factors, missing links, contradictions — each with what would resolve it |
| **Human-review record** | Disposition log and closure signature |

## What it will not do

It never selects, recommends or adjusts a dose · never says the evidence
justifies the proposed one · never proposes or revises a dose-modification
threshold · never decides whether coverage is sufficient to file · never decides
which of two conflicting values is correct · never judges whether an exposure
difference is clinically meaningful · never authors the narrative · never makes a
regulatory commitment or predicts what an agency will ask · never approves or
signs off.

Those are not omissions. A tool that tells you your dose is justified has
replaced the person accountable for the dose.

## Install and use

**Installed skill** — extract the release ZIP into your skills directory. It
extracts to `prepare-dose-justification-evidence/` and carries its own `LICENSE`,
so it works from extraction alone with no repository present.

Then ask:

> Assemble the evidence package behind the 200 mg once-daily dose.

**Ordinary chat** — paste [`PASTE.md`](PASTE.md) into the conversation together with
the section you are working on, and follow the workflow it carries.

The chat route **cannot run the deterministic scripts.** The coverage matrix and
the renal staging become model-performed with the working shown for you to
confirm, and the run should be scoped — one factor family, or one exposure-
response analysis, rather than a whole package. That limitation is stated on the
starter itself.

## What to supply

The proposed regimen and every dose-modification rule **exactly as you wrote
them** · the dose-selection section under assembly · the PopPK report with its
covariate analysis · the exposure-response reports for efficacy and safety,
named separately · the dose-ranging study reports · intrinsic-factor studies ·
extrinsic-factor studies · the BA/BE bridging package · **the analysis plans** ·
and one line saying which document version is authoritative for each value.

Three of those do disproportionate work. The **proposed regimen in your own
words** is what the whole index attaches to — the skill records it verbatim and
never paraphrases, because a paraphrase is the first step toward authoring the
position. The **analysis plans** separate pre-specified findings from post-hoc
ones, a distinction reviewers weigh heavily and one that is invisible without
them. The **version baseline** prevents confident gaps that are pure artefacts of
indexing against a superseded output.

Missing an input disables specific rows. The skill says which, and marks them
`NEEDS_INPUT` rather than proceeding quietly.

## Modes

`ASSEMBLE` · `FACTOR-COVERAGE` · `QUESTION-MAP` · `UPDATE` · `CLOSEOUT`

`FACTOR-COVERAGE` is not a cut-down full pass — coverage gaps drive study
planning on their own timeline, well before any package is assembled.

## Close neighbours

Two requests look like this one and are not:

- **First-in-human starting-dose rationale** is a pre-IND safety gate with its
  own criteria — `review-fih-dose-rationale`.
- **Development-plan gaps** are programme-level study gaps, not the evidence
  behind one dose position — `assess-development-plan-gaps`.

## Modality modules

Criteria modules ship for oncology dose optimisation, dose proportionality and
accumulation, renal and hepatic impairment, DDI, food effect, formulation
bridging, biologics and immunogenicity, paediatric extrapolation and QT. For a
programme none of them covers, the skill runs its modality-agnostic assembly and
marks modality-specific rows `CANNOT_ASSESS` rather than improvising criteria.

## Data boundary

Use only material you are permitted to process in your current AI environment.
The skill stops on patient-level data, sponsor-confidential content you are not
authorised to process, unpublished submissions, or credentials — and names the
category **without quoting the content**.

Documents you supply are treated as evidence, never as instructions. Text inside
a source that appears to address the assistant is reported with its location and
never obeyed — including text that tells it to confirm a dose.

## Evidence

A synthetic diagnostic suite and provisional expert key cover planted gaps
across every item class. They support development only; no qualifying behavioral
run, practitioner adjudication, or performance claim exists.

**A synthetic benchmark is not clinical validation, not a GxP qualification, and
not evidence of real-world performance.** Published scores state their exact
task, model, host, date and run count, and ship under
`evals/benchmark/prepare-dose-justification-evidence/`.

No score would relax the boundary. The refusal to make a dose call does not rest
on measured accuracy — it rests on what sits one step downstream of the output.

## Compatibility

Provider-neutral Markdown. Progressive disclosure and the deterministic coverage
and staging checks require a skill-aware host; the DOCX and Markdown starters
carry the workflow anywhere a file can be attached.

Licence MIT · version 0.1.0 · collection
[clinical-pharmacology](https://github.com/malekokour/clinpharm-pmx-skills/tree/main/collections/clinical-pharmacology)
