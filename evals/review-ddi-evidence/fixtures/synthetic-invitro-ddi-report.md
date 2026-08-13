# SYNTHETIC — In-vitro drug interaction report IV-DDI-VLT-003 (v2.0)

> Fully synthetic. Fictional compound "veltrapib", fictional interacting drugs
> "cyprazole" and "vorastol". No real compound, sponsor or laboratory data.
> Generated for evaluation only.

**Compound:** veltrapib
**Report version:** v2.0, issued 2025-09-30 (supersedes v1.0 of 2025-03-11)
**Systems:** pooled human liver microsomes; cryopreserved human hepatocytes;
transfected cell lines

---

## 1. Exposure inputs used throughout this report

| Input | Value | Source |
|---|---|---|
| Total Cmax at the highest clinical dose | 1.86 µM | Study VLT-1002 |
| Unbound fraction in plasma | 0.045 | Report BIND-VLT-001 |
| Unbound Cmax (Imax,u) | 0.084 µM | Calculated, 1.86 × 0.045 |
| Nominal gut concentration (Igut) | 21.4 µM | Dose / 250 mL |

---

## 2. Reversible enzyme inhibition

### Table 2.1 — Reversible inhibition parameters (parameter table of record)

| Enzyme | IC50 | Ki | R1 = 1 + Imax,u/Ki |
|---|---|---|---|
| CYP1A2 | > 50 µM | not determined | not applicable |
| CYP2C9 | 25.2 µM | 12.6 µM | 1.01 |
| CYP2C19 | > 50 µM | not determined | not applicable |
| CYP2D6 | > 50 µM | not determined | not applicable |
| CYP3A (probe substrate site) | 33.0 µM | 16.5 µM | 1.01 |

Narrative: veltrapib inhibited CYP2C9 reversibly with an IC50 of 25.2 nM. All
other reversible inhibition was weak or absent.

Intestinal CYP3A: R1,gut = 1 + Igut/Ki = 1 + 21.4/16.5 = 2.30.

---

## 3. Time-dependent inhibition

Time-dependent inhibition was detected for CYP2B6 only. No time-dependent
inhibition of CYP3A, CYP2C9 or CYP2D6 was detected under the conditions tested.

### Table 3.1 — Time-dependent inhibition of CYP2B6

| Parameter | Value |
|---|---|
| KI | 1.8 µM |
| kinact | 0.042 min⁻¹ |
| kdeg (hepatic CYP2B6) | 0.000321 min⁻¹ |

The predicted R2 for time-dependent inhibition of hepatic CYP2B6, calculated by
this laboratory from the parameters above and the unbound Cmax in section 1, is
1.87.

No clinical interaction study of veltrapib with a CYP2B6 substrate has been
conducted, and no modelling substitution for one exists.

---

## 4. Induction

Cryopreserved human hepatocytes from three donors, 48-hour incubation.

| Enzyme | Maximum fold change in mRNA at 10 µM | Interpretation stated by the laboratory |
|---|---|---|
| CYP1A2 | 1.1 | No induction observed |
| CYP2B6 | 1.3 | No induction observed |
| CYP3A4 | 1.4 | Below the fold-change criterion in section 6 |

---

## 5. Transporters

### Table 5.1 — Veltrapib as a transporter inhibitor

| Transporter | IC50 | Ratio computed by this laboratory | Ratio type |
|---|---|---|---|
| P-gp | > 100 µM | not applicable | — |
| BCRP | 46 µM | 1.02 | intestinal |
| OATP1B1 | 2.1 µM | 1.31 | hepatic inlet |
| OAT3 | > 100 µM | not applicable | — |

### Table 5.2 — Veltrapib as a transporter substrate

| Transporter | Efflux or uptake ratio | Interpretation stated by this laboratory |
|---|---|---|
| P-gp | 1.4 | Not a substrate under the conditions tested |
| BCRP | 1.2 | Not a substrate under the conditions tested |
| OATP1B1 | 1.1 | Not a substrate under the conditions tested |

---

## 6. Criteria applied by this laboratory

The cutoff criteria applied in sections 2, 3 and 5 are those in the guidance
extract supplied with this package; this report transcribes none of its own. The
single criterion this laboratory sets itself is the induction fold-change
criterion, which it fixes at a **2-fold** change in mRNA relative to vehicle
control.
