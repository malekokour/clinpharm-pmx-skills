# Workflow — population PK analysis

**Journey:** from an analysis dataset to a pharmacometrics deliverable someone has
signed off. **Documented, not automated.**

## Steps

### 1. Establish the work context

**Skill:** `build-work-context`
Modality, therapeutic area, population, region. This is what decides which contexts
attach to every later step — a rare-disease antibody programme and a small-molecule
oncology programme run this same workflow very differently.

**Carries forward:** the context set.

### 2. Review the analysis plan before the analysis

**Skill:** `review-pk-analysis-plan` *(planned)*
Structural model space, covariate strategy, handling of BLQ and time deviations,
acceptance criteria — agreed before results exist.

**Common failure:** the plan is written after the model is chosen, so the acceptance
criteria are the ones the model happened to meet.

### 3. Confirm the data rules were applied as written

**Skill:** `review-blq-and-time-deviation-rules` *(planned)*
BLQ handling method, actual versus nominal times, exclusions and their reasons.

**Common failure:** exclusions applied during modelling and documented afterwards, which
makes them look like data cleaning rather than analysis decisions.

### 4. Review the model deliverable

**Skill:** `review-model-analysis-deliverable`
Structural model, random effects, covariate selection, and whether the covariate effects
found are supported by the design.

**Carries forward:** the candidate model and its diagnostics.

### 5. Review the diagnostics on their own terms

**Skill:** `review-model-diagnostics` *(planned)*
Goodness-of-fit, shrinkage, predictive checks. Kept separate from step 4 deliberately:
diagnostics assessed by whoever built the model tend to be read generously.

---

## 🔴 Gate — model acceptance

**A qualified pharmacometrician accepts the model, or does not.**

Nothing downstream is valid without this. The workflow supplies the evidence: fit,
diagnostics, covariate support, sensitivity to the debatable choices. It does not
supply the decision.

Ask before accepting: *if the shrinkage were higher, would I still accept this?* and
*which covariate effect would I drop first, and what breaks?*

---

### 6. Assess clinical meaningfulness of the covariate effects

**Skill:** `assess-covariate-clinical-meaningfulness` *(planned, refuse-boundary)*
Prepares the exposure comparison across covariate ranges. **Refuses to declare whether
the difference matters clinically** — that is the gate below.

### 7. Review the model analysis plan and report as a document

**Skill:** `review-model-analysis-plan-and-report` *(planned)*
Whether the report says what the analysis did, whether the plan and report agree, and
whether a reader could reproduce the conclusion.

### 8. Sign-off review

**Skill:** `review-pharmacometrics-deliverable` *(planned)*
The final pass before the deliverable leaves the function.

---

## 🔴 Gate — sign-off

**A qualified human signs. The workflow never does.**

---

## Where this connects

The accepted model feeds `prepare-dose-justification-evidence`, the exposure–response
skills, and eventually the CTD 2.7.2 content. **Cross-document consistency is not
automatic** — `reconcile-cross-document-facts` exists because parameter values drift
between the model report and every document that quotes it.

## Contexts that change this workflow most

`rare-disease` — sparse data makes model-based evidence primary rather than
supporting · `mab` — target-mediated disposition and immunogenicity as a covariate ·
`oncology` — dropout is informative and confounds exposure with prognosis.
