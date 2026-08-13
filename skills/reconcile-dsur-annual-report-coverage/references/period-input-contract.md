# Reporting-period input contract

Load this reference when preparing structured input for the deterministic
period checker.

```json
{
  "as_of_date": "2026-08-11",
  "documents": [
    {
      "id": "DSUR-2025",
      "kind": "DSUR",
      "version": "v1.0",
      "status": "final",
      "period_start": "2024-04-01",
      "period_end": "2025-03-31",
      "locator": "DSUR-2025 title page, reporting period"
    }
  ]
}
```

## Rules

- `documents` must be a non-empty list.
- `id` must be unique and non-empty.
- `kind` must be `DSUR` or `IND_ANNUAL_REPORT`.
- `period_start` and `period_end` must be ISO calendar dates and are inclusive.
- `locator` must identify where both dates were read.
- `version` and `status` are preserved as provenance but do not change the date
  arithmetic.
- `as_of_date` is provenance only. It is never used to infer regulatory status.

Missing or malformed records are reported under `unassessable`; they are not
discarded and are not counted as clean coverage.
