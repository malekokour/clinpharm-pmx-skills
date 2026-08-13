severity_status: adjudicated
# Expert key — synthetic information-request fixture IR-2026-0417 (veltarozan, VTZ-330)

> **Answer key. Do not supply this to the model under evaluation.**
>
> Eleven planted defects across decomposition, evidence mapping, citation
> tracing and version baselining. Every one is discoverable from the four
> supplied documents alone. No turnaround norm, no guidance date, and no
> external staging rule is needed to find any of them.

## The documents

| File | Plays the part of |
|---|---|
| `synthetic-information-request.md` | I1 the request as received, I2 request metadata |
| `synthetic-submission-baseline-and-history.md` | I7 submission version baseline, I3 prior correspondence, I6 owner roster |
| `synthetic-evidence-sources.md` | I4 submitted documents, I5 source outputs |
| `synthetic-draft-response.md` | I8 draft response — the object of the claim-to-citation trace |

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | stale-version | **Critical** | either | Draft Q1 vs baseline Part A | Draft cites **Module 2.7.2 v3.0**. The baseline states **The version of Module 2.7.2 held by the authority is v2.0.** The response answers against a document the authority has never seen |
| D2 | numeric-mismatch | **Critical** | script | Draft Q2 vs popPK Part B / Table 14.2.5 | Draft states AUC0–24,ss of **1240 ng·h/mL**; both sources say **1420 ng·h/mL**. Transposed digits, 13% apart |
| D3 | numeric-mismatch | **Critical** | script | Draft header vs request metadata | Draft header carries **Response due: 2026-10-18**; the request itself states **Response due: 2026-09-18**. A response date the request does not give |
| D4 | unsupported-claim | Major | model | Draft Q3 vs request Question 3 | Question 3 asks **Please confirm whether the applicant intends to conduct a dedicated hepatic impairment study.** The draft answers with a commitment: **The sponsor will conduct a dedicated hepatic impairment study and submit the report by Q3 2027.** A `commitment-sought` unit answered with an undertaking no named human approved |
| D5 | completeness-gap | **Critical** | either | Draft header vs request | Draft contents read **Responses to Questions 1–4**. The request carries five, and **Question 5** has no response section anywhere in the draft |
| D6 | unresolvable-citation | Major | script | Draft Q2 vs CSR section map | Draft cites **Table 14.2.6**. The CSR states **The highest numbered pharmacokinetic table in the VTZ-201 CSR is Table 14.2.5.** The citation does not resolve |
| D7 | locator-mismatch | Major | script | Draft Q4 vs CSR section map | Draft cites **Section 12.3** for the exposure–response exclusion. §12.3 is *Distribution and elimination*; the exclusion is in §12.7, and the renal subgroup is in **§12.6 Renal function subgroup**. The citation resolves to the wrong section |
| D8 | contradiction | Major | script | Draft Q1 vs prior correspondence and popPK | Draft states clearance **22.4 L/h**. Both the prior sent response and the population pharmacokinetic report say **18.6 L/h**, and the report records no revision. A value changed without the change being declared |
| D9 | unit-inconsistency | Major | script | Draft Q2 vs Table 14.2.5 | Draft gives peak concentration as **612 µg/mL**; the source table says **612 ng/mL**. A 1000× unit swap on a value going to an authority |
| D10 | presentation | Minor | script | Draft title | Draft titles the compound **VTZ-300**; every other document says **VTZ-330** |
| D11 | presentation | Minor | script | Draft header vs request metadata | Draft header gives procedure identifier **IR-2026-0471**; the request says **IR-2026-0417**. Transposed |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **4 / 5 / 2** |
| Script-detectable | 8 (D2, D3, D6, D7, D8, D9, D10, D11) |
| Script + model (`either`) | 2 (D1, D5) |
| Model-only | 1 (D4) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **4(5) + 5(3) + 2(1) = 37**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

All eleven were planted deliberately. That each is present is a fact about how
this fixture was authored, and it is not open to disagreement.

The severity column is a different claim entirely, and **no practitioner has
adjudicated it.** It is the fixture author's provisional reading, recorded so
the suite has something to score against.

**This package may not be promoted to `released` on the strength of this key.**
The promotion gate turns on the Critical denominator — "missed no Critical"
means nothing until the count of Criticals is settled — and moving a single
defect between Critical and Major moves that denominator underneath every run
already scored against it. That is not hypothetical: on the CSR fixture, one
severity re-scored after outputs had been inspected converted nine completed
runs from release evidence into diagnostic evidence.

`severity_status: provisional` on line 1 is machine-read by
`scripts/validate_repo.py`, which fails the build if this package is marked
`released` while that line still reads `provisional`. Promotion needs a
practitioner adjudication, dated and recorded here, and a fresh held-out rerun
against the frozen key.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **Question 4 carrying three asks in one sentence.** That is the
   decomposition target, not a defect in the request. The correct behaviour is
   to split it into `Q4(a)`, `Q4(b)`, `Q4(c)` with the wording preserved
   verbatim. Reporting the request itself as defective is a fail.
2. **The prior response's 18.6 L/h.** That value is correct and matches the
   population pharmacokinetic report. A run that flags the prior response has
   picked the wrong side of D8.
3. **AUC 1420 ng·h/mL against 980 ng·h/mL.** Moderate renal impairment against
   normal renal function — two populations, not a mismatch. Question 5 asks for
   exactly this comparison.
4. **The existence of an internal Module 2.7.2 v3.0.** The baseline records it
   openly. Holding a newer internal revision is normal; the defect (D1) is
   *citing* it as though the authority held it.
5. **The body-mass-index exclusion being pre-specified.** The CSR states the
   exclusion is pre-specified in `VTZ-ER-SAP v1.0 §5.4`, and the draft says the
   same. The defect in that paragraph is the citation (D7), not the
   pre-specification claim.

## Adjudication boundary

Every defect is reported with **both values and both locators**, disposition
`open`. A run that decides which clearance value is correct, that states the
response is complete, that supplies a response deadline the request does not
state, or that lets the draft's commitment sentence stand as an answer has
violated the skill's boundary regardless of whether its numbers were right.

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
