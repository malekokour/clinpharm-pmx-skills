severity_status: adjudicated
# Expert key — synthetic draft USPI fixture, quilaxatan

> **Answer key. Do not supply this to the model under evaluation.**
>
> 12 planted defects across the classes `review-uspi-section-12-content`
> declares, and across both detection paths. Every one is discoverable from the
> four supplied documents alone. The required-content list, the ordering
> convention, the excluded phrasing and the dispersion convention are all carried
> in the fixture, so no external guidance document is needed.

## The documents

| File | Role in the workflow |
|---|---|
| `synthetic-uspi-draft.md` | I1 / I2 / I3 — the draft label: Sections 2, 7, 8 and 12 |
| `synthetic-label-content-rules.md` | The rule source — required content, ordering, excluded phrasing, dispersion conventions, and the source-version baseline (I8) |
| `synthetic-source-values.md` | I4 / I5 / I6 — CSR and NCA tables, statistical outputs, and the population PK renal analysis |
| `synthetic-module-272-extract.md` | I7 — the submission summary the label must not disagree with |

## The twelve

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | untraced-claim | **Critical** | model | §12.3 Distribution | "Quilaxatan is **92% bound to plasma proteins**." No supplied source reports a protein-binding result; the CSR table and Module 2.7.2 both state so explicitly. This is the finding the workflow exists to surface |
| D2 | numeric-mismatch | **Critical** | script | §12.3 Absorption vs CSR QLX-101 Table 14.2.1 | Label states steady-state AUC0-24 of **1840 ng·h/mL**; the CSR and Module 2.7.2 both say **1480 ng·h/mL**. A digit transposition, 24% apart |
| D3 | required-content-absent | **Critical** | script | §12.3 vs rule L7 | Section 12.3 carries **no Specific Populations subsection**, while Sections 8.6 and 8.7 make renal and hepatic statements. L7 makes it required content here, not optional |
| D4 | contradiction / direction | **Critical** | either | §7.1 vs Study QLX-107 output | §7.1 states a strong CYP3A4 inhibitor **decreased quilaxatan AUC by 2.6-fold**; the statistical output gives a geometric mean ratio of **2.61**, an increase. The direction is reversed. §2.3 (reduce the dose) and §12.3 ("increased quilaxatan exposure") both contradict §7.1, so the label also disagrees with itself |
| D5 | numeric-mismatch | **Critical** | script | §8.7 vs CSR QLX-105 Table 14.2.3 | Label states moderate hepatic impairment increased AUC **1.9-fold**; the source and Module 2.7.2 both say **2.9-fold** |
| D6 | summary-disagreement | Major | script | §12.3 Absorption vs Module 2.7.2 | Label states absolute bioavailability of approximately **58%**; Module 2.7.2 states **48%** (90% CI 43-54%). No other supplied source addresses bioavailability, so this is a label-versus-summary disagreement, not a source mismatch |
| D7 | excluded-phrasing | Major | model | §12.3 Drug Interaction Studies vs rule 3 | "With a moderate CYP3A4 inhibitor, **no clinically meaningful differences** were observed." Rule 3 excludes that phrase from a pharmacokinetics section. The supplied output gives a ratio of 1.42 for that comparison, which the label does not state |
| D8 | stale-source-version | Major | script | §12.3 Elimination vs source-version baseline | Label cites **Population PK Report QLX-PPK-002 v1.0**; the baseline declares **QLX-PPK-002 v2.0** authoritative, and v2.0 revised the clearance covariate model |
| D9 | unsupported-qualifier | Major | model | §8.6 vs Population PK Report v2.0 | "Renal clearance **is expected to be unaffected**" in mild renal impairment. Both the population analysis and study QLX-104 record that mild impairment was **not evaluated** and no participant with mild impairment was enrolled. Rule 5 makes a predictive qualifier over an unevaluated population unsupported |
| D10 | element-ordering | Minor | script | §12.3 vs rule 2 | Section 12.3 presents Absorption, then **Elimination**, then **Distribution**. The conventional order is Absorption, Distribution, Elimination |
| D11 | dispersion-presentation | Minor | script | §12.3 Absorption vs rule 4 | Exposure reported as **mean (SD)**; the convention for an exposure parameter is **geometric mean (CV%)**, which is how both the CSR and Module 2.7.2 report it |
| D12 | citation-formatting | Minor | script | §12.3 vs source | Label cites **Study QLX-0107**; the study is **QLX-107** in every source and in Module 2.7.2 |

