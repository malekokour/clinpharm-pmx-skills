# Evaluation suite — structure-benefit-risk-effects-table

Ten synthetic cases cover declared activation, near miss, missing input, restricted
data, prompt injection, refusal of benefit-risk conclusions, degraded Markdown use,
clean install, source currency, and an execution fixture.

The execution fixture contains five deliberately planted structural defects. Their
presence is certain; their severities are **provisional**, not practitioner-adjudicated.
This suite therefore provides diagnostic build evidence only and cannot promote the
package or prove clinical validation.

Run schema checks with `.venv/bin/python scripts/eval_suite_check.py`. The optional
script check is `python3 ../../skills/structure-benefit-risk-effects-table/scripts/validate_effects_table.py --input fixtures/synthetic-effects-table-draft.md`.
