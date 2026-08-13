severity_status: adjudicated
# Expert key — synthetic bioanalytical fixture ZLV-102 / BA-VAL-2025-041

> **Answer key. Do not supply this to the model under evaluation.**
>
> 11 planted defects across the ICH M10 conformance rubric and the PK-relevance
> pass. Every one is discoverable from the four supplied documents alone; none
> requires outside knowledge, and none requires a threshold or acceptance
> criterion that the documents do not themselves state.

## Fixture documents

| File | Role |
|---|---|
| `synthetic-validation-report.md` | I1 — method validation report BA-VAL-2025-041 v2.0 |
| `synthetic-sample-analysis-report.md` | I2 — study sample analysis report BA-SSA-2025-088 v1.0 |
| `synthetic-protocol-sample-handling.md` | I5 + I3 + I7 — sample handling, declared standard, version baseline |
| `synthetic-pk-analysis-plan.md` | I6 — BLQ handling and concentration conventions |

## Detection paths in a package that ships no script

`review-bioanalytical-report` ships no script, so **no defect here is
script-only**. The `detected_by` values in the case file are `either` where the
defect is a literal value comparison a shipped consistency tool would also catch,
and `model` where finding it requires reading the rubric against the report. The
"detection path" column below describes what the reviewer actually has to do.

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | cross-document-inconsistency | **Critical** | value comparison across I2 and I1 | SSA §3.3 vs validation §7 | Study samples stored at −70 °C for up to **14 months**; long-term matrix stability is demonstrated only to **9 months**. Concentrations from the earliest samples sit outside the demonstrated window |
| D2 | cross-document-inconsistency | **Critical** | value comparison across I2 and I6 | SSA §5 vs analysis plan §3.2 | Below-limit results were reported as **0.00 ng/mL**; the PK analysis plan requires them **set to missing** and states explicitly that they are not imputed as zero. A silent propagation into AUC and half-life |
| D3 | cross-document-inconsistency | **Critical** | value comparison across I2 and I1 | SSA §6 vs validation §6 | 46 samples reanalysed after **20-fold** dilution; dilution integrity is demonstrated at **10-fold** only, and the validation states no higher factor was assessed. Affects the high end of the profile, where Cmax sits |
| D4 | cross-document-inconsistency | Major | value comparison across I2 and I1 | SSA §4 vs validation §2 | LLOQ applied to study samples stated as **0.250 ng/mL**; the authoritative validation report states **0.500 ng/mL** |
| D5 | internal-inconsistency | Major | recomputation from the report's own table (model-performed arithmetic) | SSA §8 and Table 8.1 | Text states **94.0%** of ISR pairs met the criterion; the table it summarises shows **62 of 70** pairs within ±20%, which is 88.6% |
| D6 | missing-element | Major | rubric walk | Validation report, whole document | The **carryover assessment** rubric element is absent from the validation report. SSA §10 defers to the validation report for it, so neither document carries it |
| D7 | cross-document-inconsistency | Major | value comparison across I2 and I1 | SSA §7 vs validation §7 | Repeated samples underwent up to **5 freeze-thaw cycles**; stability is demonstrated over **3 freeze-thaw cycles** |
| D8 | stale-version | Minor | citation resolution against the baseline | SSA §2 vs baseline table | SSA cites the method as **BA-VAL-2025-041 v1.0**; the declared authoritative version is **BA-VAL-2025-041 v2.0** |
| D9 | internal-inconsistency | Minor | header-against-text comparison | Validation Table 3 vs validation §2 | Table 3 header reads **Nominal concentration (µg/mL)** while the stated calibration range is **0.500 to 500 ng/mL** and the analysis plan states no concentration is reported in µg/mL |
| D10 | incomplete-element | Minor | rubric walk | Validation Table 4 | Between-run precision is **not reported** at the LLOQ QC, while the rubric element covers accuracy and precision within *and* between run |
| D11 | internal-inconsistency | Major | reading two sections against each other | SSA §9 vs SSA §3.2 | §9 states **No protocol deviations affected sample analysis**; §3.2 records that Cohort 2 samples were **received at +4 °C rather than on dry ice**, a documented shipping deviation |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **3 / 5 / 3** |
| Value-comparison path (`either`) | 6 (D1, D2, D3, D4, D7, D8) |
| Reading / rubric-walk path (`model`) | 5 (D5, D6, D9, D10, D11) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → maximum weighted score
**3(5) + 5(3) + 3(1) = 15 + 15 + 3 = 33**

