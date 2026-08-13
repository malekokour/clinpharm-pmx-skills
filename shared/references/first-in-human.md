---
module: first-in-human
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
anchors: [ema-fih, fda-mrsd]
consumers: [review-protocol-pk-sections, prepare-dose-justification-evidence, assess-development-plan-gaps, review-ctd-272-content, reconcile-cross-document-facts, review-csr-pk-consistency]
---

# Study-type module — first-in-human

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

Both anchors are `research-sourced` in `guidance-index.md` — dates inherited, not
re-verified against the issuing body's page. Per maintenance rule 1, verify
`ema-fih` (EMA 2017 Rev 1) and `fda-mrsd` (FDA 2005) before this module freezes.

## Design conventions to check

- Starting-dose derivation stated with its **method named** — NOAEL/HED, PAD, or
  MABEL — and every input reported: pivotal species, NOAEL with units, the
  interspecies conversion factor, and the safety factor applied.
- Where more than one method is presented, the value that governs is stated
  explicitly, with the others shown for comparison.
- MABEL derivation present where the mechanism is agonist, immune-modulating, or
  target-amplifying — the mechanism triggers it, not the molecule class.
  PROVISIONAL: treating "biologic" alone as the trigger is practice convention.
- Escalation schema pre-specified: every planned dose level listed, the increment
  rule stated, and a maximum planned dose or maximum planned exposure named.
- Sentinel dosing described for the first cohort. PROVISIONAL: the
  one-active/one-placebo composition and an observation interval spanning
  expected Tmax are convention, not fixed criteria.
- Staggering interval — sentinel to remainder, and cohort to cohort — stated as a
  duration with the observation window it covers.
- Stopping rules pre-defined at subject, cohort, and trial level, with
  progression criteria stated separately from them.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Pivotal species | Named, with why it was carried forward |
| NOAEL | Value with units and the study it came from |
| HED | Value with units, plus the animal-to-human conversion factor it used, sourced to the guidance table |
| Safety factor | A number, with the reason if it departs from the default |
| Starting dose | A value at or below the derived maximum, in the units the protocol doses in |
| MABEL (where applicable) | The in vitro or PK/PD basis, the endpoint, and the factor applied |
| Escalation | Full dose-level list, increment rule, maximum planned dose, and the anticipated human Cmax/AUC at that dose against the nonclinical exposure bounding it |
| Stopping rules | Explicit criteria, separately stated from progression criteria |

## Mechanical checks this module enables

1. **HED recomputes** from the stated NOAEL and conversion factor. Delegated to
   T03. A mismatch is a disagreement between two reported numbers, not evidence
   that either is wrong.
2. **Starting dose recomputes** as HED — or the MABEL-derived value — divided by
   the stated safety factor. Delegated to T03.
3. **Safety factor is reported as a number**, and a departure from the default
   carries a reason. UNVERIFIED: `fda-mrsd` states a numeric default — do not
   assert its value until the anchor is re-verified.
4. **Governing species is the one it claims to be.** Where HEDs are tabled per
   species, the value carried forward is the lowest, or a justification exists.
5. **Multiple methods reconcile.** Where NOAEL-, PAD-, and MABEL-derived values
   are all reported, the dose used is at or below all, or one is named as governing.
6. **Unit consistency across the derivation chain** — mg/kg, mg/m², and flat mg
   mixed without a stated reference body weight is a mechanical defect.
7. **Escalation arithmetic.** Each listed level follows from the previous by the
   stated increment rule; the highest equals the stated maximum planned dose. T03.
8. **Exposure margin recomputes** from anticipated human exposure at the maximum
   planned dose against the nonclinical exposure it is bounded by. T03.
9. **Required elements present** as discrete statements: sentinel dosing,
   staggering interval, stopping rules, progression criteria.
10. **Cross-document identity.** Starting dose, NOAEL, HED, safety factor, and
    maximum planned dose identical across brochure, protocol, and CTD summaries. T05.

## Boundaries

This module does not select or adjust a starting dose, does not decide whether a
safety factor is adequate, does not judge whether MABEL was required for a given
molecule, and does not assess whether an escalation schema or staggering interval
is safe. Absence of a required element is findable; adequacy is not. It never
evaluates whether a stopping rule should have triggered — real-time escalation
decisions are excluded from this library. A qualified reviewer applies judgment;
the sponsor makes the regulatory commitment.

This module does not decide whether any observed difference is **clinically significant**, and does not **select, adjust or justify a dose**. Both are reserved for a qualified reviewer.
