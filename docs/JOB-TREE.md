# Job tree (navigation spine)

ClinPharm PMx Skills skills map to **L3 tasks**. Folders below are discovery paths
(`nav_path`), not skills. Package bodies currently live at `skills/<id>/`; the
router uses [`../catalog/nav_registry.json`](../catalog/nav_registry.json).

## Clinical pharmacology (active)

| nav_path | Example skills |
|---|---|
| `documents/csr` | review-csr-pk-consistency |
| `documents/protocol` | review-protocol-pk-sections |
| `documents/bioanalytical` | review-bioanalytical-report |
| `documents/ctd/2-7-2` | review-ctd-272-content |
| `documents/cross-document` | reconcile-cross-document-facts |
| `documents/ind-impd` | extract-embedded-ind-impd-cp-content |
| `documents/investigators-brochure` | check-investigators-brochure-pk-section |
| `documents/dsur` | reconcile-dsur-annual-report-coverage |
| `agency/briefing` | prepare-briefing-package-content |
| `agency/information-request` | map-agency-question-evidence |
| `studies/characterisation/ddi` | review-ddi-evidence |
| `studies/analysis/nca` | verify-nca-outputs |
| `studies/analysis/pharmacometrics` | review-model-analysis-deliverable |
| `studies/conduct` | review-study-conduct-pk |
| `dose-regimen/justification` | prepare-dose-justification-evidence |
| `translation/fih/dose-rationale` | review-fih-dose-rationale |
| `labelling/uspi` | review-uspi-section-12-content |
| `programme/development-plan` | assess-development-plan-gaps |
| `safety/benefit-risk` | structure-benefit-risk-effects-table |
| `safety/reference-safety` | reconcile-reference-safety-information |

## Pharmacometrics (Next / co-equal track)

Public Next: deepen PMx collection, modules, and skills. Today the strongest
PMx-facing package is `review-model-analysis-deliverable` under
`studies/analysis/pharmacometrics`.

## Utilities

| nav_path | Skill |
|---|---|
| `work-context` | build-work-context (`released`) |
| `library` | library-router (`built` scaffold) |

Regenerate tallies from collections before quoting readiness.
