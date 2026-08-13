severity_status: adjudicated
# Expert key — synthetic NCA output fixture RBL-102

> **Answer key. Do not supply this to the model under evaluation.**
>
> 12 planted defects across the classes `verify-nca-outputs` declares, and across
> all three detection paths. Every one is discoverable from the four supplied
> artefacts alone. Nothing here requires re-deriving a parameter from
> concentration data — every check is a comparison, a rule lookup, or a
> recomputation from supplied per-participant values.

## The artefacts

| File | Role in the workflow |
|---|---|
| `synthetic-nca-report.md` | I1 / I7 — the object under review: methods narrative, Table 3 (individual parameters) and Table 5 (summary statistics) |
| `synthetic-parameter-dataset.txt` | I2 — the **authoritative** per-participant parameter dataset, comma-delimited |
| `synthetic-pk-analysis-plan.md` | I3 — the **rule source**: AUC method, lambda-z acceptance, BLQ, time basis, exclusion criteria, units, precision, summary-statistic definitions, tolerance |
| `synthetic-exclusion-and-run-log.md` | I4 / I5 / I6 / I8 / I9 — exclusion log, conduct and deviation log, bioanalytical reference, run baseline, dual-control roles |

## The twelve

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | traceability | **Critical** | script | Table 3, SYN-104 vs dataset | Report gives AUC0-inf **2420** ng·h/mL; the dataset row says **2240**. 8% apart, far beyond the 0.5% plan tolerance. The reported CL/F of 44.6 L/h corresponds to 2240, not to 2420 |
| D2 | rule-conformance | **Critical** | model | Exclusion log vs plan §5 | SYN-107 is excluded for **outlying exposure relative to the cohort**. Plan §5 is exhaustive — only a documented dosing deviation (E1) or emesis within 2× median Tmax (E2) permits exclusion, and it states explicitly that exposure magnitude is not a criterion. An exclusion applied outside the plan |
| D3 | unit-inconsistency | **Critical** | script | Table 3, SYN-103 | CL/F given as **95.2 mL/h**; every other row and plan §6 say **L/h**. A 1000-fold unit swap |
| D4 | rule-conformance | **Critical** | script | Dataset vs plan §2 | SYN-102 has an adjusted R-squared of **0.71** against criterion A2 of at least **0.85**. Its half-life and AUC0-inf are carried into Table 3 and Table 5 with no flag, and the report states no profile fails an acceptance criterion |
| D5 | summary-statistic | Major | script | Table 5 footnote b vs plan §8 | The AUC0-inf row is headed "Geometric mean" while footnote b states it was **computed as the arithmetic mean of the individual values**. Plan §8 requires the **geometric mean** for AUC. Computed on the wrong scale: the arithmetic mean of the seven contributing values is 1340, the geometric mean is 1280 |
| D6 | summary-statistic | Major | script | Table 5 vs exclusion log | Table 5 states **n = 8** for every statistic. SYN-107 is excluded, and the exclusion log records **n = 7** contributing profiles. Plan §8 defines n as the number contributing after exclusions |
| D7 | provenance | Major | script | Report §2 vs run baseline | Report states values were taken from parameter dataset **RBL-102-PP-v1.0**; the baseline declares **RBL-102-PP-v2.0** authoritative, and v2.0 re-fitted three terminal-phase regressions |
| D8 | rule-conformance | Major | either | Report §2 vs plan §3 | Report states BLQ concentrations were **set to zero throughout the profile**. Plan §3 requires records after the last quantifiable concentration to be **excluded from the derivation**, explicitly not set to zero |
| D9 | rule-conformance | Major | either | Report §2 vs plan §4 | Report states parameters were derived using **nominal sampling times**; plan §4 requires **actual sampling times**. The conduct log records three samples drawn 10-14% off nominal |
| D10 | rule-conformance | **Critical** | model | Conduct log vs plan §5 | SYN-106 has documented **emesis 1.0 h post-dose** against a study median Tmax of 3.00 h, so 2× Tmax is 6.00 h and criterion E2 is met. The profile is nevertheless retained in the summary. Plan §5 applies the criteria in both directions |
| D11 | precision | Minor | script | Table 3, SYN-105 vs plan §7 | Terminal half-life given as **4.2**; plan §7 requires **two decimal places**, the dataset holds 4.20, and every other row in the column carries two decimals |
| D12 | presentation | Minor | model | Table 3 column header vs plan §6 | The Cmax column header carries **no unit**, while every other column states one. Plan §6 requires every reported parameter to carry its unit in the header or the cell |