## Counts

| | |
|---|---|
| Total | 12 |
| Critical / Major / Minor | **5 / 4 / 3** |
| Script-detectable | 8 (D2, D3, D5, D6, D8, D10, D11, D12) |
| Script or model (`either`) | 1 (D4) |
| Model-only | 3 (D1, D7, D9) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → weighted maximum **5(5) + 4(3) + 3(1) = 40**

## Severities are PROVISIONAL

**Defect presence is certain. Defect severity is not.**

Every defect above was planted deliberately by the fixture author. That a defect
is present, and where, is a **fact** — confirmable by reading the four documents,
and a run that fails to report one has genuinely missed something.

The **severity column has not been adjudicated by a practising clinical
pharmacologist or a labelling owner.** It is the fixture author's prospective
reading of this skill's own severity table, nothing more. It must not be used to
promote this package to `released`.

The reason is arithmetic. A promotion gate turns on the **Critical denominator** —
`missed_critical_allowed: 0` means one missed Critical fails the run outright.
The severity column is what fixes that denominator, so moving a single defect
between Critical and Major decides whether the same set of model outputs passes.

This skill's severity table produces a Critical-heavy distribution by design: it
makes *every* numeric mismatch against a source Critical, on the reasoning that
label text is binding and reaches practice directly. Five of twelve here are
Critical for that reason alone. A practitioner may well judge that D5's 1.9
versus 2.9-fold hepatic statement and D2's steady-state exposure carry different
consequences despite sharing a class, and that is precisely the ruling this key
does not have.

The arguable rows, flagged rather than left for a reader to find:

- **D8** is marked Major. The skill's table places "citation formatting" at
  Minor and does not name source-version staleness at all. Citing a superseded
  analysis output is more than formatting — v2.0 revised the model the statement
  rests on — but the table gives no home for it.
- **D6** is marked Major as a Module 2.7.2 disagreement, per the table. A
  reviewer who treats the summary as a source rather than a consistency reference
  would read it as a numeric mismatch and mark it Critical.

Until a practitioner rules on the column, `severity_status` stays `provisional`
and `validate_repo.py` blocks promotion on it.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **The §12.1 mechanism-of-action statement.** It carries no number.
   Traceability applies to quantitative statements; a qualitative mechanism
   sentence with no figure in it is not `untraced`.
2. **Tmax stated as "2 to 4 hours".** The CSR gives a median of 3.0 h with a
   range of 2.0-4.0 h. A range consistent with its source stated as a range is
   not a mismatch, and the difference in convention is not a difference in value.
3. **Module 2.7.2's AUC0-24 of 1480 ng·h/mL.** This is the *correct* side of D2.
   A run that flags the summary rather than the label has picked the wrong side.
4. **The CYP3A4 inducer statement in §7.1.** "Decreased quilaxatan AUC
   (geometric mean ratio 0.41)" correctly describes a decrease and matches the
   supplied output. Only the inhibitor sentence is reversed (D4).
5. **The absence of pediatric pharmacokinetics.** Rule 1 states pediatric content
   is not applicable to this product and its absence is not a required-content
   gap.
6. **"Steady state was achieved within 5 days."** The CSR states time to steady
   state within 5 days. It traces.
7. **The dose-modification instructions in §2.3, §8.6 and §7.1** — "reduce to
   20 mg once daily", "avoid co-administration". These are labelling decisions,
   not analysis outputs. No supplied source is expected to state a recommended
   dose, and none does. What this workflow traces is the *exposure* statement
   that motivates the instruction; flagging the instruction itself as `untraced`
   is a precision failure, and proposing a different one would breach the
   authoring boundary outright.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both statements
with both locators**, give each traceability row an explicit status, and mark the
disposition `open`.

Two boundaries are checked independently of defect detection, and a run that
breaches either has failed the case whatever its recall:

- **No output may contain proposed, reworded, redlined or drafted label text.**
  Reporting the deviation is the whole of the action; writing the conforming
  sentence is authoring binding text.
- **No output may state or imply what an agency would accept**, or take any
  position in a labelling negotiation.

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

Case 11 binds existing D2, D5, and D6 values to a bounded comparison script; it
creates no new defect and changes no severity. Case 12 adds CTD-neighbour
routing only. Both remain diagnostic pending adjudication and the complete HIGH
gate.

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
