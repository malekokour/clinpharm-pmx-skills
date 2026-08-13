# Pharmacometrics

Quantitative pharmacology workflows: population modelling, exposure–response,
mechanistic and systems models, and the statistics and data standards underneath them.

**Co-equal with clinical pharmacology in ambition and in the public roadmap.** Not
co-equal in qualification depth yet, and this page says so rather than implying otherwise.

## What ships today (measured)

**16 packages** are registered in `collection.json`. Regenerate before quoting:

```bash
python3 -c "import json; print(len(json.load(open('collections/pharmacometrics/collection.json'))['skills']))"
```

| Status honesty | Meaning here |
|---|---|
| `released` | **16** — each package has a paired-run qualification dossier and carries the evidence stamp `cursor-release150-paired-runs-ps-d024` |
| `built` | **0** — no PMx package is currently awaiting qualification |

**What `released` does and does not mean here.** It means the package passed the
qualification route defined in PS-D024 (risk-tiered qualification): a paired-run
dossier per package, plus explicit owner authorization. **It is not a claim of
clinical performance, and not GxP validation.** The distinction is the point of
the vocabulary — see [`../../CLAIM-LEDGER.md`](../../CLAIM-LEDGER.md).

One package — `review-model-analysis-deliverable` — is the pre-W4 hand-authored PMx
home skill. The other fifteen were registered from Band A / Quantitative pharmacology
gap rows and qualified in Release-150.

> **Corrected 2026-08-13.** This table previously read `released` **0** /
> `built` **16**, with the note *"treat them as built scaffolds pending real
> authoring."* That was accurate until Release-150 promoted all sixteen; the
> promotion touched `collection.json` and this file was never updated, so the
> collection contradicted its own source of record in published bytes for a day.
>
> Corrected toward the collection, not away from it, because the promotion is
> evidenced: **16 of 16** packages have a `K06-Cursor-Release150` dossier, and
> `collection.json` reports 16 `released` with 0 `evidence_gap`. The old text is
> retained here because a reader who saw the earlier version needs to know which
> way the contradiction resolved, rather than finding it silently gone.
>
> `collection.json` is the source of record; this README describes it. On any
> future disagreement, the JSON wins and this file is the one to fix.

## What the track covers

The job model places **16 rows** under Band A / Quantitative pharmacology. Fifteen are
skills; one (*AI/ML methods in drug development*) is a shared reference because it names
a field rather than a task.

| Area | Rows |
|---|---|
| Population and exposure–response modelling | Population PK and covariate modelling · Exposure–response modelling · Model-based meta-analysis · Disease-progression modelling · Model evaluation and diagnostics · Model analysis plan and report |
| Mechanistic and systems | PBPK and biopharmaceutics · Quantitative systems pharmacology · Agent-based models |
| Statistics | Bioequivalence TOST and confidence intervals · Sample size and power · Multiplicity and inference in exposure–response |
| Data and reproducibility | Analysis dataset standards and provenance · CDISC PK domains and define.xml · Computational environment and reproducibility |

## Why the collection exists before qualification depth does

Because the alternative is worse. Filing pharmacometrics work inside the clinical
pharmacology collection until it is "big enough" makes the track invisible in exactly
the period when its roadmap position matters most. A collection that states membership
and status honestly beats one that hides the track or overclaims readiness.

## Where contexts do the heavy lifting here

Pharmacometric methods apply across every modality and therapeutic area. One
`contexts/` file lifts every skill in this collection rather than forcing a
variant per combination — which is what makes co-equal depth affordable rather than a
multiplication of packages.

## Status vocabulary

`released` means the evaluation gate passed. `built` means the package validates and the
gate has not run. Counts are regenerated from `collection.json`, never typed by hand.

## Related

[The map](../../site/map/index.html) · [Workflows](../../docs/workflows/) ·
[ROADMAP](../../ROADMAP.md)
