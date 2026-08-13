# Governance

How decisions get made in ClinPharm PMx Skills, and what it takes to change what the
project claims.

## Maintainer

Malek Okour is the maintainer and final decision-maker. The project is small and
does not pretend to have a committee.

## The claim this project defends

Every skill here reports **mechanical findings** — internal inconsistencies
between documents, values that contradict their own analysis plan, arithmetic
that does not hold. None of them recommends a dose, and none issues a clinical
conclusion. A tool that reports a discrepancy is telling you two documents
disagree, not which one is right.

That boundary is enforced in code and tested, not merely written down. Changes
that weaken it will not be merged, however useful they seem.

## Skill status — `released` vs `built`

Every package carries one of these in [`catalog/catalog.json`](../catalog/catalog.json):

| Status | Means |
|---|---|
| `released` | The evaluation gate passed. Planted-defect recall and precision met the declared threshold, no Critical defect was missed, activation was measured against named neighbours |
| `built` | The package exists and validates, but **the evaluation has not been run**. It carries an explicit `evidence_gap` saying what is missing |

`built` exists because the alternative vocabulary — "done" — would have been a
lie. A package can be well-formed, install cleanly, and still miss the defects it
was written to catch. Structural validity is not evidence of detection.

The collections under `collections/*/collection.json` are the **source of record**
for status. The catalog is a derived view. CI fails if they disagree, and fails if
a `built` entry declares no `evidence_gap`.

## Contributing a skill

1. Open an issue using the **skill request** template first. Scope is agreed before
   anyone writes a package.
2. New packages enter as `built` with an honest `evidence_gap`. Nothing is born
   `released`.
3. Promotion to `released` requires the full evaluation: a synthetic fixture with
   enumerated planted defects and an expert key, recall and precision against the
   declared threshold, no missed Critical, and activation accuracy against the
   skill's named neighbours.

Script-detectable defects must be found by the scripts **in every run**. A miss
there is a script bug, not model variance, and is fixed in the script.

## Evidence and citation

Regulatory anchors — ICH, FDA, EMA, PMDA — are verified against the **issuing
body's own page**, recording title, status (draft or final), and revision date.
Secondary compilations have been wrong here more than once. Claims that drift
carry the date they were checked.

## Data

Only public, synthetic, or redistributable material enters this repository, its
history, its issues, or its releases. No patient-level data, no sponsor-confidential
material, no unpublished submissions.

Fixtures are synthetic by construction. If you contribute one, it must be
synthetic by construction too — not anonymised from something real.

## Security

See [`SECURITY.md`](../SECURITY.md) for reporting. Secret scanning runs before any
push; a finding stops the push rather than being allowlisted away.

## Changing this document

Governance changes go through a pull request and are the maintainer's call. If a
change would alter what the project claims about its own skills, say so
explicitly in the PR description rather than leaving it to be inferred from the
diff.
