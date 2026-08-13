# Library-router selection confusion matrix

**Updated:** 2026-08-11 (post W4 reopen / domain authoring)  
**Gate:** `scripts/check_router_selection.py`  
**Cases:** `evals/library-router/selection-cases.json`  
**Registry:** 151 packages (`catalog/nav_registry.json`)

Deterministic runner — no model in the loop. Each row asserts an expected `decision` / `chosen` / `complexity` (and optional reason tokens) against `scripts/library_router.py` under the case profile.

## Run summary (2026-08-11, post-authoring)

| Metric | Value |
|---|---|
| Total cases executed | **231** / 231 |
| Gate result | **PASS** (`make -C clinpharm-pmx-skills check`) |
| Top-1 accuracy (SINGLE class) | **149 / 149 = 100%** |
| Profiles exercised | 7 (`shipped`, `auto`, `auto_released_only`, `manual_only`, `auto_csr_disabled`, `force_ddi`, `force_ddi_disabled`) |

## Pass / fail by case class

| Class | Denominator | Pass | Fail | Notes |
|---|---:|---:|---:|---|
| SINGLE | 149 | 149 | 0 | One top-1 case per selectable package except `review-exposure-safety-margins` (near-tie; held as AMBIGUOUS trap) |
| AMBIGUOUS | 37 | 37 | 0 | Vague requests, meta skill asks, near-miss siblings |
| MULTI | 9 | 9 | 0 | Programme-scope and two-strong-candidates + conjunction guard |
| SIMPLE | 10 | 10 | 0 | Too-short / no-signal utterances → `no_candidates` |
| HUMAN_ONLY | 9 | 9 | 0 | Dose selection, sign-off, autonomous decisions → refuse |
| OOS | 10 | 10 | 0 | Wet-lab, CMC, medical affairs, patient-facing → refuse |
| POSTURE | 3 | 3 | 0 | Shipped ask-and-confirm, released-only guard, manual-only |
| OPERATOR | 4 | 4 | 0 | Disabled skill, force skill, contradictory force+disable |

**Class total:** 149+37+9+10+9+10+3+4 = **231**.

## SINGLE coverage gap (intentional)

| Package id | Disposition |
|---|---|
| `review-exposure-safety-margins` | No unambiguous top-1 utterance under current IDF scoring; pair covered by AMBIGUOUS traps |
| `library-router` | Non-selectable meta skill (`NON_SELECTABLE`) |

## How to refresh

```bash
make -C clinpharm-pmx-skills check   # includes check_router_selection.py
# then update this file's denominators from the gate summary lines
```

Selection accuracy on a deterministic router is **not** PS-D024 qualification evidence.
Domain skills remain `built` until practitioner adjudication.
