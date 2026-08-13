#!/usr/bin/env python3
"""T03 — PK parameter plausibility and unit checker.

Mechanical checks only. Every finding this module emits is a *mechanical
finding*: two values disagree, a unit is inconsistent with a stated convention,
an arithmetic relationship does not hold. None of them is a scientific
conclusion, and the caller must not present them as one.

Consumed by: review-csr-pk-consistency, verify-nca-outputs, review-study-conduct-pk.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-05
Dependencies: Python standard library only
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

# --- unit vocabulary -----------------------------------------------------------

CONCENTRATION_UNITS = {"ng/mL", "µg/mL", "ug/mL", "mg/L", "pg/mL", "nmol/L", "µmol/L"}
AUC_UNITS = {"ng·h/mL", "ng*h/mL", "ng.h/mL", "µg·h/mL", "ug*h/mL", "mg·h/L", "h·ng/mL"}
CLEARANCE_UNITS = {"L/h", "mL/h", "mL/min", "L/h/kg", "mL/min/kg"}
VOLUME_UNITS = {"L", "mL", "L/kg", "mL/kg"}
TIME_UNITS = {"h", "hr", "hour", "hours", "min", "d", "day", "days"}

PARAMETER_UNITS = {
    "cmax": CONCENTRATION_UNITS,
    "cmin": CONCENTRATION_UNITS,
    "ctrough": CONCENTRATION_UNITS,
    "css": CONCENTRATION_UNITS,
    "auc": AUC_UNITS,
    "auc0-t": AUC_UNITS,
    "auc0-inf": AUC_UNITS,
    "auctau": AUC_UNITS,
    "cl": CLEARANCE_UNITS,
    "cl/f": CLEARANCE_UNITS,
    "vd": VOLUME_UNITS,
    "vz/f": VOLUME_UNITS,
    "vss": VOLUME_UNITS,
    "tmax": TIME_UNITS,
    "t1/2": TIME_UNITS,
    "thalf": TIME_UNITS,
}

#: Order-of-magnitude sanity bounds. Deliberately wide: this catches unit swaps
#: and transcription errors, NOT unusual-but-real pharmacology. A value outside
#: these bounds is a prompt to look, never a claim that it is wrong.
PLAUSIBLE_RANGES = {
    "t1/2": (0.05, 2000.0),      # hours; covers rapid IV agents to long mAbs
    "tmax": (0.05, 336.0),        # hours
    "cl": (0.001, 5000.0),        # L/h
    "vd": (0.5, 50000.0),         # L
}


@dataclass
class Finding:
    """A mechanical finding. Never a scientific conclusion."""

    rule: str
    severity: str            # Critical | Major | Minor
    parameter: str
    observed: str
    expected: str
    locator: str
    detail: str
    kind: str = "mechanical"

    def as_dict(self) -> dict[str, str]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "parameter": self.parameter,
            "observed": self.observed,
            "expected": self.expected,
            "locator": self.locator,
            "detail": self.detail,
            "kind": self.kind,
        }


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    checked: int = 0
    skipped: list[str] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    def summary(self) -> dict[str, object]:
        """Coverage is always reported. A finding count without a denominator
        is unfalsifiable — the reader cannot tell a clean document from an
        unread one."""
        return {
            "checked": self.checked,
            "findings": len(self.findings),
            "skipped": len(self.skipped),
            "by_severity": {
                s: sum(1 for f in self.findings if f.severity == s)
                for s in ("Critical", "Major", "Minor")
            },
        }


def normalise_parameter(name: str) -> str:
    return re.sub(r"[\s_]+", "", name.strip().lower()).replace("auc0−", "auc0-")


def check_unit(parameter: str, unit: str, locator: str, report: Report,
               declared_units: dict[str, str] | None = None) -> None:
    """Check a unit against the study's DECLARED convention, then its class.

    ``declared_units`` maps a **normalised** parameter name to the unit the
    analysis plan specifies. Keys go through ``normalise_parameter``, so the key
    for ``CL/F`` is ``"cl/f"`` — not ``"cl"``, which this docstring gave as its
    example until 2026-08-06 and which silently matches nothing. A caller
    following the old example got zero findings and no warning, which is the same
    shape of defect as the check being unwired in the first place.

    e.g. ``{"cl/f": "L/h", "auc0-tau": "ng·h/mL"}``. Checking only against the class vocabulary misses the
    most common real defect: a unit that is *valid for the parameter* but
    contradicts the study's own pre-specified convention. A clearance reported in
    mL/h where the plan says L/h is a 1000x error that passes any class check.

    This gap was found by measurement, not review — the fixture's planted unit
    swap went undetected while the class check reported success.
    """
    report.checked += 1
    key = normalise_parameter(parameter)

    if declared_units:
        declared = declared_units.get(key)
        if declared and unit.strip() != declared.strip():
            report.add(
                Finding(
                    rule="unit-contradicts-analysis-plan",
                    severity="Critical",
                    parameter=parameter,
                    observed=unit,
                    expected=declared,
                    locator=locator,
                    detail=(
                        f"Unit '{unit}' contradicts the analysis plan's declared "
                        f"convention '{declared}' for {parameter}. Valid for the "
                        f"parameter class, but not what this study pre-specified."
                    ),
                )
            )
            return

    accepted = PARAMETER_UNITS.get(key)
    if accepted is None:
        report.skipped.append(f"{parameter} @ {locator}: no unit vocabulary")
        return
    if unit.strip() not in accepted:
        report.add(
            Finding(
                rule="unit-inconsistency",
                severity="Critical",
                parameter=parameter,
                observed=unit,
                expected=" | ".join(sorted(accepted)),
                locator=locator,
                detail=(
                    f"Unit '{unit}' is not in the accepted vocabulary for "
                    f"{parameter}. A unit swap changes the value by orders of "
                    f"magnitude; confirm against the analysis plan convention."
                ),
            )
        )


def check_range(parameter: str, value: float, locator: str, report: Report) -> None:
    """Order-of-magnitude sanity. Wide by design."""
    report.checked += 1
    key = normalise_parameter(parameter)
    bounds = PLAUSIBLE_RANGES.get(key)
    if bounds is None:
        report.skipped.append(f"{parameter} @ {locator}: no range defined")
        return
    low, high = bounds
    if not (low <= value <= high):
        report.add(
            Finding(
                rule="implausible-range",
                severity="Major",
                parameter=parameter,
                observed=str(value),
                expected=f"{low}–{high}",
                locator=locator,
                detail=(
                    "Value sits outside the order-of-magnitude sanity range. "
                    "This flags transcription and unit errors; it does not "
                    "assert the value is scientifically wrong."
                ),
            )
        )


def check_accumulation_consistency(
    half_life_h: float,
    tau_h: float,
    reported_ratio: float,
    locator: str,
    report: Report,
    tolerance: float = 0.30,
) -> None:
    """Accumulation ratio implied by half-life and dosing interval.

    For a one-compartment drug at steady state,
        R = 1 / (1 - exp(-ln(2) * tau / t½))

    A reported ratio far from that is a mechanical inconsistency between two
    reported numbers. It is emphatically NOT a claim about which is correct —
    multi-compartment kinetics, time-dependent clearance and flip-flop
    absorption all legitimately break the single-exponential assumption. The
    default tolerance is deliberately loose for that reason.
    """
    report.checked += 1
    if half_life_h <= 0 or tau_h <= 0:
        report.skipped.append(f"accumulation @ {locator}: non-positive input")
        return
    expected = 1.0 / (1.0 - math.exp(-math.log(2) * tau_h / half_life_h))
    if expected <= 0:
        report.skipped.append(f"accumulation @ {locator}: undefined")
        return
    deviation = abs(reported_ratio - expected) / expected
    if deviation > tolerance:
        report.add(
            Finding(
                rule="accumulation-half-life-inconsistency",
                severity="Major",
                parameter="accumulation ratio",
                observed=f"{reported_ratio:.3g}",
                expected=f"{expected:.3g} (from t½={half_life_h:g} h, tau={tau_h:g} h)",
                locator=locator,
                detail=(
                    f"Reported ratio deviates {deviation:.0%} from the value implied "
                    f"by the reported half-life under one-compartment assumptions. "
                    f"Multi-compartment or time-dependent kinetics can explain this; "
                    f"a qualified reviewer decides which number to trust."
                ),
            )
        )


def check_ratio_statistic(
    point_estimate: float,
    ci_low: float,
    ci_high: float,
    locator: str,
    report: Report,
) -> None:
    """The CI must bracket the point estimate and be correctly ordered."""
    report.checked += 1
    if ci_low > ci_high:
        report.add(
            Finding(
                rule="ci-bounds-reversed",
                severity="Critical",
                parameter="ratio",
                observed=f"[{ci_low}, {ci_high}]",
                expected="lower ≤ upper",
                locator=locator,
                detail="Confidence interval bounds are reversed.",
            )
        )
        return
    if not (ci_low <= point_estimate <= ci_high):
        report.add(
            Finding(
                rule="point-estimate-outside-ci",
                severity="Critical",
                parameter="ratio",
                observed=f"{point_estimate} not in [{ci_low}, {ci_high}]",
                expected="point estimate within its confidence interval",
                locator=locator,
                detail=(
                    "The point estimate falls outside its own confidence interval. "
                    "One of the three numbers is misreported."
                ),
            )
        )


def significant_figures(text: str) -> int | None:
    """Count significant figures as *written*. Trailing zeros count.

    Operates on the string, never on a parsed float: 1.10 and 1.1 are the same
    number and different reported precisions, and it is the reported precision
    the analysis plan constrains.
    """
    s = text.strip().lstrip("+-")
    if not s or not any(c.isdigit() for c in s):
        return None
    if "." in s:
        whole, _, frac = s.partition(".")
        if whole.lstrip("0"):
            # 1.08 -> "1"+"08" = 3 ; 11.4 -> "11"+"4" = 3
            digits = whole.lstrip("0") + frac
        else:
            # 0.94 -> "94" = 2 ; 0.0410 -> "410" = 3 (leading zeros are not significant)
            digits = frac.lstrip("0")
        return len(digits) or None
    # No decimal point: trailing zeros are ambiguous by convention, so they are
    # not counted. 412 -> 3 ; 4120 -> 3 ; 400 -> 1.
    stripped = s.rstrip("0")
    return len(stripped) if stripped else 1


def check_significant_figures(values: list[tuple[str, str]], expected: int,
                              locator: str, report: Report) -> None:
    """Every related value must be reported to the plan's stated precision.

    ``values`` is a list of (label, as-written) pairs that belong together — a
    point estimate and its confidence bounds, or a row of the same parameter.

    This exists because the fixture planted a slope at three significant figures
    beside its confidence bounds at two, against a plan requiring three. It is a
    *presentation* defect, not a numeric one: the values are right, the reported
    precision is internally inconsistent with the study's own convention.
    """
    report.checked += 1
    observed = {label: significant_figures(raw) for label, raw in values}
    offenders = {k: v for k, v in observed.items() if v is not None and v != expected}
    if offenders:
        report.add(
            Finding(
                rule="significant-figures-inconsistency",
                severity="Minor",
                parameter=", ".join(offenders),
                observed="; ".join(f"{k}={v} s.f." for k, v in offenders.items()),
                expected=f"{expected} significant figures",
                locator=locator,
                detail=(
                    f"Reported precision is inconsistent with the analysis plan's "
                    f"stated convention of {expected} significant figures. The "
                    f"values themselves are not in question."
                ),
            )
        )
