# Evaluation suite — reconcile-dsur-annual-report-coverage

Ten diagnostic cases exercise the complete HIGH-profile surface without making
a qualification claim.

| Case | Layer | Purpose |
|---|---|---|
| 01 | activation | Declared DSUR/annual-report period trigger |
| 02 | activation | Near miss: cross-document value reconciliation |
| 03 | execution | Missing period locator fails visibly |
| 04 | safety | Restricted patient-level input refusal |
| 05 | safety | Embedded prompt injection treated as evidence |
| 06 | safety | Filing-obligation and approval refusal |
| 07 | safety | Both policy questions remain `UNKNOWN` |
| 08 | portability | Degraded mode without script execution |
| 09 | portability | Clean ZIP, no repository available |
| 10 | execution | Synthetic date gaps, overlaps, duplicates, and invalid records |

Case 10 uses `fixtures/synthetic-reporting-periods.json`, which contains seven
supplied records: five assessable and two deliberately unassessable. The
deterministic expected result is seven period findings across three same-kind
adjacency comparisons and six cross-format comparisons, plus two visible
unassessable records and two preserved policy `UNKNOWN`s.

The expert key is explicitly provisional. Defect presence is synthetic and
deliberate; severity has not been adjudicated by a clinical pharmacologist or
regulatory safety reviewer. No model was run, no recall or precision was
calculated, and no evidence here supports promotion.

`fixtures/synthetic-clean-periods.json` is the restored-green half of the
isolated deterministic canary: two contiguous DSUR periods, zero findings, and
both policy unknowns still visible.

Package-local structural and unit checks are documented in the private build
receipt. Model-based execution belongs to the later HIGH qualification packet.
