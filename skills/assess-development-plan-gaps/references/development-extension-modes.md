---
contract: development-extension-modes
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-11"
consumer: assess-development-plan-gaps
---

# Development evidence extension modes

Use these modes only after the package's permitted-source preflight. Every
output is an evidence inventory for a named human reviewer. None is a strategy,
similarity, importance, value, approval, or go/no-go conclusion.

## TPP-EXTRACTION

### Inputs

Require the supplied target product profile or draft labeling concept, its
document identity/version/date, and the source artifacts it cites. A field with
no cited source is not filled from general knowledge.

### Procedure

1. Extract each proposed indication, population, route/formulation, dosing,
   efficacy concept, safety concept, and other proposed label statement exactly
   as written.
2. Preserve the field locator and every stated supporting-study or artifact ID.
3. Resolve each cited ID only against the supplied source set. Record the source
   document identity, version, date, and locator when found.
4. Write `NEEDS_INPUT` when a field cites no source, `UNKNOWN` when the citation
   is ambiguous, and `CANNOT_ASSESS` when the source cannot be read.
5. Report `fields_extracted / fields_encountered` and
   `source_links_resolved / source_links_declared`.

### Output fields

`field_id` · `field_type` · `statement_as_written` · `tpp_locator` ·
`declared_source_ids` · `resolved_source_locators` · `source_state` ·
`owner` · `disposition=open`

Do not rewrite a proposed claim, decide whether it is desirable or feasible,
predict whether a study can support it, or recommend a development strategy.

## REGULATORY-PRECEDENT and TRIAL-LANDSCAPE

### Inputs

Require one exact mode, caller-supplied public-database filters, maximum pages,
page size, UTC retrieval time, and optional exact public IDs to exclude. Never
invent a product, indication, modality, date, phase, status, or geography
filter. Never accept credentials in a filter or URL.

### Procedure

1. Run `scripts/public_development_intelligence.py` with the caller filters.
2. Preserve the filters verbatim beside the encoded requests.
3. Preserve every request/page boundary, next token or offset, retrieval
   timestamp, response provenance, exact public record ID, and raw public row.
4. Record caller exclusions by exact ID and reason. Record missing-ID rows as
   exclusions with `public_record_id=UNKNOWN`; never drop them silently.
5. Stop at the declared page bound. If another page exists, return
   `CANNOT_ASSESS` with `bounded_before_exhaustion`; do not call the result
   complete.
6. On transport, HTTP, JSON, schema, or pagination failure, retain completed
   pages, state the failure, and return `CANNOT_ASSESS` with a non-zero CLI exit.

### Output fields

`mode` · `status` · `complete` · `caller_filters` · `pagination` ·
`requests` · `records` · `exclusions` · `counts` · `boundary`

For `REGULATORY-PRECEDENT`, the exact public ID is the Drugs@FDA application
number. For `TRIAL-LANDSCAPE`, it is the ClinicalTrials.gov NCT ID.

The tool must not decide similarity, agency acceptance, competitive importance,
differentiation, materiality, valuation, approvability, or go/no-go. It also
must not infer that absence from the retrieved pages means absence from the
public database.

### Public route provenance

Checked 2026-08-11 against the issuing services' own documentation:

- openFDA Drugs@FDA endpoint:
  <https://api.fda.gov/drug/drugsfda.json>; usage and 99-record page limit:
  <https://open.fda.gov/apis/drug/drugsfda/how-to-use-the-endpoint/>; paging:
  <https://open.fda.gov/apis/paging/>.
- ClinicalTrials.gov API v2 endpoint:
  <https://clinicaltrials.gov/api/v2/studies>; specification and update notes:
  <https://clinicaltrials.gov/data-api/api>.

Route availability and public records are freshness-sensitive. The retrieval
timestamp proves when a request ran, not that the returned record is correct,
complete, or current after that time.

## DILIGENCE-EVIDENCE-INVENTORY

### Inputs

Require a declared evidence-request list and the supplied artifact set. Each
request row needs a stable request ID, requested artifact type, declared scope,
and whether the requester marked it not applicable. Each supplied artifact
needs identity, version/date, provenance, owner if known, and a locator.

### Procedure

1. Freeze the request-list denominator before reading the supplied artifacts.
2. Match only exact declared IDs or explicit aliases supplied by the caller.
3. For each request, emit exactly one evidence state:
   `provided`, `not-provided`, `not-applicable-as-declared`, `UNKNOWN`, or
   `CANNOT_ASSESS`.
4. Preserve provenance, versions, dates, locators, duplicate candidates, and
   contradictions. Never choose among conflicting versions.
5. When supplied facts need reconciliation, route them to
   `reconcile-cross-document-facts`; record that handoff without importing or
   pretending to execute another package in a clean install.
6. Report `request_rows_assessed / request_rows_declared`, supplied artifact
   count, unmatched supplied artifacts, and each unassessable row.

### Output fields

`request_id` · `artifact_type` · `state` · `supplied_artifact_ids` ·
`provenance` · `version_date` · `locator` · `contradiction` ·
`reconciliation_route` · `owner` · `disposition=open`

Do not decide diligence materiality, asset value, transaction terms,
approvability, acceptable risk, or go/no-go. A complete inventory is not a
complete diligence assessment.
