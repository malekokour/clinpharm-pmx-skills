# Workflow — organ impairment programme

**Journey:** renal, hepatic and dialysis assessed as one decision set rather than three
separate studies. **Documented, not automated.**

These are usually run and reported independently, and then the label has to state a
coherent position across all of them. This workflow exists because the coherence is
where the defects are.

## Steps

### 1. Establish the work context

**Skill:** `build-work-context`
Modality decides how much of this applies. For an antibody, renal impairment is usually
not a dosing driver — and saying *why* is the deliverable, not omitting the section.

### 2. Establish the disposition basis

**Skill:** `review-adme-and-elimination-routes` *(planned)*
**Reference:** `shared/references/protein-binding-distribution.md`

The fraction eliminated renally and hepatically is what makes the impairment studies
predictable — or makes them necessary. Doing the studies without this is how a programme
runs a dedicated study it could have modelled.

**Carries forward:** the elimination split and the protein-binding picture.

### 3. Renal impairment

**Skill:** `review-renal-impairment-study` *(planned, wraps `renal_staging.py`)*
**Reference:** `shared/references/renal-impairment.md`

Staging basis, the equation used, and whether the categories reported match the ones the
label will use.

**Common failure:** the study stages by one equation and the label by another, so the
categories do not correspond.

### 4. Hepatic impairment

**Skill:** `review-hepatic-impairment-study` *(planned)*
**Reference:** `shared/references/hepatic-impairment.md`

Child-Pugh categories, and — because hepatic disease changes binding — whether total or
free exposure is being compared.

### 5. Dialysis and organ replacement

**Skill:** `review-dialysis-impact` *(planned)*
Whether the compound is dialysable, and what that means for timing relative to a
session. Often the section with the least data and the most confident label text.

### 6. Model-based extension

**Skill:** `predict-organ-impairment-by-model` *(planned)*
Where a category was not studied, the model that covers it and its qualification.

---

## 🔴 Gate — dose adjustment

**A qualified human decides whether an exposure change warrants a dose adjustment, and
what adjustment.**

The workflow supplies exposure by category with intervals, the free-versus-total
picture, the exposure–response context, and which categories were not studied. It
refuses to recommend the adjustment.

---

### 7. Label statements

**Skills:** `review-uspi-section-8-populations` *(planned)* ·
`review-uspi-section-2-dosing` *(planned)*
Section 8 states the exposure findings; section 2 states any adjustment. They must agree.

### 8. Cross-document reconciliation

**Skill:** `reconcile-cross-document-facts`

---

## The coherence checks

- Renal and hepatic categories in the label match the categories the studies used.
- Every category with a dose adjustment has data or a qualified model behind it.
- Every category **without** data says so, rather than being silently absent.
- Where binding changes, total and free exposure are not compared to each other.
- The dialysis statement is supported by something other than plausibility.

## Contexts that change this workflow most

`mab` — renal impairment usually not a driver; hepatic reasoning does not transfer from
small molecules · `oligonucleotide` — renal is *the* population question, since renal
elimination is a principal route · `adc` — the payload may be hepatically cleared even
when the antibody is not · `cardiometabolic-immunology` — impairment is comorbid and
correlated with other covariates rather than isolated.
