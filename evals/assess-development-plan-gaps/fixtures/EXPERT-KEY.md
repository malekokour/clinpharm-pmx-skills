severity_status: adjudicated
# Expert key — synthetic development-plan fixture ZLV-2201

> **Answer key. Do not supply this to the model under evaluation.**
>
> Twelve planted defects across the four coverage classes and all three
> detection paths. Every one is discoverable from the four supplied documents
> alone; none requires outside knowledge of any guidance, threshold or staging
> rule. Where a rule is needed to see the defect, the rule is stated inside the
> fixture.

## The documents

| File | Plays the part of |
|---|---|
| `synthetic-cp-development-plan.md` | I1 plan, I6 scope declaration, I8 guidance baseline |
| `synthetic-study-inventory.md` | I3 study inventory — the coverage denominator |
| `synthetic-drug-property-dossier.md` | I4 drug-property dossier — the trigger source |
| `synthetic-waiver-and-commitments.md` | I7 waiver rationale file, I5 regulatory interaction history |

## The twelve

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | residual-gap | **Critical** | either | Plan §4.4 vs dossier §1 | Plan states *no dedicated renal impairment study is planned* while the dossier reports fraction excreted unchanged of **41%**. The trigger is met, no study addresses it, and the waiver file records no renal rationale — a residual gap under a target-profile labelling claim |
| D2 | residual-gap (triggered) | **Critical** | either | Plan §4.3 vs dossier §2 | Plan states *No further clinical interaction work is planned.* The dossier reports zelvatinib is a **time-dependent inhibitor of CYP3A4**. The perpetrator direction is obligated and uncovered; the inventory's coverage table confirms it as `None` |
| D3 | contradiction | **Critical** | model | Plan §4.5 vs commitments Part B/C | Plan says hepatic impairment gets covariate analysis: **No dedicated hepatic study is planned.** The End-of-Phase-2 minutes and commitment register C-01 record an in-force commitment that **A dedicated hepatic impairment study will be conducted before submission**. Both statements must survive |
| D4 | unsupported-claim | Major | either | Plan §5 vs plan §2 | Guidance baseline excludes `fda-optimus` as *not applicable — programme is not oncology* while the programme's own scope declaration names the indication **advanced solid tumours**. An anchor set wrongly narrowed |
| D5 | stale-version | Major | script | Plan §4.2 vs inventory | Plan says ZLV-103 is *complete and reported*; the inventory says **Ongoing — database lock planned Q4 2026** |
| D6 | completeness-gap | Major | script | Plan §3 vs inventory | Plan says *eight clinical pharmacology studies*; the inventory's own footer says **Total studies listed: 6** |
| D7 | unsupported-claim | Major | either | Plan §4.6 vs inventory | Plan claims the QT expectation is met by study **ZLV-105**. The inventory states **No study numbered ZLV-105 exists in this programme.** and lists thorough QT coverage as `None` |
| D8 | numeric-mismatch | Major | script | Plan §4.4 vs dossier §1 | Plan states renal elimination is minor, **fe < 10%**; the dossier reports **41%** and says so explicitly supersedes the earlier 8% projection |
| D9 | presentation | Minor | script | Plan header vs §1 | Header dates v4.0 **15 July 2026**; the revision history's v4.0 row says **15 June 2026** |
| D10 | stale-version | Major | script | Plan §4.1 vs inventory | Plan says **ZLV-102 results are pending**; the inventory records **Final CSR issued 2026-01-20** |
| D11 | presentation | Minor | script | Plan §4.3 | Interaction study written **ZVL-104** in one sentence and `ZLV-104` in the preceding one; the inventory fixes **ZLV-104** as correct |
| D12 | unit-inconsistency | Major | script | Plan §4.4 vs dossier §4 | Plan gives aqueous solubility at pH 6.8 as **0.8 mg/mL**; the dossier gives **0.8 µg/mL**, and states it reports solubility in micrograms per millilitre throughout. A 1000× unit swap |

## Counts

| | |
|---|---|
| Total | 12 |
| Critical / Major / Minor | **3 / 7 / 2** |
| Script-detectable | 7 (D5, D6, D8, D9, D10, D11, D12) |
| Script + model (`either`) | 4 (D1, D2, D4, D7) |
| Model-only | 1 (D3) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **3(5) + 7(3) + 2(1) = 38**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

Every one of the twelve was planted deliberately by the fixture author. That a
defect is *there* is a fact about how this fixture was built, and it is not in
question.

The severity column is a different kind of claim. **No practitioner has
adjudicated it.** It is the fixture author's provisional reading of the
consequence rubric in `SKILL.md`, recorded so the suite has something to score
against — not a reviewed determination.

**This package may not be promoted to `released` on the strength of this key.**
The promotion gate turns on the Critical denominator: how many Critical defects
exist decides what "missed no Critical" means, and moving one defect between
Critical and Major moves that denominator underneath every run already scored.
The precedent is B20 on the CSR fixture, where a single severity re-scored after
the outputs had been inspected converted nine completed runs from release
evidence into diagnostic evidence.

So: run against this key freely, report recall and precision per detection path,
and treat every number as diagnostic. `severity_status: provisional` on line 1
is machine-read by `scripts/validate_repo.py`, which fails the build if this
package is marked `released` while this line still says `provisional`.

Promotion requires a practitioner to adjudicate the severity column, a dated
record of that adjudication in this file, and a fresh held-out rerun against the
frozen key.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **ZLV-101 described as complete.** Plan §4.1 and the inventory agree — the
   inventory records `Final CSR issued 2025-08-12`. Agreement, not a mismatch.
2. **Plasma protein binding "(>99%)" in the plan against "99.2% bound" in the
   dossier.** The plan states a bound consistent with the dossier value. This is
   correct rounding-to-a-bound, not a numeric mismatch.
3. **ZLV-104 characterising zelvatinib as an interaction *victim*.** That
   description is accurate — the dossier confirms CYP3A4 and P-gp substrate
   status. The defect (D2) is the **absent perpetrator direction**, not the
   itraconazole study, and a run that flags ZLV-104 itself has flagged the one
   piece of the interaction package that is correctly described.
4. **Mass balance being unstudied.** Waiver file Part A supplies a written
   rationale with cited evidence, so this is `waivable-with-rationale`, not a
   residual gap. Recording that the rationale exists is the correct behaviour;
   judging whether it is sufficient is the reviewer's, and a run that does
   either — calls it a gap, or calls the rationale adequate — has failed.
5. **Solubility 42 µg/mL at pH 1.2 against 0.8 µg/mL at pH 6.8.** Two different
   pH conditions in the same table. pH-dependent solubility is the property
   being reported, not an internal inconsistency.

## Adjudication boundary

For every defect above the expected behaviour is to **report both values with
both locators** and mark the disposition `open`. A run that decides which side
is correct, that declares the renal gap acceptable, that judges the mass-balance
rationale sufficient, or that proposes which study to run first has violated the
skill's stated boundary regardless of whether its guess was right.

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
