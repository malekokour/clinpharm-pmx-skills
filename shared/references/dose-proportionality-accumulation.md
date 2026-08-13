---
module: dose-proportionality-accumulation
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [ich-e4]
consumers: [review-csr-pk-consistency, verify-nca-outputs, review-protocol-pk-sections, review-uspi-section-12-content, review-ctd-272-content, reconcile-cross-document-facts, prepare-dose-justification-evidence]
---

# Study-type module — dose proportionality and accumulation

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

## What the anchor does and does not supply

`ich-e4` establishes that dose-response information supports registration. It
does **not** prescribe a statistical method for dose proportionality, an
acceptance interval for a power-model slope, or a numeric accumulation
threshold. Every analysis convention below is therefore **PROVISIONAL** —
practice, not regulation — and must never be reported as a guidance requirement.

**UNVERIFIED:** `ich-e4` is carried in `guidance-index.md` as `research-sourced`
(final, 1994-03), not re-verified against the ICH page. Verify in stage 1.

## Design conventions to check

- The **dose range** stated as an explicit low-to-high span with units, never as
  "across doses" or "the studied range".
- The analysis method **pre-specified**, not chosen after seeing the data: power
  model on log dose, ANOVA on dose-normalised parameters, or a stated
  equivalence-style comparison — with the parameters it carries (conventionally
  AUC and Cmax) and the single-dose or steady-state part they apply to.
- For accumulation: dosing interval τ, the reference occasion (day 1) and the
  steady-state occasion each stated, so the ratio has a defined numerator and
  denominator.
- A pre-specified basis for the steady-state claim — pre-dose concentrations
  across consecutive intervals, or a stated test.
- Sampling adequate for the terminal phase the accumulation claim rests on.
  PROVISIONAL convention: coverage of at least three half-lives.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Dose range | Explicit low and high dose with units, and the number of levels |
| Method and result | Named pre-specified analysis, with its slope or ratio, a confidence interval, and the interval judged against |
| Parameters | AUC and Cmax at minimum; the AUC variant (0-t, 0-inf, tau) named |
| Accumulation ratio | Rac defined by the formula used, with the parameter and τ it applies to |
| Time to steady state | A stated value or interval, with the data supporting it |
| Half-life | The estimate the accumulation and steady-state statements rest on |
| Deviation | Where proportionality does not hold, the direction and dose region named |

## Mechanical checks this module enables

1. **A proportionality claim carries a range and a statistic.** A bare "exposure
   was dose-proportional" is unsupported regardless of whether it is true.
2. **The claimed range does not exceed the doses studied** — compare it against
   the dose levels in the design section. A claim reaching beyond the highest or
   below the lowest administered dose is an extrapolation stated as observation.
3. **Accumulation ratio versus half-life and τ**, and **Rac recomputed** from the
   day-1 and steady-state values where both appear. Both delegated to T03. A
   large deviation from the linear one-compartment relation is an inconsistency
   between two reported numbers, not proof either is wrong — multi-compartment
   disposition and time-dependent kinetics legitimately break the relation.
4. **Time to steady state versus half-life.** Delegated to T03; PROVISIONAL
   convention is roughly three to five half-lives for a linear drug. Flag the
   arithmetic disagreement, never a conclusion about the kinetics.
5. **Steady state claimed only where pre-dose data support it.** A stated
   attainment day with no pre-dose series or test behind it is a missing element.
6. **Units and AUC variant consistent** wherever the same parameter is cited;
   mixing AUC0-inf and AUCtau inside one claim is a unit-level inconsistency.
7. **Confidence interval brackets its point estimate**, and the acceptance
   interval judged against is stated rather than implied. Delegated to T03.
8. **Label, CSR and 2.7.2 state the same range and the same ratio**, and no
   unqualified claim contradicts a stated deviation. Delegated to T05, as are
   cross-document occurrences of checks 2 and 6.

## Boundaries

This module does not decide whether a deviation from dose proportionality is
clinically significant, does not select or adjust a dose, does not judge whether
a dose range is adequate for registration, and does not approve a labelling
statement. It neither chooses an analysis method nor sets an acceptance interval
— where none is stated, it reports the absence. It supplies criteria; a
qualified reviewer applies judgment.
