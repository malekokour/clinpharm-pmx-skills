---
module: privacy-routing
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
anchors: []
consumers: [reconcile-cross-document-facts]
---

# Study-type module — participant-data privacy routing

Cross-cutting reference content only. This module defines the inputs and routing
states for a structural privacy inventory; it is not a legal rules engine and
does not select which law, policy, authorization, waiver, or safeguard applies.

## Applicability contract

The accountable privacy/legal owner supplies the applicability declaration. The
assistant and deterministic tool preserve it verbatim and never infer it from a
country name, organization type, document label, or dataset field.

| Field | Required owner-supplied content |
|---|---|
| `owner_supplied` | Exact boolean `true`; otherwise applicability is `UNKNOWN` |
| `owner_role` | Named accountable role, not an inferred person |
| `status` | `APPLICABLE`, `NOT_APPLICABLE`, or `UNKNOWN`, as declared by the owner |
| `jurisdictions` | Explicit list; an empty or absent list remains `UNKNOWN` |
| `frameworks` | Owner-declared framework or policy identifiers; the module validates presence only |
| `as_of_date` | Date on which the applicability declaration was confirmed |
| `source_register` | Owner-controlled source/version locators supporting the declaration |

An `UNKNOWN` applicability state does not mean no privacy obligation applies.
It means the supplied evidence does not determine the route. Name the owner and
source that would resolve it; do not silently choose a familiar framework.

## Design conventions to check

- Accept only a schema explicitly labelled `SYNTHETIC_SCHEMA`. Reject record,
  row, participant, subject, observation, or value payloads before inventory
  checks. Qualification fixtures are synthetic by construction, never
  anonymised from a real participant dataset.
- Give every dataset a stable identifier, declared purpose, data-class list,
  coding state, key-custodian state, access-role list, access-log state,
  recipients, retention statement, and withdrawal statement.
- Separate coded data from the re-identification key and name the key custodian.
  Presence is checkable; adequacy and acceptable re-identification risk are not.
- Map every transfer to one dataset, one declared recipient, and one agreement
  identifier. Preserve cross-border or third-party labels as supplied without
  interpreting their legality.
- Record each agreement identifier and its declared recipients. An agreement's
  presence is not evidence that its terms are sufficient or applicable.
- Keep protocol, consent/authorization, data-management, vendor, retention, and
  withdrawal statements as separately located sources so mismatches remain
  visible instead of being harmonised.

## Expected statements in a report

| Element | Expected form |
|---|---|
| Input boundary | `SYNTHETIC_SCHEMA`; no participant records processed |
| Applicability | Owner role, status, jurisdictions, frameworks, as-of date, and source-register denominator |
| Inventory | Datasets, declared fields, flows, agreements, and structural checks as explicit counts |
| Findings | `PRESENT`, `MISSING`, or `MISMATCH`, with both identifiers/locators where relevant |
| Unresolved state | Exact token `UNKNOWN`, the unresolved question, and what owner-supplied evidence would resolve it |
| Review | `HUMAN-REVIEW` for applicability, lawful basis, compliance, safeguard adequacy, and re-identification risk |

Never report "privacy checks passed" without the structural-check denominator.
Never convert an empty list, missing applicability declaration, or unsupported
field into an implied clean result.

## Mechanical checks this module enables

1. **Applicability envelope present.** Required fields are present, and
   `owner_supplied` is exactly `true`; otherwise emit `UNKNOWN`.
2. **Dataset identifiers unique.** Duplicate identifiers are a mechanical
   mismatch because flows cannot be resolved deterministically.
3. **Structural fields present.** Count the required schema fields checked and
   name every missing field; do not judge the content of a present field.
4. **Code/key separation declared.** Compare `coding_state` with
   `key_custodian`; do not decide whether the separation is adequate.
5. **Flow dataset resolves.** Every flow refers to one declared dataset.
6. **Recipient concordance.** The flow recipient appears in the dataset's
   declared recipients and in the referenced agreement.
7. **Agreement resolves.** Every non-empty agreement identifier refers to one
   supplied agreement record.
8. **Unknowns remain visible.** Missing applicability, logging, retention,
   withdrawal, recipient, or agreement evidence stays `UNKNOWN` or `MISSING`;
   it is never converted to `NOT_APPLICABLE`.

## Boundaries

This module does not decide jurisdiction or applicability, lawful basis,
authorization or waiver validity, privacy or legal compliance, transfer
legality, safeguard adequacy, breach status, de-identification sufficiency, or
acceptable re-identification risk. Those remain with the named privacy/legal,
data-governance, security, and ethics owners.

It does not judge whether any difference is clinically significant and does not
select, adjust, recommend, or justify a dose. It processes no participant data,
draws no clinical conclusion, and approves no document, submission, agreement,
or use of data.
