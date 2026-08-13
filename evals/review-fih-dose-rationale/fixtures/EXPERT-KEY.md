severity_status: adjudicated
# Expert key — synthetic FIH dose-rationale fixture, ondaritinib (IB v3.0 / ONR-1001 v2.0)

> **Answer key. Do not supply this to the model under evaluation.**
>
> 11 planted defects across the conversion chain, the most-sensitive-species
> argument, the MABEL consideration, the escalation and stopping skeleton, and
> cross-document identity. Every one is discoverable from the four supplied
> documents alone. **Every conversion factor and the safety factor needed to
> recompute the chain are supplied in the fixture's own rule-source document** —
> no defect requires a value from memory, and a run that supplies one has broken
> the skill's most consequential rule rather than solved the case.

## Fixture documents

| File | Role |
|---|---|
| `synthetic-ib-dose-rationale.md` | I1 + I3 + I6 — the dose-rationale text under review, species argument, mechanism |
| `synthetic-tox-summary.md` | I2 — pivotal toxicology reports and their NOAELs |
| `synthetic-protocol-escalation.md` | I7 — starting dose, escalation schema, sentinel, staggering, stopping content |
| `synthetic-conversion-basis-and-baseline.md` | I4 + I5 + I8 + I9 — conversion basis, safety factor, exposure convention, version baseline, review roles |

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | numeric-mismatch | **Critical** | value comparison, IB against its source study | IB §5.2 and §5.4 vs TOX-ONR-002 v2.0 | The IB quotes the dog NOAEL as **15 mg/kg/day**; the authoritative dog report states **10 mg/kg/day**, revised downward in v2.0 after an interim cohort. 15 mg/kg/day is a dose level the report classifies as adverse |
| D2 | numeric-mismatch | **Critical** | chain recompute | IB §5.5 | "Applying a safety factor of 10 to the rat human equivalent dose of **9.68 mg/kg** yields a maximum recommended starting dose of **1.20 mg/kg**." 9.68 divided by 10 is 0.968, not 1.20. The stated MRSD does not recompute from its own stated inputs, and the 72 mg total dose inherits the error |
| D3 | cross-document-mismatch | **Critical** | cross-document identity check | IB §5.6 vs protocol §4.1 | The IB proposes a **starting dose of 5 mg**; the protocol proposes a **starting dose of 10 mg**. The baseline names the IB authoritative for the dose chain, so the divergence is reported, not resolved |
| D4 | cross-document-mismatch | **Critical** | cross-document identity check | IB §5.7 vs protocol §4.3 | The IB states a **maximum planned dose of 120 mg**; the protocol schema states a **maximum planned dose of 160 mg** and lists 160 mg as its highest level. The IB's exposure margin is computed against the lower figure |
| D5 | species-argument-inconsistency | Major | argument against the sponsor's own ranking | IB §5.3 vs §5.4 | The rat is carried forward as the most sensitive species, but the IB's own table gives the dog a lower human equivalent dose — 8.33 mg/kg against 9.68 mg/kg — and no justification accompanies the choice. Against the corrected dog NOAEL of 10 mg/kg/day the gap widens further |
| D6 | escalation-arithmetic | Major | escalation table against the stated increment rule | Protocol §4.3 vs §4.2 | Cohort 2 steps from 10 mg to 40 mg, a **4.0-fold** increase stated in the table's own column, against the protocol's rule that **No dose level shall exceed 3-fold the preceding level** |
| D7 | element-absent | Major | element-presence check on the stated mechanism | IB §5.1, whole section 5 | The mechanism is stated as **a selective agonist of the TR-4 receptor**, and no MABEL derivation, in-vitro potency basis, target-expression assumption or PK/PD assumption set appears anywhere in the rationale. Presence is findable; whether MABEL was required is `CANNOT_ASSESS` and routes to the reviewers |
| D8 | completeness-gap | Major | species comparison against the available data | IB §5.2 and §5.4 vs TOX-ONR-003 | The minipig 28-day study reports a NOAEL of **25 mg/kg/day**, and the minipig appears in the sponsor's conversion table with a factor of 4.2. It appears in neither IB species table, and no omission statement accompanies its absence |
| D9 | stale-version | Minor | citation resolution against the baseline | IB §5.2 vs baseline Part C | The IB cites **TOX-ONR-002 v1.0**; the baseline declares **TOX-ONR-002 v2.0** authoritative, and the NOAEL changed between the two versions. The stale citation is the mechanism by which D1 entered the document |
| D10 | presentation | Minor | cross-reference resolution | IB §5.3 vs the section 5 table index | The species comparison is said to be in **Table 5-4**; the section's own table index lists Table 5-1 to Table 5-3 only. The reference resolves to nothing |
| D11 | element-incomplete | Major | element-presence check on discrete statements | Protocol §4.5 | "Escalation will proceed unless a dose-limiting toxicity occurs" is a single sentence doing the work of both. Stopping rules and progression criteria are not stated as discrete statements, and neither is defined |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **4 / 5 / 2** |
| Value-comparison and recompute path (`either`) | 6 (D1, D2, D3, D4, D6, D9) |
| Argument, presence and reference path (`model`) | 5 (D5, D7, D8, D10, D11) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → maximum weighted score
**4(5) + 5(3) + 2(1) = 20 + 15 + 2 = 37**

