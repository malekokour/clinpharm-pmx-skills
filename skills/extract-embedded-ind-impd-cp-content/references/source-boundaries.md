# Source boundaries for the IND/IMPD inventory

## Accepted locators

| Instrument | Accepted locator | Mechanical use | Recorded caveat |
|---|---|---|---|
| IND | 21 CFR 312.23(a)(8)(i), Pharmacology and Drug Disposition | Locate pharmacological effects/mechanism and ADME disclosures, including an explicit unknown | Accepted research used a 2023 govinfo annual-edition mirror because live eCFR access was blocked; re-check current text before submission-facing use |
| IMPD | Regulation (EU) No 536/2014, Annex I paragraphs 41–48 | Locate Module-4-shaped nonclinical and Module-5-shaped prior-clinical/human-experience summaries | Accepted research used a UK retained-law statutory mirror rather than EUR-Lex; re-check current canonical EU text before EU-facing use |

The accepted research conclusion is narrow: neither instrument names a dedicated
"Clinical Pharmacology" section. Do not invent one. This package checks whether
declared content homes and disclosures can be located in the supplied scope.

## What these locators do not establish

They do not establish that the located science is adequate, that a particular
trial phase is supported, that a filing is complete, or that an agency will accept
it. Those are human regulatory and clinical-pharmacology judgments.

## Currency rule

Record the exact source/version the user directs the review to apply. If current
applicability is not established, emit `NEEDS_INPUT` and preserve the accepted
research caveat. Never silently represent an older mirror as current law.
