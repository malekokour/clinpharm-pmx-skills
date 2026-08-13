<!-- VENDORED from shared/policies/evidence-hierarchy.md at build time. Do not edit here.
     Edit the canonical source and rebuild; a freshness check compares them. -->

---
contract: evidence-hierarchy
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-04"
consumers: [review-csr-pk-consistency]
---

# Evidence hierarchy and source locators

## Precedence

When two supplied documents disagree, precedence decides which is treated as the
expected value — it never decides which is scientifically correct.

1. The **locked source output** the value derives from (analysis outputs,
   parameter datasets, statistical outputs).
2. The **pre-specified rule document** (analysis plan, protocol and its
   amendments) for conventions: units, rounding, exclusions, estimation method.
3. The **document under review**, which is the object being checked, not an
   authority about itself.
4. Any **summary or derived document**, which is never authoritative over the
   source it summarises.

A user may declare a different order for a specific task. Record the declared
order in the output; do not apply it silently.

## Locators are mandatory

Every finding carries enough location for a reviewer to open the document and
land on the exact statement without searching:

- document identity and version;
- section number and heading, or table/figure number;
- row and column where the value sits in a table;
- page number when the format provides one.

A finding without a locator is not reportable. It is indistinguishable from an
assertion, and it costs a reviewer more time to verify than to redo.

## Exact values are preserved verbatim

Numbers, units, qualifiers, negations, populations, time points and statistical
descriptors are reproduced **exactly as written**, including the original
precision and any trailing zeros.

Do not normalise, round, convert, or tidy a value on the way into a finding. A
rounding difference may itself be the defect, and a silent conversion destroys
the evidence that would show it.

Where a comparison requires a tolerance — because the two documents legitimately
use different precision — apply the tolerance rule from the analysis plan and
report the rule that was applied alongside the finding.

## Contradictions are preserved, not resolved

When sources conflict, the output records **both statements with both
locators**, and marks the item as a contradiction for human resolution.

Never silently harmonise two sources. Never pick the one that looks more
plausible. Never average them. Never report only the one that matches the
document under review.

The contradiction is the finding. Resolving it is the reviewer's job.

## Staleness

A value inherited from a superseded document version is a distinct finding
class from a numeric mismatch, and is reported as such: the current document, the
version it appears to reflect, and the version that is authoritative.
