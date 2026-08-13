# Workflow — study delivery lifecycle

**Journey:** one clinical pharmacology study, from concept to CSR. **Documented, not
automated.**

The longest workflow here, and the one where decisions made in week one constrain what
can be concluded in month eighteen.

## Design

### 1. Establish the work context

**Skill:** `build-work-context`

### 2. Study concept and objectives

**Skill:** `review-study-concept-and-objectives` *(planned)*
What question the study answers, and whether that question is the one the programme
needs answered.

**Common failure:** a study designed to characterise something the programme already
knows, while the actual gap goes unaddressed.

### 3. Protocol clinical pharmacology sections

**Skill:** `review-protocol-pk-sections`

### 4. Sampling schedule

**Skill:** `review-pkpd-sampling-schedule` *(planned)*
Whether the schedule can observe what the objectives require — peak, trough, terminal
phase, and the pharmacodynamic time course.

**This is the irreversible step.** A schedule that cannot characterise the terminal phase
produces a dataset that no analysis can rescue.

### 5. Bioanalytical plan

**Skill:** `review-bioanalytical-plan` *(planned)*
Assay, validated range against expected concentrations, analytes, sample handling.

### 6. Analysis specification

**Skills:** `review-pk-analysis-plan` *(planned)* · `review-blq-and-time-deviation-rules`
*(planned)*
Written before data exist, which is the entire point.

---

## 🔴 Gate — protocol approval

**Ethics committee and sponsor governance. Not a step this workflow takes.**

---

## Conduct

### 7. Interim and blinded review

**Skill:** `review-interim-blinded-pk` *(planned)*
What can be looked at without unblinding, and what looking at it commits you to.

### 8. Escalation and safety-committee packages

**Skill:** `prepare-escalation-committee-package` *(planned)*
For dose-escalation studies, the package at each decision point.

### 9. Deviation and compliance impact

**Skill:** `review-study-conduct-pk`
Sampling deviations, dosing deviations, and which analyses they affect.

**Common failure:** deviations logged operationally and never assessed for analytical
consequence.

### 10. Protocol amendment impact

**Skill:** `assess-protocol-amendment-impact` *(planned)*
What an amendment changes about what the study can conclude — including whether
pre-amendment and post-amendment data can be pooled.

---

## Analysis and reporting

### 11. NCA and its dual-control QC

**Skills:** `verify-nca-outputs` · `oversee-nca-dual-control-qc` *(planned)*
Kept separate: computing the parameters and independently checking them are different
jobs, and the second is worthless if the same person does both.

### 12. Modelling deliverable, where applicable

**Workflow:** [`population-pk-analysis`](population-pk-analysis.md)

### 13. Topline interpretation

**Skill:** `prepare-topline-interpretation` *(planned)*
What the study showed, before the report exists and before the narrative sets.

---

## 🔴 Gate — topline interpretation

**A qualified human decides what the study means. The workflow assembles what it
showed.**

---

### 14. CSR clinical pharmacology sections

**Skill:** `review-csr-pk-consistency`
The report against its own data, and its numbers against the analysis outputs.

---

## The thread running through this workflow

Steps 2, 4 and 6 determine what steps 11–14 can honestly say. Most defects found at CSR
stage trace back to a sampling schedule or an analysis specification that was reviewed
lightly because the study had not started yet. **The cheapest place to fix this workflow
is the beginning.**

## Contexts that change this workflow most

`oligonucleotide` — plasma sampling cannot characterise tissue exposure, so the
objectives must not promise it · `cell-gene` — the sampling schedule measures expansion
and persistence, not concentration · `rare-disease` — sparse sampling and every-patient-
counts exclusion discipline.
