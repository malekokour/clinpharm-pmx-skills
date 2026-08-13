# DSUR and Annual Report Coverage Reconciliation

Compare the inclusive dates declared by Development Safety Update Reports
(DSURs) and US IND annual reports. The package flags same-format gaps and
overlaps plus dates shared across formats, always with both document locators.

It does not determine whether a DSUR satisfies 21 CFR 312.33, whether a filing
obligation is met, or whether a safety conclusion is adequate. Those decisions
remain with the accountable regulatory owner and qualified reviewers.

## Inputs

Provide a report inventory with, for each record: report ID, kind, version,
status, inclusive reporting-period start and end, and an exact source locator.
Use synthetic, public, redistributable, or explicitly authorized material only.

## Installed route

Run the standard-library script from the package directory:

```bash
python3 scripts/reconcile_reporting_periods.py --input periods.json --json
```

The result states exact denominators and always surfaces the two build-time
policy questions as `UNKNOWN`. See `SKILL.md` for the complete procedure.

## Markdown route

Use [`PASTE.md`](PASTE.md)
when script execution is unavailable. This route is degraded: calculations are
model-performed and must be shown for human confirmation.

## Evidence

The synthetic suite is diagnostic only. Its expert-key severities are
provisional, no practitioner has adjudicated them, and no model qualification
has run. The package is not registered by this build folder and must not be
described as `released`.

License MIT · version 0.1.0 · collection clinical-pharmacology
