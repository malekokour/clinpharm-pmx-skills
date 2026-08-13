# Evaluation suite — reconcile-reference-safety-information

Ten synthetic cases cover declared activation, a named-neighbour near miss, missing
input, restricted data, prompt injection, refusal of a required-change determination,
degraded Markdown use, clean install, currency/change-record ambiguity, and an
execution fixture.

The execution fixture contains five deliberately planted list/version divergences.
Their presence is certain; their severities are **provisional**, not practitioner-
adjudicated. This suite provides diagnostic build evidence only and cannot promote the
package or prove clinical validation.

Run schema checks with `.venv/bin/python scripts/eval_suite_check.py`. The optional
script check is `python3 ../../skills/reconcile-reference-safety-information/scripts/reconcile_safety_lists.py --left fixtures/synthetic-ccsi-v3.md --right fixtures/synthetic-regional-label.md`.
