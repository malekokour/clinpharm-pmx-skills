# Validation — what has been tested, and what has not

> Someone asked, publicly, on the day this library launched:
>
> *"Were these skills created by AI, or have they been validated by humans —
> tested with actual reports, analyses, datasets?"*
>
> **It is a fair question and it deserves a straight answer.** This page is that
> answer. It will be updated as results come in, including the unflattering ones.

## The short version

**These skills were drafted with AI assistance and reviewed by a practising
clinical pharmacologist.** The packaging, structure, and stated boundaries are
checked automatically on every change. Their *behaviour on real regulatory
documents* is being measured now, against public documents anyone can download,
and results are published here either way.

**Nothing here is clinically validated, and nothing here will claim to be.**

## What "validated" can mean, and which one applies

Four different claims get blurred together under one word. They are kept apart
here because the difference is the entire point of the project.

| Layer | The claim | Status | Evidence |
|---|---|---|---|
| **1 · Package validity** | The package is well-formed, installs cleanly, links resolve, and it declares what it refuses | ✅ **Verified** | 32 automated gates on every change. **29 have been deliberately broken to confirm they actually fail** — see [`scripts/canary_gates.py`](scripts/canary_gates.py) |
| **2 · Diagnostic evidence** | Given a document with known planted errors, the skill finds them | ⚠️ **Partial** | Synthetic fixtures with enumerated defects. **The fixtures are synthetic by construction** — that is a real limitation, not a detail |
| **3 · Real-document performance** | Given a real regulatory document, the skill finds what a real expert found | 🔬 **In progress** | Corpus fetched, protocol frozen — see below |
| **4 · Clinical validation** | Fit to support a regulatory or clinical decision | 🔴 **Not claimed. Ever.** | A human decides. The tool reports and refuses |

If you only read one row, read the last one. **No output from this library is a
decision.** Every skill states, in its own contract, that it will not select a
dose, resolve a scientific disagreement, sign off, or submit.

## Layer 3 — how real-document validation is being done

### The corpus is public, and that is deliberate

Every document is one **you can download yourself**, free, without a login:

| Source | What it provides |
|---|---|
| [Drugs@FDA](https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files) — Clinical Pharmacology & Biopharmaceutics Reviews | Real PK tables, real dose rationales, real reviewer findings |
| FDA Integrated / Multi-discipline Reviews | Real exposure-response, DDI, organ-impairment assessments |
| [EMA Clinical Data Publication](https://clinicaldata.ema.europa.eu/) (Policy 0070) | **Full redacted Clinical Study Reports** |
| [Health Canada — Public Release of Clinical Information](https://clinical-information.canada.ca/) | **Full redacted CSRs, protocols, statistical analysis plans** |
| Published PopPK / exposure-response papers with supplements | Real datasets, real model outputs |

**Why public rather than internal?** Because a validation result you cannot
check is not a result. If this page said *"we tested it against a confidential
CSR and it did well"*, you would have to take my word for it. Instead: fetch the
same PDF, run the same skill, compare.

```bash
python3 scripts/fetch_validation_corpus.py          # download the corpus
python3 scripts/fetch_validation_corpus.py --verify # confirm identical bytes
```

Every document's **SHA-256 is recorded** in
[`validation/corpus-manifest.json`](validation/corpus-manifest.json). The PDFs
themselves are not committed — they belong to the regulators who published them,
and the digest is what makes the result reproducible.

**Not in the corpus, ever:** anything from an employer, any sponsor-confidential
draft, any unpublished submission, any patient-level data that is not a public
synthetic or CDISC pilot dataset.

### The answer key was not written by us

This is the part that makes the result worth anything.

**An FDA Clinical Pharmacology review is already an expert's written findings**
about the study it reviews. So the key a skill is scored against was written by
an FDA reviewer, published by the FDA, and is independent of both the tool and
its author. Nobody involved in building this library gets to decide what counts
as a correct finding.

That removes the objection that sinks most self-reported evaluations: *you
graded your own homework.* Here, the grader is a regulator, and the grading was
done years before this library existed.

### Two stages, in this order

| Stage | Who | Question it answers |
|---|---|---|
| **1 · Automated scoring** | The tool, against the published review | Does it find what the reviewer found? Recall, precision, and **every miss**, with denominators |
| **2 · Independent human trial** | A practising clinical pharmacologist, on documents stage 1 never used | Is the output actually *usable*? Would a professional trust it? |

Stage 2 runs on **held-back documents**, and the reviewer sees the skill's output
before seeing any score. A reviewer who already knows the answer is not testing —
they are confirming.

### Current state

| | |
|---|---:|
| Documents fetched and verified | **5** |
| Total text under test | **1,703,405 characters** |
| Skills scored so far | **0** |
| Results published | **none yet** |

**Scoring has not started.** When it does, the misses are published with the
hits. A library that only reports its successes tells you nothing about when to
trust it — and knowing when *not* to trust a tool is worth more than knowing
when to.

## What Layer 1 actually covers

So "automated checks pass" is not mistaken for "the science is right":

- Every package's structure, frontmatter, and links resolve
- Every package installs standalone from a clean extraction
- No machine-specific paths, no contact details, no patient-identifiable field
  names, no prompt-injection shapes — scanned across the whole published tree
- Every stated count on a public page matches its source of record
- The published site makes **no third-party requests and sets no cookies** —
  verified against the served bytes, not the local files

And, unusually: **the checks themselves are tested.** 29 of the 32 gates have had
a defect deliberately planted to confirm they go red for the right reason, then
removed to confirm they go green again. Two gates are documented as *not*
currently able to fail — both are recorded as defects rather than quietly
excused.

## Honest limitations

- **The synthetic fixtures are synthetic.** They were written to contain the
  errors the skill looks for, which is a weaker test than a document that was
  never written with the tool in mind.
- **The evaluation suite has three open blocker findings** against it: assertions
  that are phrase-brittle, a suite that does not discriminate a good run from a
  baseline, and thresholds that are not measurable. It is **frozen** until those
  are fixed, and no promotion claim rests on it.
- **`released` does not mean what it might sound like.** It means the package
  passed the structural gates and its assigned qualification route. It does not
  mean clinical validation, and it does not mean the evaluation suite qualified
  its behaviour.
- **Model behaviour varies.** The same skill, the same document, a different
  model or a different day can produce different findings. That is a property of
  the technology, and any evaluation that reports a single number without
  repeated trials is overstating its certainty.

## Questions this page should answer

**Was this made by AI?**
Drafted with AI assistance, reviewed by a human clinical pharmacologist, and
checked by 32 automated gates. The domain content — what to look for in a renal
impairment section, what makes a dose rationale sound — comes from a
practitioner.

**Has it been tested on real documents?**
The corpus is fetched and the protocol is frozen. Scoring has not started.
When it has, results appear on this page including the failures.

**Can I trust it for regulatory work?**
Not as a decision-maker, and it is designed not to be one. Use it to find things
worth checking, then check them. Every finding it reports carries a locator so
you can go and look.

**How do I check it myself?**
Fetch the corpus with the command above, take any skill, run it on a document,
and compare with what the FDA reviewer wrote. That is exactly the test being run
here, and there is nothing stopping you running it independently.

---

*This page changes as results arrive. If it ever reads as more confident than
the evidence supports, that is a defect —
[open an issue](https://github.com/malekokour/clinpharm-pmx-skills/issues).*
