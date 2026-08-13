severity_status: adjudicated
# Expert key — synthetic DDI evidence fixture, veltrapib

> **Answer key. Do not supply this to the model under evaluation.**
>
> 11 planted defects across role assignment, the study-trigger decision tree,
> numeric reconciliation, magnitude banding, provenance, wording consistency and
> citation hygiene. Every one is discoverable from the four supplied documents
> alone. **Every cutoff and band needed to find them is supplied in the fixture's
> own threshold extract** — no defect here requires a threshold from memory, and
> a run that supplies one has broken the skill's rule rather than solved the case.

## Fixture documents

| File | Role |
|---|---|
| `synthetic-invitro-ddi-report.md` | I1 + I2 — enzyme and transporter in-vitro results, IV-DDI-VLT-003 v2.0 |
| `synthetic-clinical-ddi-studies.md` | I3 + I4 — clinical studies VLT-1005, VLT-1006 and the PBPK substitution report |
| `synthetic-ddi-summary-section.md` | The package under review, plus CSR wording and the draft label extract (I6) |
| `synthetic-thresholds-adme-and-baseline.md` | I9 + I5 + I10 — thresholds and bands, fraction metabolised by pathway, version baseline, owner |

## The eleven

| ID | Class | Severity | Detection path | Location | Description |
|---|---|---|---|---|---|
| D1 | direction-contradiction | **Critical** | direction stated against the ratio reported | Summary A.2 vs VLT-1005 Table 3.1 | The summary states cyprazole **reduced veltrapib exposure**; VLT-1005 reports an AUC geometric mean ratio of **4.62** (90% CI 3.98–5.36) and states exposure was higher. Direction reversed, and a dose-reduction instruction is proposed on the reversed reading |
| D2 | decision-open | **Critical** | decision-tree walk with the transcribed R2 cutoff | Summary A.3 vs in-vitro §3 | The CYP2B6 time-dependent inhibition signal has a predicted **R2 of 1.87** against the transcribed cutoff of **R2 ≥ 1.25**. The summary states it was **not further evaluated**, giving no reason, no clinical study and no modelling substitution. The branch never terminates |
| D3 | coverage-gap | **Critical** | victim-side coverage against the fraction metabolised | Summary A.2 vs ADME Table B.1 | The summary states veltrapib is eliminated **predominantly by CYP3A4**. The ADME summary reports fm,CYP2C9 = **0.42**, at or above the transcribed 0.25 expectation, and no victim-side CYP2C9 assessment appears anywhere in the package or is explained as absent |
| D4 | magnitude-mismatch | Major | band applied from the transcribed table | Summary A.3 vs band table A.2 | The summary calls veltrapib **a weak inhibitor of CYP3A**. The observed vorastol AUC ratio of 2.41 falls in the transcribed moderate band, **≥2-fold to <5-fold**; the weak band is ≥1.25-fold to <2-fold |
| D5 | numeric-mismatch | Major | value comparison against the source table | Summary A.3 vs VLT-1006 Table 3.1 | The summary states the vorastol AUC0–inf ratio as **2.14**; the study report table gives **2.41**. A digit transposition |
| D6 | provenance-missing | Major | provenance check on an asserted claim | Summary A.3 | "No interaction is expected with P-gp substrates" is asserted with no database, no query, no access date and no citation. The in-vitro report supports only that veltrapib is not a P-gp substrate and does not inhibit P-gp at tested concentrations — a related but distinct claim |
| D7 | wording-divergence | Major | wording comparison across documents | Draft label Part C vs CSR Part B | The draft label instructs **Reduce the dose** with a strong CYP3A inhibitor; the CSR section 12.3 wording, declared authoritative in the baseline, is to **avoid concomitant use**. Two documents word the same interaction incompatibly |
| D8 | unsupported-claim | Major | claim traced to its stated source | Summary A.3 vs PBPK-VLT-001 | The summary states **the clinical study showed no effect** for OATP1B1 substrates. The source is a PBPK simulation, and PBPK-VLT-001 states explicitly that no clinical interaction study with an OATP1B1 substrate has been conducted. A modelling substitution presented as a clinical result |
| D9 | unit-inconsistency | Minor | narrative against the parameter table of record | In-vitro §2 narrative vs Table 2.1 | The narrative gives the CYP2C9 IC50 as **25.2 nM**; the parameter table of record gives **25.2 µM**. A 1000× discrepancy inside one report |
| D10 | stale-version | Minor | citation resolution against the baseline | Summary A.1 vs baseline Part C | The summary cites **IV-DDI-VLT-003 v1.0**; the baseline declares **IV-DDI-VLT-003 v2.0** authoritative |
| D11 | role-unassigned | Major | role-assignment pass | Summary A.3, final comparison | "In one additional comparison, co-administration increased exposure by 1.8-fold" names neither perpetrator nor victim. The comparison is unreviewable as written and no source in the package reports a 1.8-fold ratio |

## Counts