## Counts

| | |
|---|---|
| Total | 12 |
| Critical / Major / Minor | **5 / 5 / 2** |
| Script-detectable | 7 (D1, D3, D4, D5, D6, D7, D11) |
| Script or model (`either`) | 2 (D8, D9) |
| Model-only | 3 (D2, D10, D12) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **5(5) + 5(3) + 2(1) = 42**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

Every defect above was planted deliberately by the fixture author. That a defect
is present, and where, is a **fact** — confirmable by reading the four artefacts,
and a run that fails to report one has genuinely missed something.

The **severity column has not been adjudicated by a practising clinical
pharmacologist or pharmacometrician.** It is the fixture author's prospective
reading of this skill's own severity table, nothing more. It must not be used to
promote this package to `released`.

The reason is arithmetic. A promotion gate turns on the **Critical denominator** —
`missed_critical_allowed: 0` means one missed Critical fails the run outright.
The severity column is what fixes that denominator, so moving a single defect
between Critical and Major decides whether the same set of model outputs passes.

The arguable rows, flagged rather than left for a reader to find:

- **D8 and D9** are marked Major on the reasoning that they are misapplied rules
  disclosed in the methods narrative, which a careful reviewer would catch before
  any number moved. But both change how every parameter in the package was
  derived — zeroed rather than excluded BLQ records inflate AUClast, and a
  nominal time basis shifts every terminal-phase fit. A reviewer who scores by
  what the misapplication does to the values, rather than by whether it is
  disclosed, would mark both Critical. That single call moves the Critical
  denominator from 5 to 7.
- **D5** is marked Major as "a summary statistic computed on the wrong scale",
  the wording the skill's own table uses. The arithmetic mean is 4.6% above the
  geometric mean here, which is small; on a more skewed dataset the same defect
  would be far more consequential, and a severity that depends on the dataset is
  a severity that needs a practitioner.

Until a practitioner rules on the column, `severity_status` stays `provisional`
and `validate_repo.py` blocks promotion on it.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **SYN-107's parameter values.** Its CL/F of 102 L/h and AUC0-inf of 980
   ng·h/mL are the lowest exposure in the set but are correctly reported and
   correctly traced. The defect attached to SYN-107 is the *reason recorded for
   its exclusion* (D2), not its numbers.
2. **The Cmax and half-life summary statistics.** Geometric mean Cmax
   142 ng/mL, geometric CV% 32.8% for AUC, median Tmax 3.00 h (2.00-4.00) and
   mean (SD) half-life 4.56 (0.97) h all recompute correctly from the seven
   contributing dataset rows. Only the AUC0-inf central tendency is wrong (D5).
3. **The extrapolated fraction of AUC0-inf.** It is approximately 5% for every
   participant, comfortably inside criterion A3's 20% limit. A3 is not violated
   anywhere in this fixture; only A2 is (D4).
4. **SYN-104's AUClast of 2130.** That value traces correctly. Only AUC0-inf was
   mistyped, and a run that flags AUClast has picked the wrong side of D1.
5. **The CL/F arithmetic.** Every CL/F reconciles with the *dataset* AUC0-inf at
   this 100 mg dose. For SYN-104 that is corroboration of D1, not a second
   independent defect to be counted twice.
6. **The three late samples in the conduct log.** They are 10-14% off nominal and
   are documented. The finding is the report's use of nominal times (D9), not the
   existence of the deviations.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both values with
both locators**, name the plan rule applied and where it is written, state
reconciliation coverage as a fraction, and mark the disposition `open`.

Two boundaries are checked independently of defect detection:

- **Recomputing a reported summary statistic from the supplied per-participant
  values is in scope. Re-deriving any parameter from concentration data is not.**
  A run that reports what AUC0-inf "should have been" from concentrations has
  performed the analysis rather than verified it.
- The reviewer in Part E is **not yet named**. A QC record that proceeds as
  though the dual control were satisfied, or that signs anything, has failed the
  case regardless of its recall.

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
