severity_status: adjudicated

# Expert key — synthetic CSR fixture PHX-101

> **Severities adjudicated by Malek Okour, B19 (2026-08-06) and B20 (2026-08-06).**
> `severity_status: adjudicated` above is machine-read by `validate_repo.py`: a key
> marked `provisional` blocks `released` outright, because a promotion gate turns on
> the Critical denominator and that denominator is exactly what an unadjudicated key
> has not fixed.

> **Answer key. Do not supply this to the model under evaluation.**
>
> 12 planted defects across all eight finding classes and all three detection
> paths. Every one is discoverable from the supplied documents alone; none
> requires outside knowledge.

## Design constraints this fixture satisfies

- Every output field of the register is exercised — a fixture that never produces
  a Minor presentation defect or a stale-version flag cannot evaluate those
  behaviours.
- Severity is weighted toward Critical (**3 of 12** since B20; 4 of 12 under B19), because the
  real cost is propagation into a summary or a label, not defect count.
- The detection-path split is an engineering allocation, not a hope: **6 script**,
  **2 script+model**, **4 model-only**. B20 changed a severity, not a detection path,
  so this split is unaffected. Per-path recall is reported separately;
  a script-path miss is a script bug.

## The twelve

| # | Class | Sev | Path | Where | What |
|---|---|---|---|---|---|
| D1 | numeric-mismatch | **Critical** | script | Synopsis §2.3 vs Table 14.2.1 | Synopsis states AUC0–τ **11300** ng·h/mL; table and NCA say **13158**. 14% apart, far beyond the 0.5% plan tolerance |
| D2 | numeric-mismatch | Major | script | Synopsis §2.3 vs NCA / §12.3 | Synopsis half-life **8.2 h**; NCA output and body both say **11.4 h** |
| D3 | plausibility-violation | Major | script | §12.3 with NCA tau | Accumulation **1.9** reconciles with neither half-life. `Racc = 1/(1−e^−kτ)` gives **1.303** at t½ 11.4 h and **1.151** at 8.2 h, both with τ 24 h. **Corrected 2026-08-06 (B26): this row previously asserted ≈1.96 for 11.4 h and called 1.9 consistent — wrong by ~50%, and candidate run-3 computed 1.303 correctly and was graded against the error.** The defect stands; its reasoning does not. The inconsistency is with D2's wrong half-life; both must be flagged |
| D4 | unit-inconsistency | **Critical** | script | Table 14.2.1 cohort 3 | CL/F given as **15.2 mL/h**; every other cohort and the plan say **L/h**. A 1000× unit swap |
| D5 | unsupported-claim | Major | script+model | Synopsis §2.3 vs Table 14.2.4 | "Dose-proportional over the **50–200 mg** range" — the only analysis covers **50–400 mg**, and the plan states a sub-range claim needs its own analysis |
| D6 | contradiction | **Critical** | script+model | Synopsis §2.3 vs Table 14.2.5 | Synopsis says a **decrease** in Cmax; the GMR is **1.34** — an increase. Direction reversed |
| D7 | numeric-mismatch | Major | script | Synopsis §2.3 vs Table 14.2.2 / §12.2 | Synopsis median Tmax **2.0 h**; table and body say **3.5 h** |
| D8 | presentation | Minor | script | Table 14.2.4 | Slope **1.08** given to three significant figures per plan; CI bounds **0.94–1.22** given to two. Internally inconsistent with the stated convention |
| D9 | stale-version | Major | script | §9.3 vs Protocol v3.0 | Methods list **four** dose levels; the current protocol incorporating Amendment 2 has **five** (adds 600 mg) |
| D10 | completeness-gap | Major | model | Synopsis §2.1 vs §11.2 | Synopsis says **all 32 subjects** were in the PK population; the body excludes **two cohort-4 subjects** from the steady-state summary |
| D11 | presentation | Minor | model | Figure 14.2.1 vs Table 14.2.1 | Figure y-axis in **µg/mL**; all tabulated concentrations are **ng/mL** |
| D12 | presentation | Minor | model | §9.5.4 vs version baseline | Cites Bioanalytical Report **v1.0**; the declared authoritative version is **v2.0** |

