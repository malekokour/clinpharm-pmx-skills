severity_status: adjudicated
# Expert key — synthetic Module 2.7.2 fixture, programme RLT (relotinib)

> **Answer key. Do not supply this to the model under evaluation.**
>
> 12 planted defects across the five-part structure check, the dose
> reconciliation against Modules 2.7.3 and 2.7.4, the Module 5 placement check,
> source fidelity, and citation hygiene. Every one is discoverable from the four
> supplied documents alone.

## Fixture documents

| File | Role |
|---|---|
| `synthetic-module-272-draft.md` | I2 — the draft Module 2.7.2 under review |
| `synthetic-module-273-274-extracts.md` | I3 + I4 — dose passages from 2.7.3 and 2.7.4 |
| `synthetic-source-csr-synopses.md` | I6 + I7 — source CSR synopses and the modelling report list |
| `synthetic-module5-index-and-conventions.md` | I1 + I5 + I8 + I9 + I10 — owner, study index, conventions, version baseline |

## The twelve

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | numeric-mismatch | **Critical** | value comparison, 2.7.2 against 2.7.4 | 2.7.2.1 vs 2.7.4.1 | 2.7.2.1 states the recommended Phase 3 dose is **80 mg once daily**; 2.7.4.1 and 2.7.3.3 both state **60 mg once daily**. 2.7.4.2 adds that no dose group received more than 60 mg once daily |
| D2 | unit-inconsistency | **Critical** | value comparison, 2.7.2 against its source CSR | 2.7.2.2 RLT-1001 vs RLT-1001 CSR | Cmax reported as **318 µg/mL**; the CSR reports **318 ng/mL** and the dossier conventions forbid µg/mL anywhere in Module 2. A 1000× unit swap |
| D3 | contradiction | **Critical** | direction stated against the ratio reported | 2.7.2.3 vs RLT-1004 CSR | 2.7.2.3 states azolimide **decreased** relotinib exposure by approximately 3.1-fold; the CSR reports an AUC geometric mean ratio of **3.14** and states exposure was higher. Direction reversed, and a dose-reduction instruction is proposed on the reversed reading |
| D4 | structure-misplacement | Major | five-part structure validation | 2.7.2.2 vs 2.7.2.3 | The cross-study population pharmacokinetic covariate analysis is written into **2.7.2.2 Summary of Results of Individual Studies**. Cross-study and modelling analyses belong in 2.7.2.3 |
| D5 | structure-incomplete | Major | five-part structure validation | Between 2.7.2.3 and 2.7.2.5 | **Part 2.7.2.4 Special Studies is absent.** The draft runs 2.7.2.3 straight into 2.7.2.5, so four of the five parts are present |
| D6 | placement-error | Major | placement check on the primary objective | Module 5 index, RLT-1007 | RLT-1007's stated primary objective is the pharmacokinetics of relotinib in renal impairment — an intrinsic-factor PK study, which the submission's own legend places in **5.3.3.3**. It is filed in **5.3.5.1**, controlled clinical studies |
| D7 | unsupported-claim | Major | claim traced to the source list | 2.7.2.3 | "The exposure–response analysis demonstrated no clinically relevant relationship between exposure and QTc interval." No exposure–QTc analysis exists in either modelling report, and the RLT-1009 CSR states explicitly that none was performed |
| D8 | completeness-gap | Major | count against the study index | 2.7.2.1 vs Module 5 index | 2.7.2.1 states **Six clinical pharmacology studies** were conducted; the index states **Seven clinical pharmacology studies** are placed in Module 5. RLT-1002, the food-effect study, is summarised nowhere in 2.7.2 |
| D9 | stale-version | Minor | citation resolution against the baseline | 2.7.2.5 appendix table vs baseline | Cites the bioanalytical method summary as **BAS-RLT-002 v1.0**; the baseline declares **BAS-RLT-002 v3.0** authoritative |
| D10 | presentation | Minor | convention applied from I10 | 2.7.2.2 RLT-1001 | AUC0–24 restated as **1240.5 ng·h/mL**, five significant figures, where the dossier conventions require **three significant figures** in Module 2 |
| D11 | presentation | Minor | cross-reference resolution | 2.7.2.3 vs 2.7.2.5 | Refers to **Appendix 2.7.2.5.3**; the appendix table lists only 2.7.2.5.1 and 2.7.2.5.2. The reference resolves to nothing |
| D12 | numeric-mismatch | Major | value comparison, 2.7.2 against its source CSR | 2.7.2.2 RLT-1001 vs RLT-1001 CSR | The multiple-dose regimen is described as **40 mg twice daily**; the CSR states **40 mg once daily** and adds that no twice-daily regimen was studied at any dose level |

