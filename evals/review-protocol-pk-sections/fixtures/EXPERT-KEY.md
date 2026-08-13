severity_status: adjudicated
# Expert key — synthetic protocol fixture CVS-101

> **Answer key. Do not supply this to the model under evaluation.**
>
> 11 planted defects across the classes `review-protocol-pk-sections` declares,
> and across all three detection paths. Every one is discoverable from the four
> supplied documents alone; none requires outside knowledge, and none requires a
> guidance document that is not in the fixture set.

## The documents

| File | Role in the workflow |
|---|---|
| `synthetic-protocol.md` | I1 — the object under review (Protocol v2.0), with §9.6 as the embedded analysis plan (I5) |
| `synthetic-ib-extract.md` | I3 — Investigator's Brochure Edition 4.0; also carries the dose-derivation table that I4 would supply |
| `synthetic-sponsor-conventions.md` | I7 — the **rule source**: required elements, window and coverage conventions, units, precision, and the version baseline |
| `synthetic-bioanalytical-summary.md` | I6 — method identifier, validated range and LLOQ |

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | design-inconsistency | **Critical** | script | §9.4.2 vs IB §5.2 | The 24 h sampling duration is justified by a terminal half-life of **6.2 h**; the authoritative IB Edition 4.0 reports **18.6 h**. At 18.6 h the schedule covers 1.3 half-lives, not the three the conventions require, and terminal half-life is a pre-specified endpoint |
| D2 | completeness-gap | **Critical** | model | §9.6 vs convention R9 | §9.6 names the parameters but **never defines a PK analysis population** — which participants and which profiles contribute to each summary. R9 requires it |
| D3 | unit-inconsistency | Major | script | §9.5 vs bioanalytical summary | Protocol states the LLOQ as **0.25 µg/mL**; the validated method summary states **0.25 ng/mL**. A 1000-fold unit swap in the protocol text |
| D4 | internal-contradiction | Major | script | Synopsis vs Schedule of Assessments | Synopsis says PK profiles on **Days 1 and 14**; the Schedule of Assessments shows **Days 1, 7 and 14** |
| D5 | untraceable-rationale | Major | either | §6.1 vs IB §5.4 | Cohort 4 is dosed at **600 mg**. The IB records derivations for 50, 150 and 300 mg only, and states no derivation above 300 mg. Convention 5 makes this `untraceable-rationale` |
| D6 | stale-version | Major | script | §9.5 vs version baseline | Protocol cites **Investigator's Brochure Edition 3.0**; the declared authoritative version is **Edition 4.0**, and Edition 4.0 explicitly supersedes the Edition 3.0 half-life |
| D7 | completeness-gap | Major | model | §9.6 vs convention R10 | No **BLQ handling convention** appears anywhere in §9.6 — neither before nor after the first quantifiable concentration. R10 requires it, and §9.6 does not declare it deferred |
| D8 | window-convention | Major | script | §9.4.1 vs convention 2 | The 4 h sample carries a **±55 min** window. The nearest adjacent nominal time is 3 h, 60 min away, so the convention permits at most **±30 min**; as written the 4 h and 3 h windows overlap |
| D9 | restriction-gap | **Critical** | model | §5.4 vs convention R7 | §5.4 restricts alcohol, caffeine, grapefruit and exercise but specifies **no standardised meal requirement**, in a study whose endpoints include Cmax. R7 requires it and the IB §5.6 recommends it. Not correctable once the study runs |
| D10 | precision | Minor | script | §9.6 vs convention 4 | §9.6 reports values to **two significant figures**; the convention is **three significant figures** |
| D11 | citation-hygiene | Minor | script | §9.5 vs bioanalytical summary | Protocol cites method **BA-M-0142**; the validated method is **BA-M-0412** — a digit transposition |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **3 / 6 / 2** |
| Script-detectable | 7 (D1, D3, D4, D6, D8, D10, D11) |
| Script or model (`either`) | 1 (D5) |
| Model-only | 3 (D2, D7, D9) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **3(5) + 6(3) + 2(1) = 35**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

Every defect above was planted deliberately by the fixture author. That a defect
is present, and where, is a **fact** — it can be confirmed by reading the four
documents, and a run that fails to report one has genuinely missed something.

The **severity column has not been adjudicated by a practising clinical
pharmacologist.** It is the fixture author's prospective reading of this skill's
own severity table, nothing more. It must not be used to promote this package to
`released`.

This matters because of arithmetic, not ceremony. The promotion gate turns on the
**Critical denominator** — `missed_critical_allowed: 0` means a single missed
Critical fails the run outright. That denominator is exactly what the severity
column fixes. Move one defect between Critical and Major and the same set of
model outputs passes or fails. A gate whose pass condition is set by an
unadjudicated judgement is not a gate.

Two rows are known to be genuinely arguable and are flagged here rather than left
for a reader to discover:

- **D3** is marked Major on the reasoning that the assay is validated at
  0.25 ng/mL regardless of what the protocol says, so the data remain analysable
  and an amendment fixes it. A reviewer who reads a 1000-fold unit error in a
  protocol as irreversible-by-propagation would mark it Critical.
