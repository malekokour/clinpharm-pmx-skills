# SYNTHETIC — PBPK reporting source and report pair

> Fully synthetic. Generated for diagnostic evaluation only. No real compound,
> sponsor, participant, model, dataset, or analysis result is represented.

## Part A — pre-stated reporting source

**Context of use:** describe the declared human concentration-time prediction
for synthetic compound veloradine and compare it with the named observed dataset.
This source does not support species selection, dose selection, or a claim of
predictive adequacy.

| Trace field | Pre-stated identity or criterion | Locator |
|---|---|---|
| Model identity | SYN-PBPK-MODEL-007 v2.1 | source table row 1 |
| Model hash | 1111111111111111111111111111111111111111111111111111111111111111 | source table row 2 |
| Hepatic clearance provenance | SYN-IN-VITRO-CL-02 | source table row 3 |
| Tissue partition provenance | SYN-METHOD-KP-01 | source table row 4 |
| Run identity | SYN-PBPK-RUN-2026-08-11-A | source table row 5 |
| Platform/environment | SYN-PBPK-ENGINE 4.2 / SYN-ENV-17 | source table row 6 |
| Observed/predicted trace | SYN-OBS-HV-03 linked to SYN-PRED-HV-03 | source table row 7 |
| Acceptance criterion | AUC ratio 0.80–1.25 and Cmax ratio 0.80–1.25 | source table row 8 |

## Part B — PBPK report under review

**Report identity:** SYN-PBPK-REPORT-007 v1.0.

The report names **SYN-PBPK-MODEL-007 v2.0** and run
**SYN-PBPK-RUN-2026-08-11-B**. It cites platform SYN-PBPK-ENGINE 4.2 and
environment SYN-ENV-17.

Hepatic clearance is attributed to SYN-IN-VITRO-CL-02. Tissue partition
coefficients are listed, but no provenance locator is supplied.

Predicted output SYN-PRED-HV-03 is shown. The report says the observed comparison
was satisfactory but supplies no observed-dataset identity or locator.

The report calls visual agreement acceptable. It does not state or evaluate the
pre-stated AUC-ratio and Cmax-ratio criterion.

The conclusion says the analysis **supports selection of the Phase 2 dose**,
which is outside the pre-stated context of use.