## Counts

| | |
|---|---|
| Total | 12 |
| Critical / Major / Minor | **3 / 6 / 3** |
| Value-comparison path (`either`) | 6 (D1, D2, D3, D6, D8, D12) |
| Structure, traceability and reading path (`model`) | 6 (D4, D5, D7, D9, D10, D11) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → maximum weighted score
**3(5) + 6(3) + 3(1) = 15 + 18 + 3 = 36**

## Severities are PROVISIONAL

**Defect *presence* is certain. Defect *severity* is not.**

All twelve items were planted deliberately. That a discrepancy exists at each
location is a fact about this fixture, and a run that fails to report one has
genuinely missed something real.

The **severity** column is a different kind of claim, and **it has not been
adjudicated by a practitioner.** It is the fixture author's prospective
application of this skill's own severity table, nothing more.

The Critical denominator is what a promotion gate turns on: the release rule is
that no Critical may be missed, so which three of these twelve are Critical
decides whether a run passes. Move one row between Critical and Major and the
same output changes verdict with nothing about the run having changed.

Consequences, all binding:

- **This package may not be promoted to `released` on the strength of this key.**
  `severity_status: provisional` on line 1 is machine-read by
  `scripts/validate_repo.py`, which fails the build if a `released` package
  carries a provisional key.
- Runs graded against this key are **diagnostic evidence, not release evidence**.
- Adjudicating severities after outputs have been inspected turns every run
  already graded into diagnostic evidence and requires a fresh held-out rerun.

Rows the author is least confident about, flagged for the adjudicator:

- **D6** placement. Graded Major on the skill's own table, which puts "a study
  placed in the wrong Module 5 section" under Major. A reviewer who weighs the
  filing consequence at a dossier freeze would argue Critical.
- **D12** regimen. Graded Major because it does not change the reported exposure
  numbers, but a twice-daily regimen that was never studied is arguably a
  Critical fidelity failure on the same reasoning that makes D1 Critical.
- **D5** the missing part. Graded Major as a structural gap; a reviewer running a
  dossier-freeze pass may treat an absent required part as Critical.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **RLT-1012 hepatic impairment filed in 5.3.3.3.** Correct under the
   submission's own section legend. Only RLT-1007 is misplaced, and a run
   flagging both intrinsic-factor studies has over-reported D6.
2. **The RLT-1001 CSR reporting AUC0–24 as 1240.5 ng·h/mL.** The
   three-significant-figure convention binds Modules 2.7.2, 2.7.3 and 2.7.4 by
   its own wording. The finding is the Module 2 restatement, not the CSR.
3. **2.7.3 and 2.7.4 both stating 60 mg once daily.** They agree with each other.
   The disagreement is between 2.7.2 and both of them; a run reporting a
   2.7.3-versus-2.7.4 conflict has manufactured one.
4. **RLT-1004 Cmax ratio 2.06 alongside AUC ratio 3.14.** Different parameters
   moving by different amounts, both increases. Not a mismatch.
5. **RLT-2001 appearing in the population pharmacokinetic pooling but not in the
   Module 5 clinical pharmacology index.** RLT-2001 is a Phase 2 efficacy study,
   not a clinical pharmacology study. Its absence from that index is correct and
   is not the completeness gap D8 describes.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both statements
with both locators** and mark the disposition `open`. A run that decides which of
two conflicting doses is correct, that renumbers or moves a section to fix D4 or
D5, or that declares the section ready to file has violated the human-review
contract regardless of whether its guess was right.

The ownership gate applies throughout: the accountable owner comes from the I1
declaration in `synthetic-module5-index-and-conventions.md`, and every
ownership-dependent statement is labelled `PROVISIONAL-PRACTICE`.

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

## K07 remediation addendum — provisional

Cases 11 and 12 add ownership-boundary and non-vacuous route assertions. Case
12 reuses planted defect D1 and changes neither the twelve-defect denominator
nor any severity. Both remain diagnostic pending adjudication and the complete
HIGH gate.

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
