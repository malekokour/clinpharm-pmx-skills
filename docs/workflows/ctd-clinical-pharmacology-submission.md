# Workflow — CTD clinical pharmacology submission

**Journey:** the 2.7.x clinical pharmacology set, assembled so the documents agree with
each other and with their sources. **Documented, not automated.**

The defining risk here is not any single document. It is that six documents each quote
the same numbers and one of them is stale.

## Steps

### 1. Establish the work context

**Skill:** `build-work-context`

### 2. Biopharmaceutics summary

**Skill:** `review-ctd-271-biopharmaceutics` *(planned)*
Formulation bridging, food effect, biowaiver justification, dissolution.

### 3. Clinical pharmacology summary

**Skill:** `review-ctd-272-content`
The core document. Absorption through elimination, special populations, interactions,
exposure–response.

**Carries forward:** every parameter value this document states. They will reappear
elsewhere.

### 4. Exposure–safety summary

**Skill:** `review-ctd-2734-exposure-safety` *(planned)*
2.7.3.4 and 2.7.4 — the exposure–safety relationships and how they were derived.

### 5. Study synopses

**Skill:** `review-ctd-276-synopses` *(planned)*
Each synopsis against its own study report.

**Common failure:** a synopsis rounds a value the report states precisely, and the
rounded figure is the one every later document quotes.

### 6. Clinical overview

**Skill:** `review-ctd-25-clinical-overview` *(planned)*
The clinical pharmacology contribution to 2.5, and whether it is consistent with 2.7.2
rather than a second telling of it.

### 7. Module 5 placement

**Skill:** `place-module-5-content` *(planned, wraps `ctd_placement.py`)*
Which report belongs where, and whether anything referenced in a summary is actually
filed.

### 8. Submission datasets and define.xml

**Skill:** `review-submission-datasets-and-define` *(planned)*
Analysis datasets, their definitions, and whether the values in the summaries can be
regenerated from them.

### 9. Cross-document reconciliation

**Skill:** `reconcile-cross-document-facts`
**This is the step the workflow exists for.** Every parameter, every population
estimate, every exposure ratio, checked across all documents against its source of
record.

**Common failure:** the model report is updated after 2.7.2 is drafted, and only the
documents someone remembered get updated.

---

## 🔴 Gate — submission-readiness

**A qualified human declares the set ready. The workflow reports discrepancies; it does
not clear them.**

A reconciliation that finds nothing is only meaningful with its denominator: *how many
facts were checked, across how many documents.* A clean result over three checked values
is not a clean submission.

---

## Where the assessment phase continues

`author-applicants-position` and `map-agency-question-evidence` pick up after filing.
`reconcile-cross-document-facts` runs again after any response that changes a number —
the consistency problem does not end at submission, it gets harder.

## Contexts that change this workflow most

`adc` — multiple analytes mean 2.7.2 must state which analyte every parameter belongs
to · `rare-disease` — model-based evidence substitutes for studies that do not exist,
and the substitution must be explicit in the summary · `oncology` — exposure–response
built on a single dose level needs its confounding stated, not implied.
