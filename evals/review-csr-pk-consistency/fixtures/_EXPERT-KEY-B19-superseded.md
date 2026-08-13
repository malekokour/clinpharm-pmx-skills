# Expert key — synthetic CSR fixture PHX-101

> **Answer key. Do not supply this to the model under evaluation.**
>
> 12 planted defects across all eight finding classes and all three detection
> paths. Every one is discoverable from the supplied documents alone; none
> requires outside knowledge.

## Design constraints this fixture satisfies

- Every output field of the register is exercised — a fixture that never produces
  a Minor presentation defect or a stale-version flag cannot evaluate those
  behaviours.
- Severity is deliberately weighted toward Critical (**4 of 12**), because the
  real cost is propagation into a summary or a label, not defect count.
- The detection-path split is an engineering allocation, not a hope: **6 script**,
  **2 script+model**, **4 model-only**. Per-path recall is reported separately;
  a script-path miss is a script bug.

## The twelve

| # | Class | Sev | Path | Where | What |
|---|---|---|---|---|---|
| D1 | numeric-mismatch | **Critical** | script | Synopsis §2.3 vs Table 14.2.1 | Synopsis states AUC0–τ **412** ng·h/mL; table and NCA say **481**. 14% apart, far beyond the 0.5% plan tolerance |
| D2 | numeric-mismatch | Major | script | Synopsis §2.3 vs NCA / §12.3 | Synopsis half-life **8.2 h**; NCA output and body both say **11.4 h** |
| D3 | plausibility-violation | Major | script | §12.3 with NCA tau | Accumulation **1.9** against t½ 11.4 h and tau 24 h implies ≈1.96 — consistent. **Against the synopsis's 8.2 h it implies ≈1.63.** The inconsistency is with D2's wrong half-life; both must be flagged |
| D4 | unit-inconsistency | **Critical** | script | Table 14.2.1 cohort 3 | CL/F given as **15.2 mL/h**; every other cohort and the plan say **L/h**. A 1000× unit swap |
| D5 | unsupported-claim | **Critical** | script+model | Synopsis §2.3 vs Table 14.2.4 | "Dose-proportional over the **50–200 mg** range" — the only analysis covers **50–400 mg**, and the plan states a sub-range claim needs its own analysis |
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

## Counts

| | |
|---|---|
| Total | 12 |
| Critical / Major / Minor | 4 / 5 / 3 |
| Script-detectable | 6 (D1, D2, D3, D4, D7, D8) |
| Script + model | 2 (D5, D6) |
| Model-only | 4 (D9*, D10, D11, D12) |

\* D9 is script-detectable **only when the version baseline (I8) is supplied**.
Without it, it degrades to model-only. This is deliberate: it measures whether
the skill actually uses the baseline input rather than ignoring it.

## Severity weights

Critical 5 · Major 3 · Minor 1 → maximum weighted score **4(5) + 5(3) + 3(1) = 38**

## What must NOT be flagged — false-positive traps

A run that flags any of these has a precision problem, not a recall win:

1. **Cohorts 1, 2, 4 CL/F values** — all correctly in L/h. Only cohort 3 is wrong.
2. **AUC 206 vs Cmax 124 in cohort 2** — different parameters, not a mismatch.
3. **Body §12.3 half-life 11.4 h** — this one is *correct*; the synopsis is wrong.
   A run flagging the body value has picked the wrong side of D2.
4. **Table 14.2.4 slope 1.08 with CI spanning 1.0** — a legitimate result, not a
   defect. The defect is the significant-figure inconsistency, not the number.
5. **Food-effect AUC ratio 1.29** — consistent with its CI and with the Cmax
   direction. Only the synopsis wording is reversed.

## Adjudication boundary

For every defect above, the expected behaviour is to **report both values with
both locators** and mark the disposition `open`. A run that states which value is
correct, or that resolves a contradiction, has violated the human-review contract
regardless of whether its guess was right.
