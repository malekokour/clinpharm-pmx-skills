---
contract: contradiction-ledger
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-04"
consumers: [review-csr-pk-consistency]
---

# Contradiction-preserving ledger

The record structure that makes "preserve the contradiction" enforceable rather
than aspirational. `evidence-hierarchy.md` states the principle; this file fixes
the shape.

## One row per flagged item

| Field | Required | Content |
|---|---|---|
| `id` | yes | Stable within the run, e.g. `D-007` |
| `class` | yes | One of: numeric-mismatch · contradiction · unsupported-claim · unit-inconsistency · plausibility-violation · stale-version · completeness-gap · presentation |
| `statement_as_written` | yes | The text under review, verbatim |
| `statement_locator` | yes | Document, version, section/table, row, page |
| `expected_value_or_content` | yes | What the precedent source says, verbatim |
| `expected_locator` | yes | Document, version, section/table, row, page |
| `detection_path` | yes | script · script-plus-model · model-only |
| `rule_applied` | when a tolerance or convention was used | e.g. "analysis plan §4.2 rounding: 3 significant figures" |
| `severity` | yes | Critical · Major · Minor — see below |
| `severity_basis` | yes | Why that class, in one line |
| `suggested_remediation` | optional | Proposed wording or correction, clearly marked as a proposal |
| `owner` | yes | Configurable; confirmed at run start, never assumed |
| `disposition` | yes | open · accepted · rejected-with-rationale · closed |
| `disposition_rationale` | when not `open` | Written by the human, not the assistant |

## Severity is calibrated to propagation, not prominence

The cost function is a wrong value travelling downstream into summaries,
labelling and agency answers — not how visible the error looks on the page.

- **Critical** — would change a numeric result or the direction of a conclusion
  that reaches a downstream document. Synopsis-versus-body mismatches, unit
  swaps, reversed comparison directions.
- **Major** — would mislead a careful reader without changing the headline
  result. Unsupported qualifiers, values reflecting a superseded amendment.
- **Minor** — presentation and citation hygiene.

## Both sides always survive

A contradiction row is malformed if it records only one statement. Both the
document's text and the precedent source's text appear, each with its own
locator, and neither is edited to fit the other.

The assistant does not choose between them, does not average them, does not mark
one "likely correct", and does not omit the one that is inconvenient for a tidy
register.

## Closure is not the assistant's

`disposition` may be written as `open` by the assistant and nothing else. Any
run whose output arrives with items already `accepted`, `rejected` or `closed`
has violated the human-review contract and should be treated as invalid.
