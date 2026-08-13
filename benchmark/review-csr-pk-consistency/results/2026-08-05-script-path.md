# Script-path benchmark — 2026-08-05

**Deterministic. Reproducible by running the tools against the fixture; no model
involved, so there is no run-to-run variance to average.**

## Result

| Metric | Value | Target | |
|---|---|---|---|
| Script-path recall | **6 / 6 = 1.00** | 1.00 | ✅ |
| False positives on the documented traps | **0 / 5** | 0 | ✅ |

| Defect | Class | Sev | Detected by |
|---|---|---|---|
| D1 AUC 412 vs 481 | numeric-mismatch | Critical | T05 reconcile |
| D2 t½ 8.2 vs 11.4 | numeric-mismatch | Major | T05 reconcile |
| D3 accumulation vs half-life | plausibility-violation | Major | T03 accumulation |
| D4 CL in mL/h against a plan declaring L/h | unit-contradicts-analysis-plan | Critical | T03 unit |
| D7 Tmax 2.0 vs 3.5 | numeric-mismatch | Major | T05 reconcile |
| D8 slope 3 s.f. beside CI at 2 s.f. | presentation | Minor | T03 significant figures |

Trap 1 (correct `L/h` in cohorts 1, 2, 4) was **not** flagged.

## What this does not measure

The model path. D5, D6, D9, D10, D11 and D12 require a model executing the
`SKILL.md` workflow, and the then-planned three-run reproducibility requirement
was unmet.
**No aggregate recall, precision, or severity-agreement figure may be quoted
from this file.** At the time of this 2026-08-05 record, catalog
`evidence_level` was `synthetic-benchmark-pending-run`; current catalog authority
may supersede that historical label.

## Four defects this measurement found in the tools themselves

Recall was **0.50** on the first honest measurement. Every gap below passed code
review and unit tests, and was invisible until the tools ran against a document.

| # | Defect | Effect | Fix |
|---|---|---|---|
| 1 | Reconciliation keyed on raw surrounding text | Prose and table rows never compared — 27 values extracted, 1 comparison | Key on an identified parameter |
| 2 | Label match scored by earliest position | `"ratio"` beat `"accumulation ratio"`; food-effect GMRs reconciled against an accumulation ratio | End-position + longest-alias tie-break |
| 3 | Context window 48 characters | In prose the parameter label sits ~50 characters before its value, so **D1 was missed entirely** | Widened to 140 |
| 4 | Unit checked against a class vocabulary only | `mL/h` is a *valid* clearance unit, so **D4 passed** despite contradicting the plan's declared `L/h` | Check the study's declared convention first |

Defects 3 and 4 are the instructive pair: each produced a **confident clean
result** on a document containing a planted Critical defect. A tool that reports
success while missing the thing it exists to find is worse than no tool, and
neither was reachable by inspection.

## Reproduce

```bash
python3 skills/review-csr-pk-consistency/scripts/reconcile.py \
  --left  evals/review-csr-pk-consistency/fixtures/synthetic-csr-synopsis.md \
  --right evals/review-csr-pk-consistency/fixtures/synthetic-nca-output.md \
  --left-name CSR --left-version 3.0 --left-locator "Synopsis §2.3" \
  --right-name NCA --right-version 2.0 --right-locator "NCA output"
```

Expert key: `evals/review-csr-pk-consistency/fixtures/EXPERT-KEY.md`.

## Limitations

Synthetic document · one fixture · deterministic path only · no model runs · no
practitioner review of fixture realism. **Not clinical validation. Not a GxP
qualification. Not evidence of real-world performance.**