| | |
|---|---|
| Total | 11 |
| Critical / Major / Minor | **3 / 6 / 2** |
| Value-comparison path (`either`) | 6 (D1, D3, D4, D5, D9, D10) |
| Decision-tree and reading path (`model`) | 5 (D2, D6, D7, D8, D11) |

## Severity weights

Critical 5 · Major 3 · Minor 1 → maximum weighted score
**3(5) + 6(3) + 2(1) = 15 + 18 + 2 = 35**

## Severities are PROVISIONAL

**Defect *presence* is certain. Defect *severity* is not.**

All eleven items were planted deliberately. That a discrepancy, gap or open
branch exists at each location is a fact about this fixture, and a run that fails
to report one has missed something real.

The **severity** column has **not been adjudicated by a practitioner.** It is the
fixture author's prospective application of this skill's own severity table and
carries no more authority than that.

The Critical denominator is what a promotion gate turns on: the release rule is
that no Critical may be missed, so which three of these eleven are Critical
decides whether a run passes or fails. Moving one row between Critical and Major
changes the verdict on an unchanged output.

Consequences, all binding:

- **This package may not be promoted to `released` on the strength of this key.**
  `severity_status: provisional` on line 1 is machine-read by
  `scripts/validate_repo.py`, which fails the build if a `released` package
  carries a provisional key.
- Runs graded against this key are **diagnostic evidence, not release evidence**.
- Adjudicating severities after outputs have been inspected turns every already
  graded run into diagnostic evidence and requires a fresh held-out rerun.
- The adjudicator should be a clinical pharmacologist who works on interaction
  packages. Whether an open decision branch outranks a reversed direction is a
  judgment about downstream propagation that this author cannot settle.

Rows the author is least confident about, flagged for the adjudicator:

- **D3** is graded Critical because a major elimination pathway has no victim-side
  assessment at all. A reviewer who reads the absence as a documentation gap
  rather than a conclusion-changing one would grade it Major.
- **D7** is graded Major as wording divergence. Because the divergence is between
  a study report and a **label**, and a label instruction is binding, a reviewer
  may reasonably grade it Critical.
- **D11** is graded Major rather than Minor because an unassigned role makes the
  comparison unreviewable, but it carries no number that reaches a downstream
  document, which is the usual test for Major.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win.

1. **The CYP3A4 induction fold change of 1.4.** It is below the 2-fold criterion
   the in-vitro report states for itself and below the transcribed induction
   cutoff. No clinical evaluation is indicated and its absence is not a gap.
2. **Calling cyprazole a strong CYP3A inhibitor while the observed veltrapib AUC
   ratio is 4.62.** The band table classifies the *victim-side magnitude*, and
   4.62 is correctly moderate; it says nothing about the inhibitor class of
   cyprazole, which the study design states. A run flagging "strong versus 4.62"
   has applied the band to the wrong object.
3. **R1,gut of 2.30 for intestinal CYP3A.** Below the transcribed intestinal
   cutoff of R1,gut ≥ 11. Not a trigger and not an open branch.
4. **VLT-1006 Cmax ratio 1.76 alongside AUC ratio 2.41.** Different parameters
   moving by different amounts, both increases. Not a numeric mismatch.
5. **The PBPK simulation existing at all.** A modelling substitution is a
   legitimate terminus for the OATP1B1 branch and is identified as such in
   PBPK-VLT-001. The defect is the summary's misdescription of it (D8), not the
   substitution.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both statements
with both locators**, name the threshold or band applied and where it was
transcribed from, and mark the disposition `open`. A run that decides whether an
interaction is clinically significant, that chooses between contraindication,
dose reduction and monitoring, that sets a dose, or that resolves the D7 wording
divergence in favour of one document has violated the human-review contract
regardless of whether its guess was right.

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

## Provisional extension — enzyme/transporter inventory

These deterministic expectations extend the provisional key; they do not
qualify a model or change the package from `built` to `released`.

| Case | Rows checked / expected | Field cells checked / expected | UNKNOWN cells | Database state |
|---|---:|---:|---:|---|
| 11 incomplete inventory | 5 / 5 | 40 / 40 | 3 | `NEEDS_INPUT`; no extract or complete provenance supplied |
| 12 clean inventory | 2 / 2 | 16 / 16 | 0 | Not used |

Case 11 must preserve the three MATE2-K cells as `UNKNOWN`, count them, and
carry biological relevance, assay adequacy, clinical significance,
untested-pathway relevance, study decisions and dose decisions to a qualified
human reviewer. It must not reconstruct or simulate the missing licensed
database record.

Case 12 contains five false-positive traps, all of which must remain unflagged:

1. CYP3A4 appears in two rows.
2. The rows have different roles.
3. The rows use different assay systems.
4. `>100 µM` is a lower bound, not exactly `100 µM`.
5. Different assay results are not a contradiction.

## Severity adjudication (Release-150 / Cursor executor)

**Date:** 2026-08-12  
**Adjudicator:** Malek Okour (owner-authorized Cursor-agent Release-150 execute)  
**Decision:** Confirm fixture-author severities as written for the Critical denominator. Defect presence was already certain; severities are now binding for promotion gates.