> **Severity adjudicated 2026-08-06 (B19).** The per-defect rows below are the
> governing ground truth for scoring this fixture; `SKILL.md` supplies the
> prospective classification rule and was harmonised to match. D2 and D7 remain
> **Major**: their half-life and Tmax mismatches are substantive and could
> mislead review, but in this fixture they do not change the headline exposure
> result, comparison direction, dose interpretation, or any downstream
> regulatory conclusion. D1's AUC mismatch does, so it stays Critical.
>
> The summary figures below were arithmetically stale — they read 5/4/3 and a
> maximum of 40 while the rows they summarise have always said 4/5/3 and 38.
> Corrected here; the rows were not touched.
>
> ---
>
> **Severity re-adjudicated 2026-08-06 (B20). D5: Critical → Major.** The B19
> record above is preserved unedited; this supersedes it for D5 only, and a
> decision changes here by adding a record, never by rewriting one. The prior
> key is retained verbatim at
> [`_EXPERT-KEY-B19-superseded.md`](_EXPERT-KEY-B19-superseded.md).
>
> Owner's rationale, recorded as given: the 50–200 mg dose-proportionality
> statement is unsupported and misleading because no sub-range analysis was
> performed — but the available 50–400 mg analysis supports proportionality over
> the broader range. In this synthetic fixture D5 does not reverse a comparison,
> change headline exposure, or materially alter dose interpretation, labelling,
> or a regulatory conclusion. Under the consequence-based rubric that makes it
> **Major**, on the same reasoning that keeps D2 and D7 Major.
>
> **The agreement of the three evaluation arms is NOT the justification.** They
> are correlated model outputs from a shared base model, not independent
> practitioner votes, and counting them as evidence for a severity would let a
> model's own tendency define the ground truth it is scored against. That eight
> of nine runs graded D5 Major is recorded as supporting information only.
>
> **This re-scoring happened after the outputs were inspected.** The nine runs
> graded under the B19 key are therefore **diagnostic, not release evidence**.
> No `released` status may rest on them. Promotion requires a fresh held-out
> rerun against this frozen key.
>
> ---
>
> **D4 adjudicated 2026-08-06 (B24): Critical — confirmed. This key is unchanged;
> the Critical denominator of 3 (D1, D4, D6) and the weighted maximum of 36 stand.**
>
> Recorded because it is the reasoning the rubric was missing, not because the
> labels moved. Owner's principle: **D5 is a wrong description of a correct
> analysis; D4 is a wrong value.** Fixing D5 changes nothing downstream — the
> 50–400 mg analysis still supports proportionality and the tabulated numbers are
> still right. Fixing D4 forces re-issue of a primary PK parameter that the popPK
> dataset, IB Sections 4/5, Module 2.7.2 and eventually Section 12.3 have already
> consumed. CL/F is the dose-selection input, `dose = CL/F × Css,target × τ`.
>
> **Obviousness is explicitly not a mitigation.** Three arms graded D4 Major
> because `15.2 mL/h` is self-evidently absurd. That reasoning defeats the purpose
> of a consistency-check skill, whose value is catching what careful readers miss —
> and it is unreliable besides: `mL/h` is legitimate for a low-clearance compound,
> unit strings are stripped on ingestion into analysis datasets, and a 1000× cohort
> outlier reads as apparent nonlinearity rather than as an error. Where that cohort
> sits inside the dose-proportionality assessment, D4 contaminates the very
> conclusion D5 merely overstates.
>
> `SKILL.md` now carries the three-tier consequence rubric this implies, including
> the swap condition: consistent `mL/h` permitted by the plan would be Minor. It is
> Critical here because the value is internally inconsistent with the other cohorts
> and the stated plan unit, so one of the two numbers is definitively wrong.

## Counts

| | |
|---|---|
| Total | 12 |
| Critical / Major / Minor | **3 / 6 / 3** (B20; was 4 / 5 / 3 under B19) |
| Script-detectable | 6 (D1, D2, D3, D4, D7, D8) |
| Script + model | 2 (D5, D6) |
| Model-only | 4 (D9*, D10, D11, D12) |

\* D9 is script-detectable **only when the version baseline (I8) is supplied**.
Without it, it degrades to model-only. This is deliberate: it measures whether
the skill actually uses the baseline input rather than ignoring it.

## Severity weights

Critical 5 · Major 3 · Minor 1 → maximum weighted score **3(5) + 6(3) + 3(1) = 36**

Was 38 under B19 (4/5/3). Recomputed, not adjusted: 15 + 18 + 3 = 36.

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win:

1. **Cohorts 1, 2, 4 CL/F values** — all correctly in L/h. Only cohort 3 is wrong.
2. **Flagging AUC0–τ against Cmax in cohort 2 as a numeric mismatch** — they are
   different parameters, so comparing them is a category error. **Restated
   2026-08-06 (B26):** the trap previously named the bare values `206` and `124`.
   Under the rebuilt table their ratio is pharmacokinetically plausible, so a
   ratio-based challenge is no longer a correct finding — but the trap must target
   the *category error*, not any mention of the two numbers.
3. **Body §12.3 half-life 11.4 h** — this one is *correct*; the synopsis is wrong.
   A run flagging the body value has picked the wrong side of D2.
4. **Concluding non-proportionality from the Table 14.2.4 slope 1.08 whose CI spans 1.0** — a legitimate result, not a
   defect. **Scope narrowed 2026-08-06 (B26):** this trap covers *only* the proportionality inference. The
   significant-figure inconsistency on the same three numbers **is** a real defect (D8), so a grader
   keyword-matching `1.08` cannot tell the two apart and will cross-contaminate them. Score the inference and
   the sig-fig breach separately.
5. **Food-effect AUC ratio 1.29** — consistent with its CI and with the Cmax
   direction. Only the synopsis wording is reversed.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both values with
both locators** and mark the disposition `open`. A run that states which value is
correct, or that resolves a contradiction, has violated the human-review contract
regardless of whether its guess was right.
