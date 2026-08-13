# SYNTHETIC — topline snapshot and named sources

> Fully synthetic. Study, population, dates, endpoints, estimates, and
> deviations are fictional and created only for diagnostic evaluation.

## Snapshot under review

| Field | Snapshot statement | Snapshot locator |
|---|---|---|
| Population | Adults with SYN-condition receiving SYN-101 | Snapshot row 1 |
| Data cutoff | 2026-06-30 | Snapshot row 2 |
| Endpoint | Change from baseline in SYN-score at Week 12 | Snapshot row 3 |
| Analysis set | All randomized participants | Snapshot row 4 |
| Effect estimate | -4.2 points | Snapshot row 5 |
| 95% interval | -6.1 to -2.3 points | Snapshot row 6 |
| Exposure | Median AUC 812 ng·h/mL | Snapshot row 7 |
| Deviations | No material deviations | Snapshot row 8 |
| p-value | `UNKNOWN` | Snapshot row 9 |

## Named source facts

| Source | Field | Source statement | Source locator |
|---|---|---|---|
| Protocol SYN-101 v4.0 | Population | Adults with SYN-condition receiving SYN-101 | §6 |
| Locked output index | Data cutoff | 2026-06-15 | Header |
| SAP SYN-101 v2.0 | Endpoint | Change from baseline in SYN-score at Week 12 | §4.1 |
| SAP SYN-101 v2.0 | Analysis set | Modified intent-to-treat population | §5.2 |
| Locked output T14.2.1 | Effect estimate | -4.2 points | Row 1 |
| Locked output T14.2.1 | 95% interval | -6.1 to -2.3 points | Row 1 |
| Locked PK output T14.2.8 | Exposure | Median AUC 812 ng·h/mL | Row 4 |
| Deviation listing | Deviations | Two prespecified-window deviations remain open | Rows 7 and 11 |

## Diagnostic key

- Mismatch: cutoff 2026-06-30 versus 2026-06-15.
- Mismatch: all randomized participants versus modified intent-to-treat.
- Mismatch: no material deviations versus two open prespecified-window deviations.
- `UNKNOWN`: no p-value source was supplied; do not invent one.
- Clean fields: population, endpoint, effect estimate, interval, and exposure.

The task is source reconciliation only. Clinical meaning, causality,
benefit-risk, disclosure wording, and commitments remain human.
