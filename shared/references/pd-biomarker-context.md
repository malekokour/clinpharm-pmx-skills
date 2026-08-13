---
module: pd-biomarker-context
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
sources: [ich-e16, fda-biomarker-qualification-evidentiary-framework-draft]
anchors: [ich-e16, fda-biomarker-qualification-evidentiary-framework-draft]
consumers: [review-protocol-pk-sections, review-csr-pk-consistency, reconcile-cross-document-facts]
---

# Study-type module — PD and biomarker context

Reference content only. This module adds a source-located context-and-traceability
surface to an existing review or reconciliation workflow. It is not a biomarker
qualification workflow and does not select a biomarker, endpoint, or dose.

## Design conventions to check

| Source | Status at 2026-08-11 | What it supports | Limit |
|---|---|---|---|
| ICH E16, *Biomarkers Related to Drug or Biotechnology Product Development — Context, Structure and Format of Qualification Submissions*, §§1.2–1.4 | Step 4, 2010-08-20 | Clear biomarker identity and proposed context-of-use trace in a qualification-submission structure | E16 does not establish evidentiary sufficiency or a universal biomarker strategy |
| FDA, *Biomarker Qualification: Evidentiary Framework* | Draft, nonbinding, 2018-12 | A source to track when the owner declares qualification use | Draft; not an implementation requirement and freshness-sensitive |

Before applying the module, obtain these owner-supplied applicability inputs:

1. biomarker or PD-measure identity and declared role;
2. intended context of use and development stage;
3. population and study/protocol scope;
4. jurisdiction/program and qualification-route status, if any;
5. authoritative source/version register with access or effective dates; and
6. named clinical pharmacology and biomarker/PD reviewers.

If any applicability input is absent, record it as `UNKNOWN`; do not infer a
qualification route, role, or intended use from the assay name.

## Expected statements in a report

Check exactly **8 fields per declared biomarker or PD measure**. Report coverage
as `fields traced / (8 × declared measures)` and also state the number of declared
measures. A finding count without both denominators is invalid.

| # | Field | Mechanical trace question |
|---:|---|---|
| 1 | Identity | Is one stable name/identifier used, with synonyms mapped? |
| 2 | Role | Is the declared role stated (for example PD measure, enrichment, monitoring, prognostic, predictive, or qualification candidate) without the reviewer inventing one? |
| 3 | Context of use | Is the purpose, population, decision setting, and interpretation boundary stated and source-located? |
| 4 | Specimen | Are matrix/tissue, collection context, handling, and storage source-located? |
| 5 | Method | Are platform/assay, method identifier/version, and laboratory named? |
| 6 | Timing | Are nominal collection and analysis time points traceable across protocol, schedule, SAP, and report? |
| 7 | Decision rule | Is any supplied threshold, change rule, or category reproduced verbatim with its source and status? |
| 8 | Validation reference | Is the analytical-validation or qualification reference identified with version/status, or explicitly absent? |

Supplementary traces may record population, PD endpoint, and claim-to-evidence
links, but they do not change the fixed 8-field denominator.

## Mechanical checks this module enables

- `PRESENT` — the supplied sources contain the field and a locator.
- `MISSING` — the declared source set was checked and the owner records no field.
- `MISMATCH` — two supplied sources state different identities, roles, versions,
  timing, rules, or references; preserve both statements and both locators.
- `UNKNOWN` — the source set, applicability, status, or field assessment is not
  complete enough to distinguish absence from an unprovided input.
- `CANNOT_ASSESS` — extraction failed or the selected route cannot inspect the
  artifact.
- `HUMAN_REVIEW` — mandatory disposition for every finding and every apparent gap.

Never convert `UNKNOWN` or `CANNOT_ASSESS` into a clean result. Never resolve a
terminology mismatch by choosing the biologically more plausible term.

### Consumer use

- `review-protocol-pk-sections`: trace the eight fields across objectives,
  endpoints, schedule of assessments, specimen handling, method, analysis plan,
  and supplied validation reference.
- `review-csr-pk-consistency`: reconcile the same declared context and field
  identities between protocol/SAP and report outputs.
- `reconcile-cross-document-facts`: preserve cross-document identity, role,
  context-of-use, method/version, timing, and decision-rule mismatches.

Each consumer retains its own workflow and output schema. This module supplies
criteria only and does not create a fourth editable source of record.

## Boundaries

The module must never judge **biological plausibility, qualification sufficiency,
clinical meaningfulness, surrogate validity, or dose implications**. It does not
decide whether any result is clinically significant, and it never selects,
adjusts, recommends, or justifies a dose. It also does not decide assay fitness,
endpoint selection, regulatory acceptance, or whether a threshold should drive a
clinical action. A named clinical pharmacologist and biomarker/PD reviewer make
those decisions.

Every output is prepare-only. The module never edits a protocol/report, closes a
finding, submits a qualification package, changes a study, or communicates an
external conclusion.
