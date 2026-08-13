# Workflow — US prescribing information set

**Journey:** sections 2, 7, 8 and 12 reviewed as one story rather than four documents.
**Documented, not automated.**

Label sections are written by different people at different times and read by a
prescriber in one sitting. The failure this workflow targets is a label that is
internally correct section by section and incoherent as a whole.

## Steps

### 1. Establish the work context

**Skill:** `build-work-context`
Region matters more here than in most workflows: the same evidence produces different
label text in different jurisdictions, and this workflow is the US one.

### 2. Section 12 — clinical pharmacology

**Skill:** `review-uspi-section-12-content`
Start here, not at section 2. Section 12 is where the evidence lives; the others are
consequences of it.

**Carries forward:** every parameter and every population statement. Sections 2, 7 and 8
must not assert anything section 12 does not support.

### 3. Section 7 — drug interactions

**Skill:** `review-uspi-section-7-interactions` *(planned)*
Which interactions are stated, which are omitted, and whether the management advice
follows from the magnitude.

**Common failure:** an interaction described in 12.3 with no corresponding entry in
section 7, or a section 7 entry with no evidence in 12.3.

### 4. Section 8 — specific populations

**Skill:** `review-uspi-section-8-populations` *(planned)*
Renal, hepatic, age, sex, pregnancy, lactation, paediatric. Including the populations
where the correct statement is that no dedicated study was done and why.

### 5. Section 2 — dosage and administration

**Skill:** `review-uspi-section-2-dosing` *(planned)*
Every dose adjustment in section 2 traced to the evidence in 8 or 12 that justifies it.

**Common failure:** section 2 carries a renal adjustment that section 8 does not support,
or section 8 describes an exposure change that section 2 silently ignores.

### 6. Cross-section reconciliation

**Skill:** `reconcile-cross-document-facts`
Numbers, populations and directions checked across all four sections plus their sources.

---

## 🔴 Gate — label content approval

**Regulatory and clinical sign-off. The workflow prepares; it does not approve label
text.**

---

### 7. Negotiation with the agency

**Skill:** `prepare-label-negotiation-evidence` *(planned, refuse-boundary)*
Assembles the evidence and precedent for a contested section. **Refuses to negotiate** —
that is a person in a meeting.

### 8. Post-approval updates

**Skill:** `review-post-approval-label-update` *(planned)*
The same coherence check, applied to a change rather than a first version. New evidence
arrives against a label that already exists, and the risk is a change that fixes one
section and desynchronises three.

---

## The coherence checks worth running by hand

- Every dose adjustment in section 2 has evidence in 8 or 12.
- Every interaction in 7 has a magnitude in 12.3.
- Every population in 8 either has data or says it does not.
- No parameter appears with different values in two sections.
- The dosing basis in section 2 matches the exposure–response in 12.

## Contexts that change this workflow most

`mab` — section 8 renal and hepatic statements usually say the impairment is not a
dosing driver, and must say *why* · `oncology` — section 2 dose modification schemes are
long and must reconcile with the exposure–safety evidence · `adc` — section 12 must be
explicit about which analyte each parameter describes.
