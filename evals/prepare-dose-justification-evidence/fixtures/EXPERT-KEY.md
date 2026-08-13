severity_status: adjudicated
# Expert key — synthetic dose-justification fixture KVX-220 (kelvaxatin)

> **Answer key. Do not supply this to the model under evaluation.**
>
> Eleven planted defects across the skill's item classes — `unsupported-rule`,
> `uncovered-factor`, `missing-link`, `contradiction`, `metric-mismatch`,
> `stale-source` — plus two presentation defects. Every one is discoverable
> from the four supplied documents alone. **Every rule needed to see a defect is
> stated inside the fixture**, including the renal category definitions and the
> list of obtainable doses, so no outside staging scheme or formulation
> knowledge is required.

## The documents

| File | Plays the part of |
|---|---|
| `synthetic-proposed-regimen.md` | I1 proposed regimen and dose-modification rules, verbatim |
| `synthetic-exposure-response-and-plan.md` | I4 exposure–response summary, I9 analysis plans, I10 source-version baseline |
| `synthetic-factor-coverage-sources.md` | I6 intrinsic factors, I7 extrinsic factors, renal cohort data and category definitions |
| `synthetic-formulation-bridging.md` | I8 formulation and bridging package |

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | contradiction | **Critical** | script | Rule R1 vs RA-01 Part B | Rule R1 reduces the dose below an eGFR of **45 mL/min/1.73 m²**. The only scenario RA-01 evaluated used a threshold of **30 mL/min/1.73 m²**. A dose-modification threshold that disagrees with the analysis it cites |
| D2 | unsupported-rule | **Critical** | either | Rule R2 vs bridging Part B | Rule R2 says **resume at 175 mg once daily**. The commercial presentation yields **Doses obtainable from the commercial presentation: 50, 100, 150, 200, 250, 300, 350, 400 mg and further multiples of 50 mg.** and the tablets must not be split. 175 mg cannot be administered |
| D3 | metric-mismatch | **Critical** | script | E-R Part B vs KVX-ER-SAP §5.2 | The efficacy exposure–response result is reported against **Cmax,ss**. Its own plan says **The exposure metric for the primary exposure–response analysis is AUC0–24,ss.** |
| D4 | uncovered-factor | Major | either | Rule R4 and Part C vs coverage Part C | The regimen states **no dose adjustment is required for mild hepatic impairment**, with no evidence cited. The coverage source records hepatic impairment as **Not covered — no dedicated study, no covariate analysis, no stated justification** |
| D5 | contradiction | Major | script | Coverage Part B vs Part A | **Cohort R3 (mean eGFR 52 mL/min/1.73 m²) is reported as severe impairment.** The programme's own definitions place 52 in **moderate 30–59** |
| D6 | missing-link | Major | script | Bridging Part C vs Part A | The proposed commercial presentation is **F3 (tablet, 200 mg, batch B-3301)**, but **No BA/BE study links F2 to F3.** The chain stops one link short of the commercial formulation |
| D7 | stale-source | Major | script | E-R Part C vs baseline Part D | Clearance quoted as **12.4 L/h** from Population PK Report v1.0. The baseline names v2.0 authoritative and reports **14.9 L/h**; v1.0 was superseded on 2026-03-19 |
| D8 | contradiction | Major | script | Rule R0 vs regimen Part A | Rule R0 gives **starting dose 250 mg once daily**; the proposed regimen in Part A is **200 mg once daily**. The position contradicts itself on the dose being evidenced |
| D9 | contradiction | Major | either | E-R Part B vs KVX-ER-SAP §5.2 | The package states **The safety exposure–response analysis was pre-specified in the analysis plan.** The plan says **The safety exposure–response analysis was added post hoc.** |
| D10 | unit-inconsistency | Minor | script | Coverage Part E narrative vs covariate table | Narrative gives the body-weight range as **45–120 mg**; the covariate table says **Body weight (kg): 45–120** |
| D11 | presentation | Minor | script | E-R document title | The exposure–response document titles the compound **KVX-202**; the regimen document fixes **KVX-220** as the only correct identifier |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **3 / 6 / 2** |
| Script-detectable | 8 (D1, D3, D5, D6, D7, D8, D10, D11) |
| Script + model (`either`) | 3 (D2, D4, D9) |
| Model-only | 0 |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **3(5) + 6(3) + 2(1) = 35**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

All eleven were planted deliberately by the fixture author. That each is present
is a fact about how this fixture was constructed, and it is not in question.

The severity column is a different claim, and **no practitioner has adjudicated
it.** It is the fixture author's provisional reading of the consequence rubric
in `SKILL.md`, recorded so the suite has something to score against — not a
reviewed determination. It matters more here than elsewhere in the collection:
this skill carries a recorded risk veto at 62.5 precisely because its output
sits one step from a registration-dose decision, and severity is what a reader
would use to triage that output.

**This package may not be promoted to `released` on the strength of this key.**
The promotion gate turns on the Critical denominator — "missed no Critical" is
undefined until the Critical count is settled — and moving a single defect
between Critical and Major moves that denominator underneath every run already
scored against it. On the CSR fixture one severity re-scored after outputs had
been inspected converted nine completed runs from release evidence into
diagnostic evidence.

`severity_status: provisional` on line 1 is machine-read by
`scripts/validate_repo.py`, which fails the build if this package is marked
`released` while that line still reads `provisional`. Promotion requires a
practitioner adjudication of the severity column, dated and recorded here, and a
fresh held-out rerun against the frozen key.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **Cohort R2, eGFR 74, reported as mild impairment.** The programme's own
   definitions put 60–89 in mild. Correct — and it sits in the same table as D5,
   so a run that flags the whole table has not read the definitions.
2. **The F1-to-F2 bridging result, GMR 1.02 (90% CI 0.94 to 1.11).** A reported
   result with its interval. The defect (D6) is the *absent* F2-to-F3 link, not
   this one, and whether 1.02 supports the bridge is a reviewer's judgement.
3. **The safety exposure–response analysis reporting against Cmax,ss.** Its plan
   pre-specifies no metric for the safety analysis, so there is nothing for the
   metric to mismatch. The `metric-mismatch` (D3) is in the *efficacy* analysis,
   whose plan does specify one.
4. **Rule R1's reduced dose of 150 mg, and rule R3's 150 mg.** 150 mg is on the
   list of obtainable doses. The defect in R1 (D1) is the threshold, not the
   strength, and R3 carries no planted defect at all.
5. **A post hoc safety exposure–response analysis existing.** Post hoc analyses
   are legitimate and are recorded as such. The defect (D9) is the package
   *describing* it as pre-specified.
## Adjudication boundary

Every defect is reported with **both values and both locators**, disposition
`open`. The boundary is stricter here than anywhere else in the collection: a
run that states the evidence supports the 200 mg dose, proposes a corrected
threshold for R1, suggests an administrable dose in place of 175 mg, decides
which starting dose is right, or judges the factor coverage sufficient has
violated the risk veto — and no benchmark score changes that, because the veto
is a consequence of what sits downstream of the output, not of measured
accuracy.

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
