---
asset: guidance-index
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-05"
consumers: [all skills, all study-type modules]
---

# Guidance index

The single source for regulatory anchors. A skill or module cites **this file**,
never its own copy of a date.

## How to read a row

- **Status** is `final` or `draft`. A draft is never cited as a requirement.
- **Date** is the issuing body's own stated publication or revision date.
- **Verified** is when that was last checked against the issuing body's page.

## The verification rule that produced this file

Every anchor here was checked against the **issuing body's own page**, not a
secondary compilation. That is not pedantry — three anchors below were wrong in
the source research, and all three were wrong in a way that would have shipped:

| Anchor | Research said | Actually |
|---|---|---|
| Food effect | June 2022; a possible May 2026 Rev 1 rests on "one low-authority source" | **Revision 1 issued May 2026** and substantive |
| Acid-reducing agents | "remains a November 2020 draft, finalization unconfirmed" | **Final since 2023-03-13**, over three years |
| MaPP 4000.4 | "current revision unverified" | **Rev 1, September 2016** |

Two of three would have caused a module to cite superseded criteria.

## FDA — clinical pharmacology

| ID | Title | Status | Date | Verified |
|---|---|---|---|---|
| `fda-food-effect` | Assessing the Effects of Food on Drugs in INDs and NDAs — Clinical Pharmacology Considerations, **Revision 1** | final | 2026-05 | 2026-08-05 |
| `fda-ara-gastric-ph` | Evaluation of Gastric pH-Dependent Drug Interactions With Acid-Reducing Agents: Study Design, Data Analysis, and Clinical Implications | final | 2023-03-13 | 2026-08-05 |
| `fda-renal` | Pharmacokinetics in Patients with Impaired Renal Function — Study Design, Data Analysis, and Impact on Dosing and Labeling | final | 2024-03 | research-sourced |
| `fda-mass-balance` | Clinical Pharmacology Considerations for Human Radiolabeled Mass Balance Studies | final | 2024-07 | research-sourced |
| `fda-mrsd` | Estimating the Maximum Safe Starting Dose in Initial Clinical Trials for Therapeutics in Adult Healthy Volunteers | final | 2005-07 | research-sourced |
| `fda-exposure-response` | Exposure–Response Relationships — Study Design, Data Analysis, and Regulatory Applications | final | 2003-04 | research-sourced |
| `fda-poppk` | Population Pharmacokinetics | final | 2022-02 | research-sourced |
| `fda-pbpk` | Physiologically Based Pharmacokinetic Analyses — Format and Content | final | 2018-08 | research-sourced |
| `fda-optimus` | Optimizing the Dosage of Human Prescription Drugs and Biological Products for the Treatment of Oncologic Diseases | final | 2024-08 | research-sourced |
| `fda-adc` | Clinical Pharmacology Considerations for Antibody-Drug Conjugates | final | 2024-03 | research-sourced |
| `fda-labeling-cp` | Clinical Pharmacology Section of Labeling for Human Prescription Drug and Biological Products — Content and Format | final | 2016-12 | research-sourced |
| `fda-bioanalytical` | Bioanalytical Method Validation | final | 2018-05 | research-sourced |
| `mapp-4000-4` | MAPP 4000.4 Rev 1 — Good Review Practices: Clinical Pharmacology Review of NME NDAs and Original BLAs | current | 2016-09 | 2026-08-05 |

## ICH

| ID | Title | Status | Date | Verified |
|---|---|---|---|---|
| `ich-e3` | Structure and Content of Clinical Study Reports | final | 1995-11 | research-sourced |
| `ich-e4` | Dose-Response Information to Support Drug Registration | final | 1994-03 | research-sourced |
| `ich-e11a` | Pediatric Extrapolation | Step 4 | 2024-08-21 | research-sourced |
| `ich-e14-s7b` | E14/S7B Clinical and Nonclinical Evaluation of QT/QTc — Q&As | final | 2022-02 | research-sourced |
| `ich-m4e-r2` | CTD Efficacy — including the five-part 2.7.2 structure | final | 2016-06 | research-sourced |
| `ich-m10` | Bioanalytical Method Validation and Study Sample Analysis | Step 4 | 2022-05 | research-sourced |
| `ich-m12` | Drug Interaction Studies | Step 4 | 2024-05 | research-sourced |
| `ich-m15` | General Principles for Model-Informed Drug Development | Step 4 | 2026-01 | research-sourced |

## EMA

| ID | Title | Status | Date | Verified |
|---|---|---|---|---|
| `ema-fih` | Strategies to Identify and Mitigate Risks for First-in-Human and Early Clinical Trials, Rev 1 | final | 2017-07 | research-sourced |
| `ema-immunogenicity` | Immunogenicity Assessment of Therapeutic Proteins | final | 2017-05 | research-sourced |

## US regulation

| ID | Citation | Subject |
|---|---|---|
| `cfr-201-57-c-13` | 21 CFR 201.57(c)(13) | Required Clinical Pharmacology labelling content |

## Maintenance

1. `research-sourced` rows inherit their date from the Clinical Pharmacology
   research package and have **not** been independently re-verified. Any skill
   that depends on one must verify it in pipeline stage 1 before its module
   freezes, and update the `Verified` column.
2. Never cite a draft as a requirement. State it as a draft with its date.
3. A guidance revision invalidates every module citing it. Grep this file's IDs
   to find consumers before changing a row.
4. Record what changed, not just the new date — R1 above changed criteria, not
   only its year.
