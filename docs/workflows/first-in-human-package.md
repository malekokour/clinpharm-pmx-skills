# Workflow — first-in-human package

**Journey:** from the nonclinical package to a starting dose, an escalation schema and
stopping rules that a safety committee can defend. **Documented, not automated.**

This is the workflow with the highest consequence for being wrong, and the one where the
gates matter most. Every step below prepares evidence. **No step selects the dose.**

## Steps

### 1. Establish the work context

**Skill:** `build-work-context`
Modality dominates here more than anywhere else. A first-in-human package for a
monoclonal antibody, a cell therapy and a small molecule share almost nothing beyond the
question being asked.

### 2. Synthesise the nonclinical package for human readiness

**Skill:** `synthesise-nonclinical-for-human-readiness` *(planned)*
Species, exposures, NOAEL determinations, target-organ findings, and — critically —
what was **not** studied.

**Common failure:** the synthesis reports what the studies found and omits which
questions no study addressed.

### 3. Predict human pharmacokinetics

**Skill:** `review-human-pk-prediction`
Allometry, in-vitro to in-vivo extrapolation, physiologically-based modelling. The
prediction and its uncertainty, not the prediction alone.

**Carries forward:** predicted exposure at candidate doses, with intervals.

### 4. Derive the NOAEL-based starting dose

**Skill:** `derive-noael-hed-mrsd` *(planned, wraps `mrsd_calculator.py`)*
NOAEL to human equivalent dose to maximum recommended starting dose, with the safety
factor stated and justified rather than defaulted.

### 5. Derive the pharmacology-based starting dose

**Skill:** `review-fih-dose-rationale`
MABEL and the pharmacologically active dose, from receptor occupancy or a mechanistic
model.

**The two candidate doses from steps 4 and 5 will differ.** Which governs is a judgment,
and for agents with immune-agonist or high-potency mechanisms the pharmacology-based
figure normally does. Both are carried forward; neither is chosen here.

### 6. Establish safety margins

**Skill:** `assess-safety-margins-vs-tox` *(planned)*
Predicted human exposure against toxicology exposures at the relevant endpoints, for
every candidate dose.

---

## 🔴 Gate — starting dose

**A qualified human selects the starting dose.**

The workflow lays out: both candidate derivations, their assumptions, predicted exposure
with uncertainty, safety margins, and what is unknown. It states which derivation it
believes governs and why. **It does not choose.**

This gate is not a formality. If the two derivations disagree by an order of magnitude,
that disagreement is the most important output of the whole workflow.

---

### 7. Design the escalation schema

**Skill:** `review-escalation-schema` *(planned)*
Increments, sentinel dosing, staggering, cohort review points, and what triggers a
pause.

### 8. Set the exposure cap and stopping rules

**Skill:** `define-exposure-cap-and-stopping-rules` *(planned)*
The exposure that must not be exceeded regardless of tolerability, and the events that
stop escalation.

### 9. Sentinel dosing and subject-safety design

**Skill:** `review-sentinel-dosing-design` *(planned)*
Interval between first and subsequent subjects, observation windows, site readiness.

### 10. Assemble the safety-committee package

**Skill:** `prepare-escalation-committee-package` *(planned)*
What the committee sees at each decision point, and whether it is enough to decide with.

---

## 🔴 Gate — protocol and committee approval

**Ethics committee and safety committee approve. Neither is a step this workflow can
take.**

---

## What this workflow refuses, throughout

It does not select a dose, declare a margin adequate, judge a nonclinical package
sufficient, or approve an escalation step. Every one of those is a decision with a named
accountable human, and the skills involved are built to prepare them and stop.

## Contexts that change this workflow most

`mab` — MABEL usually governs; immunogenicity affects the escalation assumptions ·
`cell-gene` — conventional NOAEL-to-HED scaling does not apply and the vocabulary
changes entirely · `oncology` — patient rather than healthy-volunteer first-in-human
changes the whole risk calculus · `rare-disease` — the escalation population may be the
treatment population.
