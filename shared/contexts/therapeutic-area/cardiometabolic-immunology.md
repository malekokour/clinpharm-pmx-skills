# Context — cardiometabolic and immunology

**Dimension:** therapeutic area · **Attaches after selection; never selected**

Two areas in one file because they share the property that most shapes
clinical-pharmacology work here: **large, long, outcome-driven programmes in populations
where the disease itself changes drug disposition.** The specifics differ, so they are
separated below.

---

## Shared consequences

- **Endpoints are distal.** Outcome trials read out in years; the exposure–response the
  clinical pharmacologist can build is usually to a biomarker, and the biomarker-to-
  outcome link is a separate, contestable argument.
- **Chronic dosing** makes accumulation, adherence, and time-varying exposure real
  analysis problems rather than technicalities.
- **Polypharmacy is the norm**, so interaction assessment is high-volume and the
  clinically relevant question is often about a specific concomitant class rather than
  about enzymes in the abstract.
- **Comorbidity is the population**, not an exclusion: renal and hepatic impairment,
  obesity and older age co-occur, and covariate effects correlate with each other.

---

## Cardiometabolic

**Disease alters disposition.** Obesity changes volume of distribution for lipophilic
compounds and complicates weight-based dosing; heart failure alters perfusion, hepatic
clearance and absorption; diabetic nephropathy changes renal elimination over time
within the same patient.

**Body size is a live dosing question** and its answer is empirical: obesity can make
weight-based dosing over-dose or under-dose depending on the compound's distribution.
Which body-size descriptor to use is part of the analysis, not a convention.

**QT is frequently in scope**, and concentration–QTc analysis is often the primary
evidence rather than a thorough QT study.

**Adherence in long trials** produces exposure variability that looks like
pharmacokinetic variability and is not. Where adherence data exist, they belong in the
exposure model.

---

## Immunology

**Inflammation suppresses drug-metabolising enzyme expression.** Two consequences that
are routinely missed:

1. Baseline clearance in an inflamed patient differs from a healthy volunteer, so
   healthy-volunteer PK can under-predict patient exposure.
2. **An effective anti-inflammatory treatment can restore enzyme activity and change
   the clearance of co-administered drugs** — a real, disease-mediated interaction with
   no in-vitro signal. This is the interaction most likely to be absent from a DDI
   package that only assessed direct mechanisms.

**Most agents are biologics**, so `contexts/modality/mab.md` usually attaches too, and
immunogenicity is a central source of exposure variability and loss of response over
time.

**Disease activity is both a covariate and an outcome**, which makes exposure–response
analyses vulnerable to reverse causality: patients doing well may have different
exposure for reasons the model reads backwards.

---

## What this context does not do

It does not decide a dosing strategy for obesity, accept a biomarker-to-outcome
argument, or judge a QT assessment. It names the disease-driven effects on disposition
that a standard framework will not surface on its own.
