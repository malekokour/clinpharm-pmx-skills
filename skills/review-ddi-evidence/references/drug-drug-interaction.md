---
module: drug-drug-interaction
version: "1.1"
owner: Malek Okour
reviewed: "2026-08-11"
anchors: [ich-m12, fda-labeling-cp]
consumers: [review-ddi-evidence, review-csr-pk-consistency, review-protocol-pk-sections, review-uspi-section-12-content, review-ctd-272-content, assess-development-plan-gaps, reconcile-cross-document-facts]
---

# Study-type module — drug-drug interaction

Reference content only. The workflow that consumes this module is unchanged by
it; only the criteria change.

Every DDI statement is either **perpetrator** (this drug changes another's
exposure) or **victim** (another changes this drug's). A ratio reported without
a named substrate cannot be checked at all — role assignment is the first check.

## Numeric cutoffs — read before using

`ich-m12` is Step 4, dated 2024-05 in `guidance-index`, on a **research-sourced**
row not independently re-verified. The basic-model cutoffs in circulation — R1
(reversible inhibition), R1,gut (intestinal CYP3A), R2 (time-dependent
inhibition), R3 (induction), and the transporter ratio cutoffs — are
**PROVISIONAL here**: widely applied and largely harmonised with prior FDA
in-vitro DDI practice, but deliberately **not** hardcoded in this module. A
stage-1 verification must transcribe them, and the strong / moderate / weak
magnitude bands, from the current M12 text before any numeric check below runs.
**UNVERIFIED:** any cutoff or band not read from that text at review time.

## Source and applicability contract

Source basis: current FDA-adopted ICH M12 supports stepwise review of enzyme-
and transporter-mediated pharmacokinetic DDI. It is nonbinding guidance, excludes
pharmacodynamic interactions and some modalities, and does not make a reported
assay clinically relevant by itself.

Before inventorying, obtain an owner-declared source set, compound, pathway scope,
review date, and source-status baseline (`FINAL`, `DRAFT`, `SUPERSEDED`,
`LICENSED-EXTRACT`, or `UNKNOWN`). If the pathway universe is not declared,
report scope applicability as `UNKNOWN`; do not infer that an unmentioned pathway
was tested or is irrelevant.

When a licensed database is cited, accept only the user-supplied database name,
query, access date, retrieved statement, licence-permitted locator, and status.
Never query without authority, reproduce the database, reconstruct an entry from
memory, or simulate proprietary content. Missing provenance is `NEEDS_INPUT`.

## Design conventions to check

- Perpetrator and victim roles stated explicitly for every arm.
- Index perpetrator or index substrate named, with dose and schedule.
- Dosing duration adequate for the mechanism claimed — a time-dependent
  inhibition or induction claim needs multiple-dose perpetrator administration.
- Sampling covers the interaction window; washout stated for crossover designs.
- Enzyme or transporter pathway under test named, not implied.
- Any model (PBPK or static) substituting for a clinical study identified as
  such, rather than the substitution left as a silent gap.
- Victim-side trigger pre-specified: fraction metabolised, with its source.

## `ENZYME-TRANSPORTER-INVENTORY`

Create one row per owner-declared identity × role × assay result. A single
identity used as a substrate in one assay and inhibitor in another is two rows,
not a contradiction. Preserve strings, units, inequality signs, and qualifiers
verbatim. Check exactly **8 fields per inventory row**:

| # | Field | Mechanical requirement |
|---:|---|---|
| 1 | Enzyme/transporter identity | Exact reported name; never normalise two identities into one |
| 2 | Assay system | Matrix, cell system, preparation, or platform as supplied |
| 3 | Substrate/inhibitor/inducer role | One supplied role per row; `UNKNOWN` when unstated |
| 4 | Concentration | Exact tested or reported concentration/range with unit; `UNKNOWN` when absent |
| 5 | Result | Exact reported parameter or categorical result without interpretation |
| 6 | Qualifier | Inequality, total/unbound basis, probe, conditions, or limitation as supplied |
| 7 | Source status | Owner-declared `FINAL`, `DRAFT`, `SUPERSEDED`, `LICENSED-EXTRACT`, or `UNKNOWN` |
| 8 | Exact locator | Document, version, section/table, row, and page where available |

Report `inventory rows checked / owner-declared rows expected` and `field cells
checked / field cells expected`, where expected field cells equal rows × 8. An
`UNKNOWN` cell is checked but unresolved and remains in the denominator. If the
owner cannot declare the expected row or pathway universe, state that denominator
as `UNKNOWN`; never convert the rows found into a completeness claim.

This inventory reports what the supplied sources say. It does not infer a
negative result from `not tested`, rank pathways, assess assay adequacy, determine
biological relevance, decide clinical significance, or decide whether another
study is needed.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Direction | Named perpetrator and named victim, per comparison |
| Comparison | Geometric mean ratio, with-perpetrator / alone |
| Precision | 90% confidence interval on the ratio |
| Parameters | Cmax and AUC at minimum, each with its own ratio and interval |
| In-vitro basis | Ki, IC50, or induction parameter, with the assay system named |
| Model output | Cutoff variable computed, with its inputs shown |
| Decision | In-vitro result carried to "study conducted" or "not conducted, with reason" |
| Management | What is done about it, or an explicit statement that no action follows |

## Mechanical checks this module enables

1. **Role assignment present and single-valued.** No named perpetrator, no named
   victim, or the same drug in both roles makes the comparison unreviewable.
2. **Direction versus ratio.** A stated "decreased exposure" alongside a ratio
   above 1.00 is a contradiction between two reported facts.
3. **Ratio recomputes** from the reported with-perpetrator and alone means, and
   the **CI brackets the point estimate** per parameter. Both delegated to T03.
4. **Cutoff variable recomputes** from its own stated inputs; arithmetic only,
   delegated to T03. Its threshold comes from the verified M12 text, not here.
5. **In-vitro-to-clinical decision logic is closed.** Every reported in-vitro
   signal terminates in a clinical study, a modelling substitution, or a stated
   reason for neither; an open branch is a findable gap.
6. **Potency units and terms consistent** across in-vitro tables, model inputs
   and text — µM versus ng/mL, Ki versus IC50 used interchangeably.
7. **Magnitude label matches the reported ratio** — a classification whose ratio
   falls outside the guidance band for that label is a mismatch.
8. **Management statement present wherever an interaction is reported**, worded
   consistently across CSR, module 2.7.2 and label. Delegated to T05.
9. **Victim-side coverage accounted for** — where a fraction metabolised by a
   pathway is reported, a victim assessment is present or its absence explained.
10. **Enzyme/transporter inventory is source linked.** Every owner-declared row
    carries all eight fields or an explicit `UNKNOWN`, plus its exact locator and
    source status. Licensed-database provenance is recorded, never reconstructed.

## Boundaries

This module does not decide whether an interaction is clinically significant,
select or adjust a dose, or choose between contraindication, dose reduction and
monitoring. It does not validate a PBPK model, assess in-vitro assay quality,
judge whether a modelling substitution was adequate, or make any regulatory
commitment. It checks that reported facts agree and required elements are
present. Biological relevance, assay adequacy, clinical significance, untested-
pathway relevance, and any study or dose decision remain human-only. A qualified
reviewer supplies every judgment.
