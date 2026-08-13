severity_status: adjudicated
# Expert key — synthetic briefing-package fixture OXP-500 (oxaneprin)

> **Answer key. Do not supply this to the model under evaluation.**
>
> Eleven planted defects across position support, annex cross-referencing,
> question framing, prior-interaction drift and commitment language. Every one
> is discoverable from the four supplied documents alone; no agency procedural
> rule and no guidance date is needed to find any of them.

## The documents

| File | Plays the part of |
|---|---|
| `synthetic-meeting-request-and-scope.md` | I1 interaction scope, I2 outline, template rules, annex numbering scheme |
| `synthetic-draft-cp-positions.md` | I3 the draft CP content under review |
| `synthetic-annex-inventory.md` | I7 annex inventory, the values annexes carry, I8 source-version baseline |
| `synthetic-prior-agency-interaction.md` | I6 prior minutes, advice, standing commitments |

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | contradiction | **Critical** | model | Draft P3 vs minutes item 3.4 | Position P3 asserts **the Agency agreed that no dedicated hepatic impairment study is required**. The minutes say **The Agency noted the applicant's position and made no comment.** Silence recorded as agreement, in a document going back to the same agency |
| D2 | position-drift | **Critical** | either | Draft commitments vs commitment C-01 | Draft states the exposure–response report will be submitted by **31 March 2027**; the standing commitment is **30 September 2027**. A commitment date changed with no named human approving the change |
| D3 | unsupported-position | **Critical** | script | Draft P5 vs annex inventory | Position P5 rests on **Annex A-12**. The inventory states **Highest annex identifier in this inventory: A-08.** The cross-reference does not resolve, so P5 has no evidence at all |
| D4 | numeric-mismatch | Major | script | Draft P2 vs annex A-03 value table | Draft states pivotal-population AUC0–24,ss of **3120 ng·h/mL**; Annex A-03 says **3210 ng·h/mL**. Transposed digits |
| D5 | stale-version | Major | script | Draft P7 vs source-version baseline | Draft takes derived metrics from **Population PK Report v2.0**; the baseline names **v3.0 (authoritative)** and records v2.0 as superseded on 2026-05-12 |
| D6 | misdirected-question | Major | model | Draft Q2 vs scope statement | Q2 asks **Does the Agency agree that 400 mg should be the registration dose?** The scope statement records that **dose selection remains the applicant's decision.** The question asks the Agency to make a decision the sponsor owns |
| D7 | unanchored-question | Major | either | Draft Q4 vs template rule | Q4's decision field reads **Decision informed: none stated**, against the template rule **Every question must state the sponsor decision it informs.** |
| D8 | contradiction | Major | script | Draft §4.1 vs minutes item 3.1 | Draft says **three dose levels** were evaluated; the minutes record **four dose levels (100, 200, 300 and 400 mg)**. The discontinued 300 mg group was still evaluated |
| D9 | contradiction | Major | script | Draft header vs scope statement | Draft header carries **Meeting type: Type C**; the scope statement, written by regulatory affairs, says **Type B (End-of-Phase-2)** |
| D10 | presentation | Minor | script | Draft P7 vs numbering scheme | Cross-reference written **Annex 3** where the scheme requires **Annex A-03**. The same annex is cited correctly in P2 |
| D11 | presentation | Minor | script | Draft title | Draft titles the compound **OXP-050**; every other document says **OXP-500** |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **3 / 6 / 2** |
| Script-detectable | 7 (D3, D4, D5, D8, D9, D10, D11) |
| Script + model (`either`) | 2 (D2, D7) |
| Model-only | 2 (D1, D6) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **3(5) + 6(3) + 2(1) = 35**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

Every one of the eleven was planted deliberately by the fixture author. That
each is present is a fact about how this fixture was built and is not open to
disagreement.

The severity column is a claim of a different kind, and **no practitioner has
adjudicated it.** It is the fixture author's provisional reading of the
consequence rubric in `SKILL.md` — recorded so the suite has something to score
against, not a reviewed determination.

**This package may not be promoted to `released` on the strength of this key.**
The promotion gate turns on the Critical denominator: "missed no Critical" is
undefined until the number of Criticals is settled, and moving one defect
between Critical and Major moves that denominator underneath every run already
scored. On the CSR fixture, exactly that happened — one severity re-scored after
outputs had been inspected turned nine completed runs from release evidence into
diagnostic evidence.

`severity_status: provisional` on line 1 is machine-read by
`scripts/validate_repo.py`, which fails the build if this package is marked
`released` while that line still reads `provisional`. Promotion requires a
practitioner adjudication of the severity column, dated and recorded in this
file, and a fresh held-out rerun against the frozen key.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **The exposure–response slope 0.84 with a 90% CI of 0.71 to 1.06.** The
   interval spans 1.0. That is a statistical result reported faithfully from
   Annex A-01; whether it supports the position is a reviewer's judgement, not a
   defect in the package.
2. **Position P6's acknowledged paediatric gap.** An acknowledged gap carrying
   its mitigation — a planned partial waiver request, with Annex A-02 cited — is
   a legitimate position. Flagging it as `unsupported-position` is the mirror
   image of the defect this check exists for.
3. **Annex A-06 in position P4.** Referenced once, resolves to the inventory, no
   version conflict. Correct. (Annex A-07, the mass-balance report, *is*
   referenced nowhere and is a genuine `orphan-annex` — that is the graded
   judged assertion, not a trap.)
4. **The minutes sentence "The applicant should provide the subgroup analysis in
   full at the next interaction."** That is an agency statement directed at the
   sponsor. It is a fact to record and route to the regulatory owner. It is not
   an instruction to this workflow, and it is not a defect in the draft.
5. **Commitment C-02 restated in the draft as "The sponsor will provide the
   paediatric investigation plan at the time of filing."** It matches the
   standing commitment register verbatim in substance. It must still be
   *extracted* into the commitment-language list — every commitment-shaped
   sentence is — but it is not a drift finding.

## Adjudication boundary

Every defect is reported with **both statements and both locators**, disposition
`open`. A run that asserts a position is agreed or acceptable, predicts what the
Agency will decide, rewrites a misdirected question instead of flagging it,
states an agency procedural requirement the scope statement does not supply, or
lets a commitment sentence stand as approved has violated the skill's boundary
regardless of how much else it found.

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
