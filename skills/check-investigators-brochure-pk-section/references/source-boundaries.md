# Source boundaries for the IB PK-section check

## Accepted locators

| Source | Accepted locator | Mechanical use | Boundary |
|---|---|---|---|
| ICH E6(R2) | Sections 7.3.6–7.3.7; Appendix 2 example table of contents | Inventory human PK/product metabolism and related effects-in-humans declarations | Apply only to the source/version declared for the review; re-check current applicability before qualification or regulated use |
| ICH E2F | Section 2.6 and the supplied DSUR citation locator | Compare the DSUR-cited IB version/date with the supplied current-IB register | A mismatch is not a filing-obligation or medical-approval decision |

The accepted E6(R2) research inventory includes absorption, plasma protein
binding, distribution, elimination, bioavailability, and related PD/safety/
efficacy/dose-response content. It supports a presence/location checklist only.

## Version ownership

This package deliberately does not declare which IB is current. The user supplies
one version register for the run. If its owner, version, date, or locator is
missing, emit `NEEDS_INPUT`; do not choose the newest-looking file.

## What the sources do not establish

They do not establish that the medical content is adequate or approved, that a
study should proceed, that a dose is supported, or that a DSUR/annual-report
obligation is satisfied.
