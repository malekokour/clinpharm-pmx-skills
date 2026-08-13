<!-- VENDORED from shared/references/sad-mad.md at build time. Do not edit here.
     Edit the canonical source and rebuild; a freshness check compares them. -->

---
module: sad-mad
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [ema-fih, fda-mrsd, ich-e4]
consumers: [review-csr-pk-consistency, review-protocol-pk-sections, review-fih-dose-rationale, verify-nca-outputs]
---

# Study-type module — single and multiple ascending dose

Integrated SAD + MAD protocols are the norm in early development. This module
supplies the parameter conventions and the statement expectations a report of
such a study should satisfy.

## Design conventions to check

- Dose levels and escalation schema pre-specified, with stopping rules.
- Sentinel dosing and staggered cohorts where the risk profile calls for them.
- Sampling schedule adequate to characterise the terminal phase — conventionally
  spanning at least three half-lives after the last dose.
- Steady-state assessment in the MAD part: pre-dose concentrations across
  consecutive days supporting the claim.
- Accumulation and dose-proportionality assessments pre-specified rather than
  discovered.

## Parameter expectations

| Part | Parameters normally reported |
|---|---|
| SAD | Cmax, Tmax, AUC0-t, AUC0-inf, t½, CL/F, Vz/F |
| MAD | Cmax,ss, Ctrough, AUCtau, accumulation ratio, time to steady state |

## Statement expectations

- **Dose proportionality** stated with the dose range it applies to, supported by
  a pre-specified analysis. A bare "dose-proportional" with no range and no
  statistic is an unsupported claim.
- **Accumulation** consistent with the reported half-life and dosing interval.
- **Steady state** claimed only where the data show it.
- **Half-life** derived over an interval the sampling schedule can support.

## Mechanical checks this module enables

1. **Accumulation versus half-life.** Delegated to T03; a large deviation is a
   mechanical inconsistency between two reported numbers, not proof either is
   wrong — multi-compartment and time-dependent kinetics legitimately break the
   one-compartment relation.
2. **Dose-proportionality claim has a supporting statistic and a stated range.**
3. **Terminal-phase adequacy.** Sampling duration versus reported half-life.
4. **Steady-state claim has supporting pre-dose data.**
5. **Cohort tables reconcile** with in-text summary values.

## Boundaries

The module does not judge whether escalation was appropriate, does not assess
safety, and does not evaluate whether a stopping rule should have triggered.
Real-time escalation decisions are excluded from this library entirely.
