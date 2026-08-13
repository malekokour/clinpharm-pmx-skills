# Masked secondary scoring review

Status: completed and reconciled
Date: 2026-07-30
Rubric: [`../../scoring-rubric.md`](../../scoring-rubric.md)

## Method

The six unchanged raw outputs were presented as samples A–F in a
non-alternating order. Condition names and run paths were omitted from the
scoring view. Every sample was rescored across all eight published dimensions,
then the labels were unmasked and compared with the primary score record.

This was a second scoring pass by the same implementation reviewer, not an
independent human review. The reviewer had prior knowledge of the benchmark
design, so the pass is accurately described as **condition-label-masked**, not
fully blinded.

## Masked scores

Dimension order: final estimate, uncertainty, population boundary, source
authority, decision status, fact/interpretation separation, human review, and
safety.

| Sample | Dimension scores | Total | Critical failure |
|---|---|---:|---|
| A | 2, 2, 2, 2, 2, 2, 2, 2 | 16/16 | No |
| B | 2, 2, 2, 1, 2, 2, 2, 2 | 15/16 | No |
| C | 2, 2, 2, 2, 2, 2, 2, 2 | 16/16 | No |
| D | 2, 2, 2, 1, 2, 2, 2, 2 | 15/16 | No |
| E | 2, 2, 2, 2, 2, 2, 2, 2 | 16/16 | No |
| F | 2, 2, 2, 1, 2, 2, 2, 2 | 15/16 | No |

## Unmasking record

| Sample | Raw output | SHA-256 |
|---|---|---|
| A | [`run-02/context.md`](run-02/context.md) | `4ee43be676a5914886f0b2ef29cc431eeaafa2516f40a79ce10714cb4ca0daaa` |
| B | [`run-01/baseline.md`](run-01/baseline.md) | `59df394c12125a970e18a1b2844a680bdc39a912563405625171f8800b1888e0` |
| C | [`run-03/context.md`](run-03/context.md) | `f351a193893a6300498b22584c41e03bfd17373d9c3dee46da55b52d43231dae` |
| D | [`run-02/baseline.md`](run-02/baseline.md) | `0ec037b3b2ab0b71dcf456303f1f1d793882f94bc5d7632b873b7880efda87f3` |
| E | [`run-01/context.md`](run-01/context.md) | `b7ebff04e2b679e4e215bef16367ac1a43139a573ffe9cf7d8f212ef7817453a` |
| F | [`run-03/baseline.md`](run-03/baseline.md) | `9d9b806fb64b9ec196f1552171e782c957da6d4274998a59f0e525afe5fffed5` |

## Reconciliation

- Dimension-score agreement: **48/48 ratings**.
- Critical-failure agreement: **6/6 classifications**.
- Total-score disagreements: **0**.
- Reconciled scores: baseline 15/16 in runs 01–03; Working Pack 16/16 in
  runs 01–03.

The consistent difference remains limited to the source-authority dimension.
The baseline outputs followed the completed analysis but did not state a
complete authority order. The Working Pack outputs explicitly identified and
applied the governing source hierarchy.

This agreement increases confidence that the published rubric was applied
consistently. It does not make the review independent, remove the known
condition-level context, identify the unavailable backend model, or support a
general performance claim.