## Severities are PROVISIONAL

**Defect *presence* is certain. Defect *severity* is not.**

Every one of the eleven items above was planted deliberately by the fixture
author. That a discrepancy exists at each location is a fact about this fixture,
and a run that fails to report one has genuinely missed something.

The **severity** column is a different kind of claim. **It has not been
adjudicated by a practitioner.** It is the fixture author's prospective reading
of the skill's own severity rubric, nothing more.

This matters because a promotion gate turns on the Critical denominator: the
release rule is that **no Critical may be missed**, so which three of these
eleven are Critical decides directly whether a given run passes or fails. Move
one row between Critical and Major and the same run output changes verdict
without a single character of the run changing.

Consequences, all binding:

- **This package may not be promoted to `released` on the strength of this key.**
  `severity_status: provisional` on line 1 is machine-read by
  `scripts/validate_repo.py`, which fails the build if a `released` package
  carries a provisional key.
- Runs graded against this key are **diagnostic evidence, not release evidence**.
- If severities are adjudicated after outputs have been inspected, every run
  already graded becomes diagnostic and a fresh held-out rerun is required — the
  B20 precedent recorded in `evals/review-csr-pk-consistency/fixtures/EXPERT-KEY.md`.
- The adjudicating reviewer for this fixture should include, or consult, someone
  qualified in bioanalysis. Whether storage beyond the demonstrated stability
  window is Critical rather than Major is a bioanalytical judgment, not a
  documentation one.

Two rows the author is least confident about, flagged for the adjudicator:

- **D11** is graded Major as a *reporting* contradiction. A reviewer who reads it
  as a thermal excursion affecting reported concentrations would grade it
  Critical.
- **D9** is graded Minor as presentation. A reviewer who treats any µg/mL versus
  ng/mL appearance as a 1000× unit hazard would grade it Critical, as the
  reference CSR fixture grades its own unit swap.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **QC concentrations (1.50, 40.0, 400 ng/mL) differing from the calibration
   standard concentrations.** Validation §3 states the QCs are set independently
   of the standards as the laboratory's practice. Not a mismatch.
2. **The 4 samples reanalysed after 10-fold dilution (SSA §6).** These sit inside
   the demonstrated dilution integrity. Only the 20-fold set is outside it, and a
   run that flags all 50 diluted samples has over-reported D3.
3. **LLOQ 0.500 ng/mL for quexatinib against 1.00 ng/mL for metabolite M1.**
   Different analytes with different calibration ranges, both stated in validation
   §2. Not an internal inconsistency.
4. **LLOQ QC bias of +18.2% against mid QC bias of +4.1%.** The report states its
   own acceptance criterion in §11 as ±20% at the LLOQ QC and ±15% elsewhere, and
   +18.2% meets it. Flagging this requires supplying a criterion the documents do
   not state — the failure mode this skill's rules single out.
5. **Short-term bench stability of 6 hours against long-term stability of 9
   months.** Validation §7 states explicitly that these are separate conditions
   and that the 6-hour figure does not bound the storage interval. A run treating
   6 hours as the applicable window has picked the wrong side of D1.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both values with
both locators** and mark the disposition `open`. A run that states which value is
correct, that resolves a contradiction, or that declares the method acceptable or
unacceptable has violated the human-review contract regardless of whether its
guess was right.

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
