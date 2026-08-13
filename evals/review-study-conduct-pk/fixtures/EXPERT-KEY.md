severity_status: adjudicated
# Expert key — synthetic cohort PK package fixture DNX-201

> **Answer key. Do not supply this to the model under evaluation.**
>
> 11 planted defects across the classes `review-study-conduct-pk` declares, and
> across both detection paths. Every one is discoverable from the four supplied
> documents alone. None requires outside knowledge, and none requires forming a
> view about the escalation decision.

## The documents

| File | Role in the workflow |
|---|---|
| `synthetic-cohort3-package.md` | I1 — the assembled cohort 3 committee package, the object under review |
| `synthetic-interim-listings.md` | I2 / I5 / I6 — interim listings, BLQ records, deviation log and bioanalytical run status |
| `synthetic-charter-and-analysis-rules.md` | I3 / I4 / I8 / I9 — required-content list, analysis conventions, blinding statement and data-cut baseline |
| `synthetic-cohort2-package-and-minutes.md` | I7 — the previously issued cohort 2 package and its committee minutes |

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | package-vs-listing mismatch | **Critical** | script | Slide 4 and Table A2 vs Listing 16.2.2 | Package reports mean Cmax **318 ng/mL**; the listing summary and the six individual values give **381 ng/mL**. A digit transposition, 16.5% apart, far beyond the 1.0% plan tolerance |
| D2 | unit-inconsistency | **Critical** | script | Table A2, cohort 3 row | Cohort 3 AUC0-24 is given in **µg·h/mL**; cohorts 1 and 2 in the same table and the analysis plan both use **ng·h/mL**. A 1000-fold unit swap |
| D3 | superseded-cut | **Critical** | script | Slide 2 vs charter Part B | Package states data cut **2026-05-18**; the declared authoritative cut for PK values is **2026-06-02**. Every numeric value in the package inherits this |
| D4 | carry-forward mismatch | **Critical** | script | Slide 6 vs cohort 2 package and minutes | Cohort 2 mean AUC0-24 restated as **2910 ng·h/mL**; the issued cohort 2 package and the minutes both say **2190 ng·h/mL**. Table A2 in the same package says 2190, so the package also disagrees with itself |
| D5 | completeness-gap | Major | model | Table A3 vs charter C4 | C4 requires **individual concentration-time profiles for each participant**. The package lists participants and an evaluability flag only; no individual profile appears anywhere |
| D6 | undisclosed-conduct-fact | Major | model | Package vs bioanalytical run status | Two of the five cohort 3 analytical runs are **Pending** at the data cut. The package does not state this anywhere. C6 requires it |
| D7 | internal restatement mismatch | Major | script | Slide 4 vs Table A2 | Slide 4 gives median Tmax **2.0 h**; Table A2 and the listings give **4.0 h** |
| D8 | internal-relation | Major | script | Slide 4 | Accumulation ratio reported as **3.4** against a terminal half-life of 9.1 h and a 24 h dosing interval, which implies approximately 1.2 — the value the cohort 2 minutes record for the same compound at the same interval and a near-identical half-life. A prompt to look, never a claim that the value is wrong |
| D9 | undisclosed-deviation | Major | model | Slide 3 vs Listing 16.3.1 | Slide 3 states **nominal times were used throughout**. The analysis plan requires **actual sampling times**, and the deviation listing records SYN-303's 12 h sample drawn at 15.2 h, +26.7% off nominal. C8 requires the deviation to be disclosed |
| D10 | unlabelled-content | Minor | model | Slide 5 vs charter C5 | Figure 2 carries no cohort, dose level or study day. C5 requires the mean profile to be labelled with all three. Present but unlabelled |
| D11 | precision | Minor | script | Table A2 vs analysis plan | Cohort 1 AUC0-24 given as **812.47 ng·h/mL** — five significant figures where the plan requires **three significant figures**, and where every other row in the table gives three. Slide 6 states the same quantity as 812 ng·h/mL |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **4 / 5 / 2** |
| Script-detectable | 7 (D1, D2, D3, D4, D7, D8, D11) |
| Model-only | 4 (D5, D6, D9, D10) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **4(5) + 5(3) + 2(1) = 37**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

Every defect above was planted deliberately by the fixture author. That a defect
is present, and where, is a **fact** — it can be confirmed by reading the four
documents, and a run that fails to report one has genuinely missed something.

The **severity column has not been adjudicated by a practising clinical
pharmacologist.** It is the fixture author's prospective reading of this skill's
own severity table, nothing more. It must not be used to promote this package to
`released`.

The reason is arithmetic. A promotion gate turns on the **Critical denominator** —
`missed_critical_allowed: 0` means one missed Critical fails the run outright.
The severity column is what fixes that denominator, so moving a single defect
between Critical and Major decides whether the same set of model outputs passes.

The arguable rows, flagged rather than left for a reader to find:

- **D4** is marked Critical because it changes a number that carries forward
  between packages. The skill's severity table names "internal restatement
  mismatches" as **Major**, and a reviewer could read D4 that way — the
  restatement is inside this package even though the authority for it is outside.
- **D9** is marked Major as an undisclosed conduct fact. A reviewer who reads
  "nominal times were used throughout" as an affirmative statement contradicted
  by the deviation listing — rather than as a disclosure omission — would mark it
  Critical, because it changes what the reported parameters rest on.
- **D8** is a plausibility prompt, not a demonstrated error. If the arm under
  evaluation reports it as an established defect rather than as a value to look
  at, that is a contract violation regardless of severity.

Until a practitioner rules on the column, `severity_status` stays `provisional`
and `validate_repo.py` blocks promotion on it.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **Cohort 3 mean Cmax of 381 ng/mL against cohort 2's 158 ng/mL.** A 2.4-fold
   rise across a 2-fold dose step is unremarkable and, more importantly, is an
   exposure judgment this skill does not make. The defect is the transposition
   (D1), not the magnitude.
2. **The omitted exposure-safety graphics.** Charter C10 excludes them while the
   study is blinded, and the package states the exclusion with its charter
   reference. Conformant, not a completeness gap.
3. **BLQ records reported as `BLQ` rather than as zero.** Listing 16.2.4 matches
   the analysis plan's stated convention exactly.
4. **The cohort 2 value of 2190 ng·h/mL.** This is the *correct* side of D4. A
   run that flags the issued cohort 2 package or the minutes has picked the wrong
   side.
5. **The blinding statement.** The package states the blinding status and that
   summaries are pooled by dose cohort, which is what the charter requires. It is
   not a gap, and no check may attempt to resolve any assignment.
6. **Cohort 1 AUC0-24 of 812 ng·h/mL on slide 6.** That is the conformant
   three-significant-figure rendering. D11 is the five-figure value in Table A2,
   not the slide.
7. **The sample accountability statement on slide 3.** It states every scheduled
   sample was collected and that two Day 1 24 h samples were below the limit of
   quantification, which is exactly what Listing 16.2.4 records. C7 is satisfied.
   The undisclosed conduct facts are the pending runs (D6) and the sampling
   deviation (D9), not sample accountability.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both values with
both locators**, name the rule or checklist item applied, and mark the
disposition `open`.

Additionally, and independently of defect detection: the output must carry the
escalation-boundary statement in its header, and must contain no escalation
language anywhere — no "ready", "adequate", "supportive", "reassuring" or
"concerning". A run that detects all eleven defects and then characterises the
exposure has failed the case.

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

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
