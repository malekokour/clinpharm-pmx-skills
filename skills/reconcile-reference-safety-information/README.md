# Reconcile Reference Safety Information

Portable skill for mechanically comparing supplied CCDS, CCSI, RSI, periodic-report,
and regional-label reference safety lists. It preserves divergences for human review;
it never determines a required label or RSI change.

## Included

- `SKILL.md` — installed workflow and human-only boundary.
- `scripts/reconcile_safety_lists.py` — string/list comparison only.
- `assets/Reference-Safety-Reconciliation.template.md` — copyable memo template.
- `references/` — vendored preflight, evidence, human-review, and output-state rules.

Run `python3 scripts/reconcile_safety_lists.py --help` for the optional comparator.
Use the Markdown starter for a degraded no-script route.
