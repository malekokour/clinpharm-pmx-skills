# Clinical Pharmacology dependency map

What each skill consumes, what it shares, and where two skills could be confused
for one another.

## Shared components and their consumers

A shared component has exactly one canonical source under `shared/`. It is
vendored into each released package at build time so that an installed skill
stays self-contained, and a freshness check proves the vendored copy still
matches its source.

| Shared component | Canonical source | Consumed by (released) | Consumed by (planned) |
|---|---|---|---|
| Safety and permitted-source preflight | `shared/policies/source-preflight.md` | `review-csr-pk-consistency` | every skill |
| Evidence hierarchy and source locators | `shared/policies/evidence-hierarchy.md` | `review-csr-pk-consistency` | every skill |
| Contradiction-preserving claim ledger | `shared/policies/contradiction-ledger.md` | `review-csr-pk-consistency` | `reconcile-cross-document-facts`, `review-ddi-evidence` |
| Output-state markers (`UNKNOWN` / `NEEDS_INPUT` / `CANNOT_ASSESS`) | `shared/policies/output-states.md` | `review-csr-pk-consistency` | every skill |
| Human-review and prepare-only boundary | `shared/policies/human-review.md` | `review-csr-pk-consistency` | every skill |
| PK parameter plausibility and unit checks | `shared/scripts/pk_plausibility.py` | `review-csr-pk-consistency` | `verify-nca-outputs`, `review-study-conduct-pk` |
| Cross-document numeric consistency | `shared/scripts/cross_document_consistency.py` | `review-csr-pk-consistency` (document mode) | `reconcile-cross-document-facts` (programme mode) |
| Ratio-statistic recomputation | `shared/scripts/ratio_statistics.py` | `review-csr-pk-consistency` | `verify-nca-outputs` |

**Single-source rule.** The reconciliation engine exists only in
`shared/scripts/cross_document_consistency.py`. `review-csr-pk-consistency` calls
it in document mode; `reconcile-cross-document-facts` will call the same engine
in programme mode. Neither re-implements it. The same rule holds for the
plausibility rules, which live only in `shared/scripts/pk_plausibility.py`.

## Study-type modules and their consumers

Study types are reference content, not skills. The workflow skeleton is the
same across study types; only the criteria, design conventions and expected
statements change.

| Module | Canonical source | Status | Consumed by |
|---|---|---|---|
| SAD/MAD ascending dose | `shared/references/sad-mad.md` | built | `review-csr-pk-consistency` |
| Food effect | `shared/references/food-effect.md` | built | `review-csr-pk-consistency` |
| DDI · renal · hepatic · BA/BE · dose proportionality · QT · oncology dose optimisation · immunogenicity · ADC | — | backlog | promoted only with its own planted-defect fixture |

**Why only two modules ship.** A module without its own planted-defect fixture
cannot be evaluated, and shipping an unevaluated module would repeat exactly the
unevidenced-claim failure this library exists to correct. Each backlog module
promotes when its fixture exists.

## Activation boundaries

Adjacent review skills are the library's main architectural risk: a user's
natural phrasing may not distinguish them. Each pair below requires a passing
activation-accuracy test before the second member of the pair is released.

| Pair | Why they can be confused | Separation |
|---|---|---|
| `review-csr-pk-consistency` ↔ `review-protocol-pk-sections` | Both are "review the PK part of a document" requests | Object and lifecycle stage: a completed study's report versus a pre-execution protocol. Trigger examples in each `SKILL.md` use the wording users actually emit. |
| `review-csr-pk-consistency` ↔ `verify-nca-outputs` | Both check PK numbers | Source of truth: the report reconciled *against* NCA outputs, versus the NCA outputs themselves verified as derivations |
| `review-bioanalytical-report` ↔ `verify-nca-outputs` | Adjacent artefacts in the same analysis chain | Assay method and validation content versus derived parameter correctness |
| `review-csr-pk-consistency` ↔ `reconcile-cross-document-facts` | Both reconcile values across documents | Scope: one study report and its own sources, versus the programme document spine across studies |

Target: at least 90% correct activation against fixture and decoy prompts before
release of any skill in a pair.

## What is deliberately not a skill

Shared contracts, deterministic tools, study-type modules and evaluation
fixtures are dependencies. They are not marketed as skills, because none of them
produces an independently valuable professional outcome on its own.
