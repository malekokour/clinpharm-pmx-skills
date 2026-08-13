---
fixture-id: ddi-inventory-unknown
compound: veltrapib
expected-inventory-rows: 5
expected-fields-per-row: 8
expected-field-cells: 40
expected-unknown-cells: 3
licensed-database-extract-supplied: false
source-status-vocabulary:
  - FINAL
  - DRAFT
---

# Synthetic enzyme/transporter inventory — incomplete fields

Synthetic public-safe fixture for deterministic package testing. The owner has
declared five expected rows. Values are invented and have no clinical meaning.

Review date: 2026-08-11
Owner-declared source set: IV-DDI-VLT-004 v1.0 and TR-DDI-VLT-002 v0.4
Owner-declared pathway universe: CYP3A4, CYP2B6, OATP1B1, P-gp, MATE2-K

| Enzyme/transporter identity | Assay system | Substrate/inhibitor/inducer role | Concentration | Result | Qualifier | Source status | Exact locator |
|---|---|---|---|---|---|---|---|
| CYP3A4 | pooled human liver microsomes | inhibitor | 0.50–50 µM | IC50 14.2 µM | reversible inhibition | FINAL | IV-DDI-VLT-004 v1.0, Table 2, row CYP3A4 |
| CYP2B6 | cryopreserved human hepatocytes | inducer | 0.1–10 µM | maximum mRNA fold change 1.30 | concentration-dependent assessment | FINAL | IV-DDI-VLT-004 v1.0, Table 5, row CYP2B6 |
| OATP1B1 | HEK293-OATP1B1 cells | inhibitor | 0.03–30 µM | IC50 2.10 µM | uptake inhibition | DRAFT | TR-DDI-VLT-002 v0.4, Table 3, row OATP1B1 |
| P-gp | Caco-2 monolayer | substrate | 1 µM | efflux ratio 1.4 | bidirectional transport | FINAL | TR-DDI-VLT-002 v0.4, Table 1, row P-gp |
| MATE2-K | UNKNOWN | UNKNOWN | UNKNOWN | not tested | not tested | FINAL | TR-DDI-VLT-002 v0.4, Section 6, sentence 2 |

## Licensed database statement

The summary says “the interaction database supports the package,” but supplies
no database name, query, access date, retrieved statement, or licence-permitted
extract. This is `NEEDS_INPUT`; the reviewer must not reconstruct or simulate a
database record.
