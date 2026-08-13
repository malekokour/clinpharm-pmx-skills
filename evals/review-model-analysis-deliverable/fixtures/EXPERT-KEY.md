severity_status: adjudicated
# Expert key — synthetic population PK deliverable fixture, fenzaridine

> **Answer key. Do not supply this to the model under evaluation.**
>
> 11 planted defects across question-to-conclusion tracing, assumption tracing,
> numeric reconciliation, deviation checking, traceability and reporting hygiene.
> Every one is discoverable from the four supplied documents alone; none requires
> a rubric element, criterion or threshold that the documents do not supply.

## Fixture documents

| File | Role |
|---|---|
| `synthetic-poppk-analysis-plan.md` | I1 + I5 — the analysis plan, rule source, pre-stated criteria, context of use |
| `synthetic-poppk-report.md` | I2 — the deliverable under review |
| `synthetic-report-appendices.md` | I4 + I6 — parameter tables, bootstrap, simulations, dataset specification, diagnostic figure list |
| `synthetic-deviation-log-and-baseline.md` | I3 + I7 + I8 + I9 — commissioning question, deviation log, version baseline, declared type, owner |

## Rubric note

The declared analysis type is **popPK**, for which the shared review-rubric
library carries **no rubric**. The correct behaviour is to run the general
`ich-m15` rubric plus the type-agnostic checks and mark popPK-specific content
`CANNOT_ASSESS`. Every defect below is findable under `ich-m15` and the plan's
own pre-stated criteria — none of them requires the missing popPK rubric, so a
run that invents one has done so gratuitously.

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | scope-breach | **Critical** | conclusion against the stated context of use | Report §5 conclusion 4 vs plan §2 | The report concludes **No dose adjustment is required for subjects with moderate hepatic impairment**. The plan states the context of use is **mild renal impairment and body weight only**, no hepatic covariate was screened, and the diagnostic figure list states no figure addresses hepatic function |
| D2 | numeric-mismatch | **Critical** | value reconciliation, body against its own appendix | Report §4.1 vs Table C-1 | The body reports **CL/F 12.4 L/h**; the final parameter table reports **14.2 L/h**. 13% apart, far outside the plan's stated 1% reconciliation tolerance, and the bootstrap median of 14.1 L/h sits with the table |
| D3 | untraced-conclusion | **Critical** | conclusion traced to a presented analysis | Report §5 conclusion 3 vs Table C-3 | The report concludes that exposure at **200 mg once daily** is comparable to 150 mg once daily in subjects over 100 kg and that the regimen is supported for Phase 3. Table C-3 states the simulated regimens were **100 mg and 150 mg once daily** and that no other regimen was simulated |
| D4 | post-hoc-criterion | Major | criterion in the report traced back to the plan | Report §3 vs plan §6 | The report calls **≥90% of observations fall within the 90% prediction interval** a pre-specified acceptance criterion. The plan's pre-stated criteria are **goodness-of-fit plots and a bootstrap of 500 replicates**, and it states that no further criterion is pre-stated. A criterion that appears only in the report |
| D5 | undocumented-deviation | Major | plan rule against the report and the deviation log | Report §2 vs plan §4 and deviation log | The report states **All subjects with evaluable pharmacokinetic data were included**; the plan pre-specifies that subjects with a **baseline eGFR below 30 mL/min are excluded**. The dataset specification shows 6 such subjects retained, and the deviation log records no departure covering it |
| D6 | unbounded-assumption | Major | assumption traced into the limitations | Report §3 vs §6 | The methods state that **the assumption of time-invariant clearance was not tested**. The limitations section does not mention it, so a conclusion drawn under the assumption is not bounded by it anywhere in the report |
| D7 | unanswered-question | Major | commissioning question traced to a conclusion | Commissioning question vs report §5 | The commissioning question asks whether renal function explains the observed variability in trough concentrations. §4.2 presents the eGFR covariate result, but no conclusion in §5 answers the question as asked |
| D8 | numeric-mismatch | Major | value reconciliation, body against its own appendix | Report §3 vs Table C-2 | The report states the bootstrap used **1000 replicates**; the appendix states **Bootstrap (n = 500)**, which is also the number the plan pre-stated. Recorded once, as one discrepancy with two locators |
| D9 | presentation | Minor | reference resolution | Report §4.2 vs Appendix C index | The covariate relationships are said to be in **Table C-4**; the Appendix C index lists Table C-1 to Table C-3 and states no other table exists. The reference resolves to nothing |
| D10 | stale-version | Minor | citation resolution against the baseline | Report header vs baseline Part B | The report names its plan as **PMX-FZD-PLAN v1.0**; the baseline declares **PMX-FZD-PLAN v2.0** authoritative |
| D11 | unit-inconsistency | Minor | unit consistency against the plan's convention | Table C-1 vs plan §7 | The apparent volume of distribution is given as **214 L/h** in the parameter table, while the plan states volume terms are **reported in L** and the report body gives the same estimate as 214 L |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **3 / 5 / 3** |
| Value-comparison path (`either`) | 6 (D2, D3, D5, D8, D10, D11) |
| Traceability and reading path (`model`) | 5 (D1, D4, D6, D7, D9) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → maximum weighted score
**3(5) + 5(3) + 3(1) = 15 + 15 + 3 = 33**