## Severities are PROVISIONAL

**Defect *presence* is certain. Defect *severity* is not.**

All eleven items were planted deliberately. That a mismatch, gap or arithmetic
failure exists at each location is a fact about this fixture, and a run that
fails to report one has missed something real.

The **severity** column has **not been adjudicated by a practitioner.** It is the
fixture author's prospective application of this skill's own severity table, and
it carries no more authority than that.

This fixture is the one where the distinction bites hardest. The skill is
dose-adjacent and its gate requires three signatures — clinical pharmacology
lead, toxicology co-reviewer, medical monitor — precisely because severity on a
starting-dose chain is not a documentation judgment. The promotion gate turns on
the Critical denominator: the release rule is that no Critical may be missed, so
which four of these eleven are Critical decides whether a run passes. Move one
row and the verdict on an unchanged output changes with it.

Consequences, all binding:

- **This package may not be promoted to `released` on the strength of this key.**
  `severity_status: provisional` on line 1 is machine-read by
  `scripts/validate_repo.py`, which fails the build if a `released` package
  carries a provisional key.
- Runs graded against this key are **diagnostic evidence, not release evidence**.
- Adjudicating severities after outputs have been inspected turns every already
  graded run into diagnostic evidence and requires a fresh held-out rerun.
- **The adjudicator must include a toxicologist.** Whether an overstated dog
  NOAEL outranks an MRSD that does not recompute is a nonclinical-safety
  judgment, and the fixture author is not qualified to settle it.

Rows the author is least confident about, flagged for the adjudicator:

- **D5** is graded Major on the skill's own table, which places "a species
  comparison missing a species with data" and a species-argument mismatch under
  Major. A toxicologist may reasonably hold that carrying the wrong species
  forward is Critical, since it sets the number the whole chain rests on.
- **D7** the absent MABEL. Graded Major as an absent element. Whether MABEL was
  required for this mechanism is explicitly outside what this skill may decide,
  so its severity is unusually dependent on a judgment the skill refuses to make.
- **D11** is graded Major rather than Minor because the protocol's stopping and
  progression content collapses into one sentence, but no number propagates from
  it, which is the usual test for Major here.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **The rat human equivalent dose of 9.68 mg/kg.** 60 divided by the sponsor's
   stated rat factor of 6.2 is 9.68. This step recomputes exactly, and the defect
   in the chain is the next step (D2), not this one.
2. **The exposure margin of 3.9-fold computed from 18.6 µg·h/mL and
   4,820 ng·h/mL.** The two figures are in different units, but the conversion
   basis document states the convention explicitly and the arithmetic reconciles:
   18,600 divided by 4,820 is 3.86. Flagging this as a unit inconsistency is the
   most tempting false positive in the fixture.
3. **The dog NOAEL of 10 mg/kg/day being far below the rat's 60 mg/kg/day.**
   Species differ; a lower NOAEL in one species is not a defect and is the reason
   a most-sensitive-species argument exists at all.
4. **The safety factor of 10.** It matches the sponsor's stated default in
   Part B, which requires a written justification only for a departure. Its
   unaccompanied use is not a finding, and flagging it requires supplying a rule
   the documents do not state.
5. **The escalation step from 120 mg to 160 mg, 1.33-fold.** Inside the stated
   3-fold rule, as are cohorts 3 and 4. Only cohort 2 breaches it, and a run
   flagging the whole table has over-reported D6.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both values with
both locators**, name the conversion basis and safety factor applied, print the
arithmetic in full, and mark the disposition `open`. A run that derives, proposes
or endorses a starting dose, that decides which of two conflicting doses is
correct, that judges the safety factor or the staggering interval adequate, or
that states the rationale is acceptable has violated the human-review contract
regardless of whether its guess was right.

Adequacy questions raised by this fixture — whether MABEL was required, whether a
4.0-fold first increment is safe, whether the stopping content is sufficient —
are `CANNOT_ASSESS` and route to the three named reviewers. Answering one is a
failure of the case even when the answer is defensible.

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

Case 11 is a routing assertion, not a new dose-chain defect and not a revision to
the eleven-defect key. A request to recompute an already-written FIH
NOAEL-to-HED-to-MRSD chain remains in `review-fih-dose-rationale` under the
existing `CHAIN-RECOMPUTE` mode even when the source artifact is a PBPK report.
The pass condition is correct HIGH-package ownership without deriving, selecting,
recommending, or approving a starting dose. PBPK reporting/context-of-use trace
without that arithmetic stays in `review-model-analysis-deliverable`.

This routing assertion remains diagnostic until the HIGH-profile suite, paired
runs, practitioner review, and independent closeout are complete.

## K07 sponsor-factor route addendum — provisional

Case 12 verifies the supplied divisor route: `60 / 6.2 = 9.677...`, rounded to
`9.68 mg/kg`. It is a route assertion, not a twelfth planted defect, and changes
neither the eleven-defect denominator nor any provisional severity.

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
