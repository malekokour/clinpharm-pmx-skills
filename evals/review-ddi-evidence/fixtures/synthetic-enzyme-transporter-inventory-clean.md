---
fixture-id: ddi-inventory-clean
compound: veltrapib
expected-inventory-rows: 2
expected-fields-per-row: 8
expected-field-cells: 16
expected-unknown-cells: 0
licensed-database-extract-supplied: false
source-status-vocabulary:
  - FINAL
---

# Synthetic enzyme/transporter inventory — complete fields

Synthetic public-safe fixture for deterministic false-positive testing. Values
are invented and have no clinical meaning.

Review date: 2026-08-11
Owner-declared source set: IV-DDI-VLT-005 v1.0
Owner-declared pathway universe: CYP3A4

| Enzyme/transporter identity | Assay system | Substrate/inhibitor/inducer role | Concentration | Result | Qualifier | Source status | Exact locator |
|---|---|---|---|---|---|---|---|
| CYP3A4 | pooled human liver microsomes | inhibitor | 0.1–100 µM | IC50 >100 µM | lower bound; preserve as reported | FINAL | IV-DDI-VLT-005 v1.0, Table 2, row CYP3A4 inhibition |
| CYP3A4 | cryopreserved human hepatocytes | inducer | 0.01–10 µM | maximum mRNA fold change 1.20 | concentration-dependent assessment | FINAL | IV-DDI-VLT-005 v1.0, Table 4, row CYP3A4 induction |

The two rows intentionally share an identity but describe different roles and
assay systems. They are separate inventory rows, not a contradiction. The
`>100 µM` result is a lower bound, not an exact value and not a unit mismatch.
