# Workflow — drug interaction programme

**Journey:** in-vitro characterisation through clinical confirmation to management
strategy and label text. **Documented, not automated.**

## Steps

### 1. Establish the work context

**Skill:** `build-work-context`
Modality decides whether most of this workflow applies at all. For a monoclonal
antibody the enzyme and transporter framework largely does not, and the correct output
is to say which mechanisms were assessed and found inapplicable — not "no DDI expected".

### 2. In-vitro package

**Skill:** `review-in-vitro-ddi-package` *(planned)*
Reaction phenotyping, inhibition (reversible and time-dependent), induction, transporter
substrate and inhibitor assessment.

**Reference:** `shared/references/enzyme-transporter-biology.md`

**Carries forward:** which signals crossed a decision threshold, and against which
version of which threshold.

**Common failure:** fraction metabolised attributed almost entirely to one enzyme with
the unassigned remainder never stated.

### 3. Model-based prediction

**Skill:** `predict-ddi-by-model` *(planned)*
Where a mechanistic model replaces a clinical study, the model, its assumptions, and its
qualification for that use.

### 4. Clinical studies

**Skill:** `review-clinical-ddi-study` *(planned)*
Design, perpetrator and victim roles, the exposure change observed with its interval.

### 5. Food effect and gastric pH

**Skill:** `review-food-effect-and-ara` *(planned)*
**Reference:** `shared/references/food-effect.md`
Frequently omitted from the DDI programme because it is filed under biopharmaceutics,
and then missing from the interaction story.

### 6. Management strategy

**Skill:** `review-ddi-evidence`
Every signal carried to a terminus: a study, a model-based conclusion, a label
statement, or a documented reason it needs none.

---

## 🔴 Gate — clinical significance

**A qualified human decides whether an exposure change matters clinically.**

The workflow supplies the magnitude, the interval, the exposure–response context, and
the comparator. It refuses to convert a fold-change into a recommendation. Every skill
in this chain carries that refusal explicitly.

---

### 7. Label text

**Skill:** `review-uspi-section-7-interactions` *(planned)*
Whether section 7 matches what section 12.3 supports, in both directions.

---

## The completeness question this workflow answers

**Not** "were any interactions found?" but **"which mechanisms were assessed, which were
not, and why?"** A programme reporting no interactions without that list has an
incomplete package, not a negative result — and the two read identically in a summary.

## The check worth running by hand

Every enzyme or transporter named anywhere in the label appears in the in-vitro package.
Every in-vitro signal above threshold has a terminus. Neither direction is automatic.

## Contexts that change this workflow most

`mab` — the replacement question is cytokine-mediated suppression of enzyme expression,
a real mechanism with no in-vitro signal · `adc` — the antibody and the payload need
separate assessments, and the payload usually carries the liability ·
`cardiometabolic-immunology` — an effective anti-inflammatory can *restore* enzyme
activity and change a co-medication's exposure · `oligonucleotide` — low CYP liability,
but say which mechanisms were checked.
