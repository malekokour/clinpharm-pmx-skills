# EU SmPC Clinical Pharmacology Section Review

**Give it a draft Summary of Product Characteristics and the studies behind it. It
returns which parts of section 5.2 the QRD structure expects and the draft is
missing, every number in 4.2, 4.5, 5.2 and 4.4 that no supplied source actually
supports, and — the check that only exists in the EU — every dose instruction in
4.2 with no exposure basis in 5.2, and every substantial exposure change in 5.2
that no section acts on.**

A qualified clinical pharmacologist and the labelling owner decide what to do
about each one.

## SmPC text is binding. This reviews it; it never writes it.

It does not draft, reword, or redline. It takes **no position in a labelling
negotiation** — not on what a rapporteur will accept, not on what to concede, not
on how to answer a list of questions. Findings quote only the span needed to
locate them.

A tool that proposes SmPC wording has started authoring a legally binding
document on a marketing authorisation holder's behalf, on evidence it cannot
fully see, in a procedure it is not party to.

## The problem this exists for

The USPI concentrates clinical pharmacology in Section 12. The SmPC spreads it
out: pharmacokinetic properties in 5.2, the posology that follows from them in
4.2, interactions in 4.5, and warnings with a quantitative basis in 4.4.

Those sections are frequently drafted by different people, revised on different
cycles, and reviewed section by section. The failure mode is specific and
familiar: **5.2 gains a renal exposure finding at a data cut and 4.2 never gains
the corresponding instruction** — or 4.2 carries a hepatic dose reduction whose
supporting exposure statement was edited out of 5.2 two revisions ago.

Neither is visible reading one section at a time, and neither is what a US-label
checker looks for.

## What you get

| Output | Contents |
|---|---|
| Conformance register | One row per finding, with severity, locator, the rule applied and the detection path |
| Claim-to-data traceability matrix | Every statement against the source that supports it — or `untraced`, stated plainly |
| **Cross-section consistency table** | Every 4.2 / 4.5 instruction against its 5.2 basis, in **both** directions |
| Structure deviation report | Expected 5.2 subsections and order against observed, citing the QRD template version you supplied |
| Human-review record | Disposition log with named owners; every disposition arrives `open` |

## What it needs from you

The draft SmPC alone gets you a structure pass and nothing else — and the skill
says so rather than implying more.

The valuable output needs the sources: CSRs and NCA tables, statistical outputs
for anything quoted with an interval, the popPK / exposure–response / PBPK
reports, and Module 2.7.2. Plus two things people forget:

- **which document version is authoritative** for each value class — tracing a
  statement to a superseded output produces confident findings that are pure
  artefacts;
- **which QRD template version** you are working to — structure expectations are
  template-version dependent, and the skill will mark every structure finding
  `NEEDS_INPUT` rather than check against a version it guessed.

## What it will not do

Decide whether an exposure change warrants a dose modification. Decide which of
two conflicting values is right. Predict what an assessor will accept. Write a
single word of SmPC text.

An unactioned exposure change in 5.2 may be perfectly correct — the change may
not warrant an instruction. The skill reports that the pair is not stated. Whether
it should be is a qualified reviewer's call.

## Status

**`built`, not `released`.** No benchmark run has been published for this skill,
so no performance claim should be made about it. See the repository's `built` vs
`released` definitions — the distinction is load-bearing here.

## Related skills

| If you actually want | Use |
|---|---|
| The US label's Section 12 | `review-uspi-section-12-content` |
| The CTD 2.7.2 submission summary | `review-ctd-272-content` |
| The PK sections of a CSR | `review-csr-pk-consistency` |
| One fact traced across protocol, CSR, 2.7.2 and label | `reconcile-cross-document-facts` |
| Evidence mapped to an agency question | `map-agency-question-evidence` |

Licensed MIT.
