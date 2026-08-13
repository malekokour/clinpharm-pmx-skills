# SYNTHETIC — periodic-report source notes

> Fully synthetic. The report identifiers, versions, statuses, dates, and
> locators in this fixture do not represent a real product, IND, sponsor, or
> filing history.

## Inventory denominator

Seven report records were supplied. Five have parseable inclusive dates and
non-empty locators. Two are deliberately not assessable:

- `BROKEN-LOCATOR` has no exact source locator.
- `BAD-RANGE` states a start date after its end date.

Neither record may disappear from the output or be counted as clean.

## Deliberate period patterns

- `DSUR-2025-A` ends on **2025-03-31** and `DSUR-2026-A` starts on
  **2025-04-03**. The inclusive gap is 2025-04-01 through 2025-04-02.
- `DSUR-2026-A` ends on **2026-03-31** and `DSUR-2027-A` starts on
  **2026-03-30**. The inclusive overlap is 2026-03-30 through 2026-03-31.
- `IND-AR-2025-A` and `IND-AR-2025-B` both declare 2024-06-15 through
  2025-06-14.
- Each of the two IND annual-report records overlaps `DSUR-2025-A` from
  2024-06-15 through 2025-03-31 and `DSUR-2026-A` from 2025-04-03 through
  2025-06-14.

## Preserved source states

`UNKNOWN_FINAL_RULE_STATUS` and `UNKNOWN_DSUR_IN_LIEU_PRACTICE` remain
`UNKNOWN`. The fixture provides no current primary authority and no
application-specific filing record. Date coverage cannot resolve either one.

## Human boundary

The clinical pharmacologist and regulatory safety reviewer adjudicate period
findings. The accountable regulatory owner determines filing obligations.
Every disposition starts and remains `open` in automated output.