## Severities are PROVISIONAL

**Defect *presence* is certain. Defect *severity* is not.**

All eleven items were planted deliberately. That a gap, mismatch or untraceable
claim exists at each location is a fact about this fixture, and a run that fails
to report one has missed something real.

The **severity** column has **not been adjudicated by a practitioner.** It is the
fixture author's prospective application of this skill's own severity table, and
it carries no more authority than that.

The Critical denominator is what a promotion gate turns on: the release rule is
that no Critical may be missed, so which three of these eleven are Critical
decides whether a run passes or fails. Moving one row between Critical and Major
changes the verdict on an output that has not changed at all.

Consequences, all binding:

- **This package may not be promoted to `released` on the strength of this key.**
  `severity_status: provisional` on line 1 is machine-read by
  `scripts/validate_repo.py`, which fails the build if a `released` package
  carries a provisional key.
- Runs graded against this key are **diagnostic evidence, not release evidence**.
- Adjudicating severities after outputs have been inspected turns every already
  graded run into diagnostic evidence and requires a fresh held-out rerun.
- **The adjudicator must include someone qualified in the modelling discipline.**
  This skill's own text says a traceability gap and a defensible modelling choice
  can look identical from the document alone, and severity is exactly where that
  ambiguity lands.

Rows the author is least confident about, flagged for the adjudicator:

- **D5** is graded Major as an undocumented deviation. A reviewer who weighs the
  retention of 6 subjects the plan excluded as changing the estimated covariate
  effect — and therefore the reported result — would grade it Critical.
- **D8** is graded Major because the bootstrap replicate count does not change a
  headline estimate. A reviewer who treats any misstatement of what was actually
  run as conclusion-affecting would grade it Critical.
- **D11** is graded Minor as a presentation defect on the reasoning that the body
  reports the same estimate correctly as 214 L. The reference CSR fixture in this
  repository grades its own unit swap Critical, so a reviewer applying that
  precedent would move this row a long way.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **The absence of popPK-specific rubric elements.** The shared library carries
   no popPK rubric. The correct output is `CANNOT_ASSESS` for popPK-specific
   content, not a set of findings against an invented checklist.
2. **The SAEM estimation method replacing FOCE-I.** This is a genuine departure
   from plan §5, and it is recorded as DEV-01 in the deviation log with a
   justification. A documented deviation is not an undocumented one, and flagging
   it as `undocumented-deviation` picks the wrong departure — the undocumented
   one is D5.
3. **Between-subject variability of 42% CV on V/F against 28% CV on CL/F.**
   Different parameters with different variability. Not a mismatch.
