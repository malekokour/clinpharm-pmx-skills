---
contract: output-states
version: "1.0"
owner: Malek Okour
reviewed: "2026-08-04"
consumers: [review-csr-pk-consistency]
---

# Output states

Three markers exist so that missing evidence is never filled by invention. Use
the exact tokens; they are greppable and they appear in evaluations.

| Marker | Means | Use when |
|---|---|---|
| `NEEDS_INPUT` | The check is possible, but a required input is absent | The user can supply the missing artefact and the check will then run |
| `UNKNOWN` | The evidence is present but does not determine an answer | The documents genuinely do not say, and no amount of re-reading will settle it |
| `CANNOT_ASSESS` | The check cannot be performed at all in this configuration | Extraction failed, the format is unsupported, or the check is out of scope for the selected mode |

## Rules

1. **A marker is a result, not a failure.** Emit it plainly, in the same output
   structure as any other finding, with the same location fields. Do not bury it
   in prose and do not apologise for it.

2. **Every marker names what would resolve it.** `NEEDS_INPUT: Table 14.2.4 not
   supplied — dose-proportionality claim cannot be reconciled` is useful.
   `NEEDS_INPUT` alone is not.

3. **Never substitute a plausible value.** If a number is required and absent,
   the answer is a marker, not an estimate, not a typical value, and not a value
   carried over from a similar document.

4. **Never convert a marker into a conclusion.** "No discrepancy found" and
   "could not check" are different results. Reporting the second as the first is
   the most consequential error this contract prevents.

5. **Coverage is stated numerically.** Any output that reconciles values reports
   how many were checked and how many could not be, so a reader can tell the
   difference between a clean document and an unread one. A completeness claim
   without a denominator is unfalsifiable.

## Mechanical finding versus scientific interpretation

A deterministic check produces a **mechanical finding**: two strings differ, a
unit is inconsistent with the stated convention, a ratio does not recompute.

A mechanical finding is never reported as a scientific conclusion. The output
distinguishes them explicitly:

- *mechanical* — "Synopsis states 412 ng·h/mL; Table 14.2.1 states 481 ng·h/mL.
  Values differ."
- *not permitted* — "The synopsis value is wrong." / "This is a minor issue."
  / "The correct value is 481."

Which value is correct, and whether the difference matters, are scientific
judgements reserved for a qualified human reviewer.
