# SYNTHETIC — Study RBL-102, PK Analysis Plan (signed v1.0)

> Fully synthetic. Fictional compound "rembrolide", fictional study RBL-102.
> This is the **rule source**. Every check on the NCA output package applies the
> rules written here, and every finding names the rule it applied.

## 1. AUC calculation

AUC is calculated by the **linear-up/log-down trapezoidal method**. AUC0-inf is
AUClast plus the extrapolated tail.

## 2. Terminal-phase (lambda-z) acceptance criteria

A terminal-phase estimate is acceptable only when **all three** hold:

| # | Criterion |
|---|---|
| A1 | At least **three** concentration points in the terminal phase |
| A2 | **Adjusted R-squared of the log-linear regression at least 0.85** |
| A3 | Extrapolated portion of AUC0-inf no more than 20% |

A profile failing any criterion is reported with its half-life and AUC0-inf
**flagged as not meeting the acceptance criteria**, and the reason stated.

## 3. BLQ handling

- Before the first quantifiable concentration: BLQ records are set to zero.
- After the last quantifiable concentration: BLQ records are **excluded from the
  derivation**. They are not set to zero and not carried forward.

## 4. Time basis

Parameters are derived using **actual sampling times**. Nominal times are used
for tabulation and figures only.

## 5. Exclusion criteria — exhaustive

A participant profile may be excluded from the summary statistics **only** for
one of the following, each documented in the exclusion log with its date:

| # | Criterion |
|---|---|
| E1 | A documented dosing deviation — dose not administered, partial dose, or wrong dose |
| E2 | **Emesis within two times the median Tmax** of the study population |

Exposure magnitude is **not** an exclusion criterion. A profile is not excluded
for being high, low, or unlike the rest of the cohort.

Where a profile meets E1 or E2 it **is** excluded; the criteria are applied in
both directions.

## 6. Units

| Parameter | Unit |
|---|---|
| AUClast, AUC0-inf | ng·h/mL |
| Cmax | ng/mL |
| Tmax, terminal half-life | h |
| Apparent clearance (CL/F) | **L/h** |
| Apparent volume of distribution (Vz/F) | L |

Every reported parameter carries its unit in the column header or the cell.

## 7. Rounding and precision

| Quantity | Convention |
|---|---|
| Exposure parameters (AUC, Cmax) | **three significant figures** |
| Terminal half-life | **two decimal places** |
| Clearance and volume | three significant figures |

## 8. Summary-statistic definitions

| Parameter | Statistic |
|---|---|
| AUC0-inf, Cmax | **Geometric mean** and geometric CV% |
| Tmax | Median with range |
| Terminal half-life | Arithmetic mean with standard deviation |
| n | **The number of profiles contributing to the statistic**, after exclusions |

## 9. Reconciliation tolerance

Rounding tolerance for reconciling a reported value against its dataset row:
**0.5%**.