4. **Shrinkage of 24% on the absorption rate constant.** It is reported with its
   value in both the body and Table C-1. Whether that shrinkage is acceptable is
   a modelling judgment this skill does not make, and no pre-stated criterion in
   the plan addresses it.
5. **The plan's exclusion of subjects with baseline eGFR below 30 mL/min.** A
   legitimate pre-stated rule, explicitly not revisited after results are seen.
   A run flagging the *plan* rather than the report's departure from it has
   picked the wrong side of D5.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both statements
with both locators**, name the rubric element or pre-stated criterion the item
failed, label each finding mechanical or model-detected, and mark the disposition
`open`. A run that re-fits or critiques the model, that decides whether the
two-compartment choice or the SAEM substitution was right, that decides which of
two conflicting clearance values is correct, or that selects a Phase 3 regimen
has violated the human-review contract regardless of whether its guess was right.

The provisional collection assignment of this package must be stated as
provisional wherever the collection is named.

## The test to apply when adjudicating these severities

Added 2026-08-06. The severities below are `provisional` — nobody has ruled on
them. When someone does, this is the standard to apply, taken from published
guidance rather than invented here.

**EMA GCP inspection findings** are classified on a consequence axis, and the
discriminator is *does affect* / *might affect* / *would not be expected to
affect*:

| Tier | Test |
|---|---|
| **Critical** | **Adversely affects** the quality and integrity of data. Totally unacceptable; possible consequence is rejection of data |
| **Major** | **Might adversely affect** it. A severe deficiency |
| **Minor** | **Would not be expected to adversely affect** it. Indicates a need for improvement |

Worked precedent from the adjudicated CSR fixture (B20, B24):

- A **1000× unit error on a tabulated primary parameter** already consumed
  downstream — *does* affect integrity. **Critical.**
- An **unsupported description of an analysis whose numbers are correct** —
  *might* mislead without changing an outcome. **Major.**
- A **figure axis in the wrong unit, every tabulated value intact** — *would not be
  expected* to affect integrity. **Minor.**

Two rules that fall out of it, both established the hard way:

1. **Detectability is never a mitigation.** "A careful reader would catch it"
   defeats the purpose of a checking tool, and is unreliable besides.
2. **A unit mismatch on a tabulated value is a wrong value, not a formatting
   defect** — there the unit is part of the value.

Note the limit of the analogy: ICH E3 classifies protocol *deviations* as major or
minor only and offers no three-tier scheme for reporting errors. The tiers here are
borrowed from the inspection standard and applied to document defects by analogy.
That is deliberate, and stated so a reviewer can reject it.

## Wave 3-B new-assertion addendum — provisional

This addendum covers only cases 11 and 12; it does not revise the original
eleven-defect key or any original severity.

### Case 11 — reproducibility-package structure

The defect manifest plants exactly four deterministic finding classes plus one
unresolved seed state: `artifact-absent`, `artifact-hash-mismatch`,
`lineage-reference-unresolved`, `unsupported-completeness-claim`, and
`CANNOT_ASSESS`. The clean manifest over the same six-artifact package is the
negative control. The checker must report its exact denominators and must not
claim scientific reproducibility, fitness for purpose, validation, correctness,
or regulated-system certification.

### Case 12 — PBPK reporting trace

Two identity mismatches are mechanically bound: model `SYN-PBPK-MODEL-007 v2.0`
versus `SYN-PBPK-MODEL-007 v2.1`, and run
`SYN-PBPK-RUN-2026-08-11-B` versus `SYN-PBPK-RUN-2026-08-11-A`. The judged
assertions cover absent tissue-partition provenance, unresolved observed-data
identity, absent pre-stated AUC/Cmax criteria, and a conclusion beyond the stated
context. Species/model/parameter/predictive/extrapolation adequacy and dose
selection remain human-only.

These are diagnostic assertions only. Practitioner adjudication and fresh
qualifying runs remain required.

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
