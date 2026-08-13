# SYNTHETIC — Sponsor protocol template, clinical pharmacology conventions (v6)

> Fully synthetic. Fictional sponsor conventions. This is the **rule source**:
> every conformance comment on study CVS-101 is checked against this file, not
> against generic expectations.

## 1. Required clinical pharmacology elements

A protocol is conformant only if every element below is present and locatable.

| # | Required element |
|---|---|
| R1 | PK and PD objectives with named endpoints |
| R2 | Dose levels, escalation schema and stopping rules |
| R3 | Administration and fasting conditions |
| R4 | PK sampling schedule as nominal times with permitted windows |
| R5 | Sample handling and shipping |
| R6 | Bioanalytical method identifier, matrix, LLOQ and validation status |
| R7 | Participant restrictions, including a **standardised meal requirement for any study deriving Cmax** |
| R8 | The PK parameters to be derived |
| R9 | **PK analysis population definition** — which participants and which profiles contribute to each summary |
| R10 | **BLQ handling convention** — before and after the first quantifiable concentration |
| R11 | Handling of missing samples, protocol deviations and profile exclusions |
| R12 | Rounding and unit conventions |

An element the protocol states it is **deliberately deferring** to a named
downstream document is recorded as deferred, not as a gap.

## 2. Sampling-window convention

A permitted sampling window **may not exceed plus or minus half the interval to
the nearest adjacent nominal time**. Windows that would overlap an adjacent
window are non-conformant regardless of their absolute width.

## 3. Terminal-phase coverage convention

For a study whose endpoints include terminal half-life, sampling must extend
**at least three reported terminal half-lives after the final dose**. The
reported half-life is taken from the current Investigator's Brochure edition
declared in the version baseline below — never estimated, and never carried over
from a similar compound.

## 4. Unit and precision conventions

| Quantity | Convention |
|---|---|
| Plasma concentration | ng/mL |
| Exposure (AUC) | ng·h/mL |
| Apparent clearance | L/h |
| Reported precision | **three significant figures** |

## 5. Dose-rationale traceability

**Every dose level in the protocol must trace to a stated derivation source** —
a nonclinical study with an exposure margin, an Investigator's Brochure section,
or a named model-based simulation. A dose level with no traceable basis is
recorded as `untraceable-rationale`.

## 6. Version baseline declaration

| Document | Authoritative version for this review |
|---|---|
| Protocol | 2.0 |
| Investigator's Brochure | **Edition 4.0** |
| Bioanalytical method summary | 1.2 |

A protocol citing a superseded version of a baseline document is a finding in its
own right, independent of whether the cited content happens to agree.
