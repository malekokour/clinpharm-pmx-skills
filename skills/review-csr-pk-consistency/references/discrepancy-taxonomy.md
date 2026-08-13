# Discrepancy taxonomy

Every register row carries exactly one class and one severity.

## Classes

| Class | Definition | Typical detection |
|---|---|---|
| `numeric-mismatch` | The same quantity differs between two locations beyond the applied tolerance | script |
| `contradiction` | Two statements cannot both be true — a reversed direction, an incompatible claim | script + model |
| `unsupported-claim` | A statement with no supporting analysis in the supplied sources | model |
| `unit-inconsistency` | A unit that conflicts with the analysis plan convention or the parameter class | script |
| `plausibility-violation` | An arithmetic relation between reported values does not hold | script |
| `stale-version` | A value reflecting a superseded document version | script, against I8 |
| `completeness-gap` | A required element is absent | script + model |
| `presentation` | Formatting, citation hygiene, rounding display | script + model |

## Severity — calibrated to downstream propagation

The cost function is a wrong number reaching a Module 2.7 summary, a label, or an
agency answer. It is **not** how visible the error looks on the page.

| Severity | Test | Examples |
|---|---|---|
| **Critical** | Would change a numeric result or the direction of a conclusion that reaches a downstream document | Synopsis value differs from its source table · unit swap · reversed food-effect direction · point estimate outside its own CI |
| **Major** | Would mislead a careful reader without changing the headline result | Unsupported qualifier · value from a superseded amendment · accumulation inconsistent with reported half-life |
| **Minor** | Presentation and citation hygiene | Rounding displayed inconsistently with the plan's rule · superseded citation version · figure axis label |

## Detection path

Recorded per finding, because per-path recall must be reported separately:

- `script` — deterministic. A miss here is a script bug, not model variance.
- `script+model` — script locates, model classifies.
- `model` — semantic; no deterministic surface exists.

## The line this taxonomy does not cross

A class and a severity describe **what kind of mismatch exists and how far it
could travel**. Neither says which value is correct, whether the difference
matters scientifically, or what should be done. Those are reviewer decisions.
