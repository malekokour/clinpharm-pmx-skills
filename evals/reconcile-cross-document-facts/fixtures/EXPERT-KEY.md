severity_status: adjudicated
# Expert key — synthetic programme-thread fixture DVS-100 (dorvastine)

> **Answer key. Do not supply this to the model under evaluation.**
>
> Eleven planted defects across the thread's three programme-specific patterns —
> `orphan-fact`, `commitment-drift`, `propagation-gap` — and the ledger classes
> they are recorded under. Every one is discoverable from the four supplied
> documents alone. The rounding convention, the unit convention, the version
> baseline and the study identities are all stated inside the fixture, so no
> outside rule is needed.

## The documents

| File | Plays the part of |
|---|---|
| `synthetic-thread-inventory.md` | I1 thread inventory, I2 source-version baseline, I9 conventions, I7 already-submitted statements |
| `synthetic-csr-extracts.md` | I4 clinical study reports — origin of most programme values |
| `synthetic-module-272.md` | I6 Module 2.7.2 — the principal summarising consumer |
| `synthetic-proposed-label.md` | I8 proposed label — terminal consumer of the thread |

## The eleven

| ID | Class (sub-type) | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | stale-version (`propagation-gap`) | **Critical** | script | Label §12.3 vs CSR §12.3 | Label states apparent clearance **16.8 L/h**; the authoritative CSR v2.0 and Module 2.7.2 both say **18.4 L/h**. A wrong value that has already reached the label |
| D2 | contradiction (`commitment-drift`) | **Critical** | either | 2.7.2 §2.7.2.3 vs submitted Briefing Document | Module 2.7.2 says **Steady state is achieved by Day 8**; the Briefing Document submitted 2026-02-14 says **Steady state is achieved by Day 5**, and so does CSR §12.2. A later document contradicting a statement already sent to a health authority |
| D3 | unit-inconsistency | **Critical** | script | Label §12.3 vs CSR §12.4 | Label gives steady-state peak concentration as **1240 µg/mL**; the CSR says **1240 ng/mL** and the conventions say concentrations are reported in ng/mL. A 1000× unit swap in labelling text |
| D4 | completeness-gap (`orphan-fact`) | Major | model | 2.7.2 §2.7.2.1 vs inventory | Module 2.7.2 states **Absolute bioavailability is 62%**. The inventory says **No absolute bioavailability study is included in this thread.** The value has no origin anywhere upstream |
| D5 | stale-version | Major | script | 2.7.2 §2.7.2.2 vs baseline | Module 2.7.2 summarises from **DVS-101 CSR v1.0**; the baseline names **DVS-101 CSR v2.0 (authoritative, issued 2026-04-30)** and records v1.0 superseded after an NCA re-run |
| D6 | presentation | Minor | script | 2.7.2 §2.7.2.2 vs conventions | AUC written **4210.00 ng·h/mL** against the convention **Exposure parameters are reported to three significant figures.** The value itself agrees with the CSR — only the presentation breaches the rule |
| D7 | contradiction | Major | script | 2.7.2 §2.7.2.3 vs DVS-103 §3.1 | Module 2.7.2 reports **a 34% decrease in AUC** with food; the food-effect report says **a 34% increase in AUC**, geometric mean ratio 1.34. Direction reversed |
| D8 | numeric-mismatch | Major | script | 2.7.2 §2.7.2.2 vs CSR §11.2 | Module 2.7.2 says the population pharmacokinetic dataset comprised **412 subjects**; the CSR says **398 subjects** |
| D9 | contradiction | Major | script | 2.7.2 §2.7.2.3 vs inventory | Module 2.7.2 sources the food-effect result to **Study DVS-102**. The inventory states **The food-effect study in this thread is DVS-103.** and that DVS-102 carries no food-effect result |
| D10 | presentation | Minor | script | Label header vs inventory | Label header carries **Effective date: 2026-01-06**; the inventory records the label draft as **effective 2026-06-01**. Transposed |
| D11 | presentation | Minor | script | 2.7.2 title | Module 2.7.2 titles the compound **DSV-100**; every other document says **DVS-100** |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **3 / 5 / 3** |
| Script-detectable | 9 (D1, D3, D5, D6, D7, D8, D9, D10, D11) |
| Script + model (`either`) | 1 (D2) |
| Model-only | 1 (D4) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **3(5) + 5(3) + 3(1) = 33**

Severity here is calibrated to **how far the fact still has to travel**, per the
skill's own rubric — which is why D1 and D3, both already in the label, outrank
D8, a larger-looking numeric error still inside an internal draft.

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

All eleven were planted deliberately by the fixture author. That each is present
is a fact about how this fixture was built, and it is not open to disagreement.

The severity column is a claim of a different kind, and **no practitioner has
adjudicated it.** It is the fixture author's provisional reading of the
travel-distance rubric in `SKILL.md`, recorded so the suite has something to
score against — not a reviewed determination. The travel-distance calibration
makes it especially movable: whether a value counts as having "reached" a draft
label is exactly the judgement a practitioner should make and this key has not.

**This package may not be promoted to `released` on the strength of this key.**
The promotion gate turns on the Critical denominator — "missed no Critical" is
undefined until the Critical count is settled — and moving one defect between
Critical and Major moves that denominator underneath every run already scored
against it. On the CSR fixture, one severity re-scored after outputs had been
inspected converted nine completed runs from release evidence into diagnostic
evidence.

`severity_status: provisional` on line 1 is machine-read by
`scripts/validate_repo.py`, which fails the build if this package is marked
`released` while that line still reads `provisional`. Promotion requires a
practitioner adjudication of the severity column, dated and recorded here, and a
fresh held-out rerun against the frozen key.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **AUC 4210 ng·h/mL in the CSR against 4210.00 ng·h/mL in Module 2.7.2.** The
   values agree exactly and sit inside the 0.5% tolerance the conventions set.
   The defect (D6) is the significant-figure breach, not a numeric mismatch, and
   reporting it as one misstates what a reviewer has to fix.
2. **Study DVS-102 existing in the thread.** It is the relative bioavailability
   study, listed in the inventory, with a legitimate result. The defect (D9) is
   Module 2.7.2 citing it for the food-effect result, not the study itself.
3. **Terminal half-life of 14 h in the CSR, Module 2.7.2 and the label.** Three
   documents, one value, no conflict. This is what a clean thread looks like.
4. **Two versions of the DVS-101 CSR existing.** The baseline records v1.0 as
   superseded openly. Holding superseded versions is normal; the defect (D5) is
   Module 2.7.2 summarising *from* the superseded one.
5. **The label's "Administration with a high-fat meal increases exposure."**
   That agrees in direction with the food-effect report. The reversal (D7) is in
   Module 2.7.2, and a run that flags the label sentence has picked the wrong
   side of it.

## Adjudication boundary

Every defect is reported with **both statements, both locators and both dates**,
disposition `open`. A run that decides which clearance value is correct, that
declares the commitment drift a correction rather than an error, that judges a
discrepancy clinically meaningful or not, or that applies the proposed
source-version record rather than proposing it has violated the skill's boundary
regardless of what else it found.

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
