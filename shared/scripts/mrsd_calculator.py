#!/usr/bin/env python3
"""T01 — NOAEL → HED → MRSD conversion chain.

Implements the FDA 2005 body-surface-area conversion (`fda-mrsd`). Every step is
arithmetic with an audit trail, so a reviewer can check the chain by hand.

**The skill consuming this never selects a starting dose.** It produces the
conversion with its assumptions visible; the dose is a human decision.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-05
Dependencies: Python standard library only
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: Km = body weight (kg) / body surface area (m²). FDA 2005 Table 1.
KM_FACTORS = {
    "human": 37.0, "human_child": 25.0, "mouse": 3.0, "hamster": 5.0,
    "rat": 6.0, "ferret": 7.0, "guinea_pig": 8.0, "rabbit": 12.0,
    "dog": 20.0, "monkey": 12.0, "marmoset": 6.0, "squirrel_monkey": 12.0,
    "baboon": 20.0, "micro_pig": 27.0, "mini_pig": 35.0,
}
DEFAULT_SAFETY_FACTOR = 10.0


@dataclass
class ConversionStep:
    step: str
    formula: str
    inputs: dict[str, float]
    result: float
    unit: str


@dataclass
class MRSDResult:
    hed_mg_kg: float
    mrsd_mg_kg: float
    mrsd_mg_total: float | None
    audit: list[ConversionStep] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def hed_from_noael(noael_mg_kg: float, species: str) -> tuple[float, ConversionStep]:
    """HED (mg/kg) = animal NOAEL (mg/kg) × (animal Km / human Km)."""
    key = species.strip().lower().replace(" ", "_").replace("-", "_")
    if key not in KM_FACTORS:
        raise ValueError(f"unknown species '{species}'; known: {sorted(KM_FACTORS)}")
    if noael_mg_kg <= 0:
        raise ValueError("NOAEL must be positive")
    ratio = KM_FACTORS[key] / KM_FACTORS["human"]
    hed = noael_mg_kg * ratio
    return hed, ConversionStep(
        step="NOAEL → HED",
        formula="HED = NOAEL × (Km_animal / Km_human)",
        inputs={"NOAEL_mg_kg": noael_mg_kg, "Km_animal": KM_FACTORS[key], "Km_human": 37.0},
        result=hed, unit="mg/kg")


def mrsd_from_hed(hed_mg_kg: float, safety_factor: float = DEFAULT_SAFETY_FACTOR,
                  human_weight_kg: float | None = 60.0) -> MRSDResult:
    """MRSD = HED / safety factor. Default factor 10 per FDA 2005."""
    if safety_factor < 1:
        raise ValueError("safety factor must be at least 1")
    mrsd = hed_mg_kg / safety_factor
    steps = [ConversionStep(step="HED → MRSD", formula="MRSD = HED / safety factor",
                            inputs={"HED_mg_kg": hed_mg_kg, "safety_factor": safety_factor},
                            result=mrsd, unit="mg/kg")]
    warnings: list[str] = []
    if safety_factor < DEFAULT_SAFETY_FACTOR:
        warnings.append(
            f"Safety factor {safety_factor} is below the default 10. A reduced factor "
            f"requires explicit justification and is a human decision.")
    total = None
    if human_weight_kg:
        total = mrsd * human_weight_kg
        steps.append(ConversionStep(step="MRSD → total dose",
                                    formula="total = MRSD × body weight",
                                    inputs={"MRSD_mg_kg": mrsd, "weight_kg": human_weight_kg},
                                    result=total, unit="mg"))
    return MRSDResult(hed_mg_kg=hed_mg_kg, mrsd_mg_kg=mrsd, mrsd_mg_total=total,
                      audit=steps, warnings=warnings)


def most_sensitive_species(noaels: dict[str, float]) -> tuple[str, float, list[tuple[str, float]]]:
    """Lowest HED identifies the most sensitive species. Returns the full ranking
    so a reviewer sees what was rejected, not only what was chosen."""
    if not noaels:
        raise ValueError("no NOAEL values supplied")
    ranked = sorted(((s, hed_from_noael(v, s)[0]) for s, v in noaels.items()),
                    key=lambda x: x[1])
    return ranked[0][0], ranked[0][1], ranked
