#!/usr/bin/env python3
"""Recompute a supplied NOAEL-to-HED-to-MRSD chain with an explicit basis.

Use exactly one HED basis: a sponsor-supplied divisor, or a species whose coded
Km values come from the package's sourced T01 mode. The tool never selects or
recommends a starting dose.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mrsd_calculator as t01


def calculate(
    noael_mg_kg: float,
    safety_factor: float,
    human_weight_kg: float,
    *,
    sponsor_conversion_factor: float | None = None,
    species: str | None = None,
) -> dict[str, object]:
    if noael_mg_kg <= 0 or safety_factor < 1 or human_weight_kg <= 0:
        raise ValueError("NOAEL and weight must be positive; safety factor must be at least 1")
    if (sponsor_conversion_factor is None) == (species is None):
        raise ValueError("supply exactly one of sponsor_conversion_factor or species")
    if sponsor_conversion_factor is not None:
        if sponsor_conversion_factor <= 0:
            raise ValueError("sponsor conversion factor must be positive")
        hed = noael_mg_kg / sponsor_conversion_factor
        basis = "sponsor-supplied divisor"
        hed_step = {
            "step": "NOAEL → HED",
            "formula": "HED = NOAEL / sponsor conversion factor",
            "inputs": {"NOAEL_mg_kg": noael_mg_kg, "conversion_factor": sponsor_conversion_factor},
            "result": hed,
            "unit": "mg/kg",
        }
    else:
        hed, step = t01.hed_from_noael(noael_mg_kg, species or "")
        basis = f"fda-mrsd coded Km table; species={species}"
        hed_step = {
            "step": step.step,
            "formula": step.formula,
            "inputs": step.inputs,
            "result": step.result,
            "unit": step.unit,
        }
    result = t01.mrsd_from_hed(hed, safety_factor, human_weight_kg)
    return {
        "basis": basis,
        "hed_mg_kg": hed,
        "hed_mg_kg_rounded_2dp": round(hed, 2),
        "mrsd_mg_kg": result.mrsd_mg_kg,
        "mrsd_mg_total": result.mrsd_mg_total,
        "audit": [hed_step] + [step.__dict__ for step in result.audit],
        "warnings": result.warnings,
        "boundary": "Arithmetic reproduction only; this tool does not select or recommend a starting dose.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--noael", required=True, type=float)
    parser.add_argument("--safety-factor", required=True, type=float)
    parser.add_argument("--human-weight", required=True, type=float)
    basis = parser.add_mutually_exclusive_group(required=True)
    basis.add_argument("--sponsor-conversion-factor", type=float)
    basis.add_argument("--species")
    args = parser.parse_args()
    try:
        result = calculate(
            args.noael,
            args.safety_factor,
            args.human_weight,
            sponsor_conversion_factor=args.sponsor_conversion_factor,
            species=args.species,
        )
    except ValueError as exc:
        print(json.dumps({"status": "CANNOT_ASSESS", "error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
