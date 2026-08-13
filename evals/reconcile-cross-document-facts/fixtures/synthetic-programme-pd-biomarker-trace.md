# Synthetic programme-thread PD/biomarker trace

All values are synthetic. No participant-level information is present.

Declared measure: `pSTAT3-change` (1 measure). Declared role: PD measure.
Declared context of use: describe pathway modulation across programme SYN-PD;
no clinical decision use. Qualification-route status is `UNKNOWN`.

| Source | Version | Status |
|---|---|---|
| Protocol SYN-PD-11 | 2.0 | final |
| CSR SYN-PD-11 | 1.0 | final |
| Module 2.7.2 SYN-PD | 3.0 | draft |

| Field | Protocol origin | CSR restatement | Module 2.7.2 restatement |
|---|---|---|---|
| Identity | `pSTAT3-change` (§7.5) | `pSTAT3-change` (§11.7) | `phospho-STAT3 change`, synonym map not supplied (§3.2) |
| Role | `PD measure` (§7.5) | `PD measure` (§11.7) | `PD measure` (§3.2) |
| Context of use | `describe pathway modulation; no clinical decision use` (§7.5) | same (§11.7) | same (§3.2) |
| Specimen | `K2EDTA plasma` (§7.5.1) | `K2EDTA plasma` (§9.8) | `serum` (§3.2) |
| Method | `LC-MS method SYN-LC v1` (§7.5.2) | `LC-MS method SYN-LC v1` (§9.8) | `LC-MS method SYN-LC v2` (§3.2) |
| Timing | `predose and 4 h postdose Day 1` (Schedule) | same (Table 14.4.2) | same (§3.2) |
| Decision rule | `report percent change; no threshold` (§7.5) | same (§11.7) | `response if change >= 20%` (§3.2) |
| Validation reference | no reference supplied | no reference supplied | no reference supplied |

Expected structural states: four `MISMATCH` findings (Identity, Specimen, Method,
Decision rule), one Validation-reference `UNKNOWN`, and three `PRESENT` fields.
Coverage is **7 / (8 × 1)** with **1 declared measure**. All findings remain
`HUMAN_REVIEW`; no clinical or qualification interpretation is permitted.