- **D9** is marked Critical on the reasoning that meal conditions cannot be
  reconstructed after the samples are drawn. A reviewer who treats meal
  standardisation as site-procedure detail rather than protocol content would
  mark it Major.

Until a practitioner rules on the column, `severity_status` stays `provisional`
and `validate_repo.py` blocks promotion on it.

## K05 extension diagnostics — CPS-204, VUL-101, and PDM-301

These extension cases are also **diagnostic only**. Their mismatches and
structural states are planted facts; their severities are provisional and do not
qualify the package.

### Case 11 — `CONSENT-CONSISTENCY`

| ID | Provisional severity | Location | Planted mechanical mismatch |
|---|---|---|---|
| CC1 | Major | Consent research-blood section vs protocol §8.2/sample manual | `Day 1 only` versus `Days 1 and 8` |
| CC2 | Major | Consent optional-genomic section vs protocol §8.3/sample manual | `4 mL` versus `6 mL` |
| CC3 | Major | Consent optional-genomic section vs protocol §8.3/sample manual | `5 years` versus `15 years` |
| CC4 | Major | Current supplied consent vs approval-register row AR-07 | `Consent Form v2.0` versus `Consent Form v1.0` |

CC4 does **not** prove that v2.0 lacks approval. The supplied register does not
resolve whether another record exists, so approval state remains `UNKNOWN` /
`NEEDS_INPUT`. The case never judges adequacy, voluntariness, understanding,
burden, or re-consent.

### Case 12 — vulnerable-population structural register

The owner declares two population rows. Five artifact fields per row produce the
fixed denominator **10**. Expected tool result: **8 `PRESENT`, 1 `MISSING`, 1
`UNKNOWN`, 10/10 `HUMAN_REVIEW`, and every disposition `UNSET`**.

- POP-01 `compensation` is explicitly `null` → `MISSING`.
- POP-02 omits `specialist_input` → `UNKNOWN`; the manifest does not say whether
  it was assessed.

The clean control declares one synthetic population with all **5/5** locators
present. Neither fixture authorizes a vulnerability, capacity, coercion,
safeguard, or risk-benefit judgment.

### Case 13 — PD/biomarker context

| ID | Provisional severity | Location | Planted mechanical mismatch |
|---|---|---|---|
| PD1 | Major | Protocol §10.2 vs SAP §6.3 | `20%` versus `25%` |

The one declared measure, BMR-7, must carry an **8/8-field denominator**. The
protocol explicitly states qualification-route status `UNKNOWN`. The model must
not choose either decision rule and must not judge biological plausibility,
qualification sufficiency, clinical meaningfulness, surrogate validity, or any
dose implication.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **The deferred population PK modelling strategy (§9.6).** The protocol states
   the deferral explicitly and names the downstream document. Convention 1 says
   an explicitly deferred element is recorded as deferred, and the skill's own
   rule is that "not yet written" and "deliberately deferred" are different
   results. Flagging it as a `completeness-gap` is wrong; `UNKNOWN` is also wrong
   here, because the protocol *does* say which it is.
2. **Sampling density around Tmax.** The IB reports median Tmax 3.0 h and the
   schedule samples at 2, 3 and 4 h. Density around the peak is adequate against
   the supplied documents; the defect is the terminal tail (D1), not the peak.
3. **The ±5 min windows at 0.5 h and 1 h.** They look conspicuously tight, but
   the adjacent interval is 30 min, so the convention permits up to ±15 min.
   ±5 min conforms.
4. **Dose levels 50, 150 and 300 mg.** All three trace to a stated derivation
   with an exposure margin in IB §5.4. Only the 600 mg level is untraceable
   (D5); flagging the traceable three is a precision failure.
5. **The 24 h LLOQ headroom.** The bioanalytical summary states 24 h
   concentrations of 3.1-8.4 ng/mL at 50 mg against a 0.25 ng/mL LLOQ. The last
   nominal sample is expected to be quantifiable, so "the last sample may fall
   below LLOQ" is not a finding on this fixture.
6. **The IB's Edition 3.0 half-life.** The IB itself explains that the Edition
   3.0 estimate was preliminary and superseded. The defect is that the *protocol*
   cites the superseded edition (D6), not that the IB mentions it.
7. **"AUC0-tau" in §3.1 against "AUC0-24" in §9.6.** The regimen is once daily,
   so tau is 24 h and the two names denote the same quantity. A naming
   difference that resolves to one quantity is not an inconsistency, and the
   conventions file states no naming rule for it.
8. **The stopping rules in §6.1.** They are present and they reference the
   Investigator's Brochure exposure cap. Whether the cap is the right one is a
   scientific judgment this skill does not make; the conformance check is that
   R2's stopping rules exist and are locatable, and they do.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both statements
with both locators**, name the convention applied and where it is written, and
mark the disposition `open`. A run that states which value is correct, that
declares the sampling schedule adequate or inadequate, or that proposes a dose
level has violated the skill's contract regardless of whether its guess was
right.

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
