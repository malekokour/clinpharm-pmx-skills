# Synthetic CSR-local PD/biomarker trace

All values are synthetic. No participant-level information is present.

## Declared applicability

- Declared measures: 1 (`pERK-change`)
- Declared role: PD measure
- Context of use: describe pathway modulation in Study SYN-PD-01; no clinical decision use
- Population/scope: Study SYN-PD-01 CSR only
- Qualification-route status: not declared (`UNKNOWN`)
- Reviewers: synthetic CP reviewer and synthetic PD reviewer

## Source/status register

| Source | Version | Status | Locator |
|---|---|---|---|
| Protocol SYN-PD-01 | 3.0 | final | §7.4 |
| SAP SYN-PD-01 | 1.0 | final | §9.2 |
| CSR SYN-PD-01 | draft 0.8 | draft | §11.6 and Table 14.4.1 |

## Eight fields for `pERK-change`

| Field | Protocol/SAP source statement | CSR source statement |
|---|---|---|
| Identity | `pERK-change` (Protocol §7.4) | `pERK-change` (CSR §11.6) |
| Role | `PD measure` (Protocol §7.4) | `PD measure` (CSR §11.6) |
| Context of use | `describe pathway modulation; no clinical decision use` (Protocol §7.4) | same text (CSR §11.6) |
| Specimen | `K2EDTA plasma, frozen at -80 C` (Protocol §7.4.2) | same text (CSR Table 14.4.1 footnote a) |
| Method | `ECL assay SYN-ECL v1` (SAP §9.2) | `ECL assay SYN-ECL v2` (CSR Table 14.4.1 footnote b) |
| Timing | `predose and 2 h postdose on Day 1` (Protocol Schedule) | same text (CSR Table 14.4.1 header) |
| Decision rule | `report percent change; no threshold` (SAP §9.2) | same text (CSR §11.6) |
| Validation reference | no reference supplied in the declared source set | no reference supplied in the declared source set |

Expected trace states: one `MISMATCH` for Method, one `UNKNOWN` for Validation
reference, and six `PRESENT` fields. Coverage is **7 / (8 × 1)**, with **1
declared measure**. The route must not interpret plausibility, qualification,
meaningfulness, surrogate validity, assay fitness, endpoint selection, or dose.
