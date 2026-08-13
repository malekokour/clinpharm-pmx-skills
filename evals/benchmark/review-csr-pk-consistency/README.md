# Benchmark — CSR PK Consistency Review

## Status

**Fixture built; scored runs not yet executed.** No performance figure is
published, and none may be quoted until three archived runs exist.

Current catalog `evidence_level` reads
`evaluation-retracted-pending-requalification`: the earlier evaluation claim was
retracted, and a fixture existing is not the same as a qualification having been
run and accepted.

## What is measured

Against a fully synthetic CSR with expert-keyed planted defects spanning every
finding class and all three detection paths.

| Metric | Definition | Target |
|---|---|---|
| Unweighted defect recall | detected / planted | ≥ 0.90 |
| Severity-weighted recall | Σ(weight × detected)/Σ(weight); Critical 5, Major 3, Minor 1 | ≥ 0.95 |
| Critical-defect recall | detected Critical / planted Critical, **per run** | 1.00 every run |
| Precision | true flags / all register rows | ≥ 0.85 |
| Location-citation accuracy | findings with a resolvable locator | ≥ 0.95 |
| Script-path recall | script-detectable subset found by scripts | **1.00** — any miss is a script bug, not model variance |
| Severity agreement | exact match against the expert key | ≥ 80% exact; 100% within one class |
| Activation accuracy | routed here vs `review-protocol-pk-sections` / `verify-nca-outputs` | ≥ 90% |
| Reproducibility | 3 independent runs, archived | no Critical miss in any run; weighted-recall spread ≤ 0.03 |

## Why recall is targeted above precision

A QC tool that misses a Critical mismatch has failed at its only job. A false
positive costs a reviewer minutes. The documented failure consequence is
**propagation** of a wrong value into a summary or a label — not alarm fatigue.

## What this benchmark is not

Not clinical validation. Not a GxP qualification. Not evidence of real-world
performance. It measures detection of *planted* defects in a *synthetic*
document, and every published figure must state its task, model, host, date and
run count.
