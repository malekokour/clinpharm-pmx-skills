# Start here

**For clinical pharmacologists and pharmacometricians. No software background
assumed. You do not need GitHub, a terminal, or an install.**

If you have ever thought *"I should check whether the numbers in this report
actually agree with the dataset"* — that is what this is for.

---

## What this actually is, in one paragraph

It is a set of **written instructions for an AI assistant**. Each one teaches the
assistant to review a particular kind of clinical pharmacology document — a
renal impairment section, a DDI package, an NCA report — the way a careful
colleague would: check the numbers against their source, flag what disagrees,
and say where it found each thing.

**It does not decide anything.** It reports what looks wrong and points you at
the page. You decide whether it is right.

---

## Try it in 60 seconds — no install, no account, nothing to set up

You need: a chat window with an AI assistant you already use (Claude, ChatGPT,
Copilot, Gemini — any of them), and a document to check.

### Step 1 — open one instruction file

[**`skills/verify-nca-outputs/PASTE.md`**](../skills/verify-nca-outputs/PASTE.md)

Click that link. You will see a page of text. That is all it is — text.

### Step 2 — copy all of it

Select everything on the page and copy it.

### Step 3 — paste it into your chat window

Paste, and send. The assistant now knows how to do this particular review.

### Step 4 — attach your document and ask

Attach the file you want checked, then type something like:

> Verify the NCA report against the parameter dataset and the analysis plan.
> Report every finding with its locator. Do not re-derive anything.

**That is the whole thing.** No account, no download, no command line.

> **Want to try it without using your own document first?**
> Four example files are here:
> [`examples/verify-nca-outputs/inputs/`](../examples/verify-nca-outputs/inputs/).
> They are synthetic — invented for testing, not from any real study — and they
> contain deliberate errors so you can see what the tool catches.

### What it should find in the example

| It catches | Why that matters |
|---|---|
| A reported `AUC` that is 8% off the dataset it came from | A transcription error that survived review |
| A `CL/F` printed in the wrong unit — off by 1000-fold | The classic unit swap |
| An excluded subject the analysis plan does not permit | A protocol deviation hiding in a table |

And it will **refuse** to tell you which of two conflicting values is
scientifically correct, refuse to pick a dose, and refuse to rerun the analysis.
That is deliberate. Those are your job.

---

## Using more than one review

There are **151** of these instruction files, one per task — hepatic impairment,
DDI evidence, CTD 2.7.2 content, USPI Section 12, and so on.

**Every one works the same way as above.** The path is always
`skills/<name>/PASTE.md`.

**Not sure which one you need?** There is a router: describe your task in plain
words and it names the right skill. See
[`skills/library-router/`](../skills/library-router/).

---

## When you outgrow copy-and-paste

If you find yourself pasting several times a day, it is worth loading the whole
library into your AI tool once, so it is always available. That takes a download
and a couple of commands.

Steps for each tool are in [`docs/HOSTS.md`](HOSTS.md). If those instructions
lose you at any point, **that is a bug in our documentation** —
[tell us](https://github.com/malekokour/clinpharm-pmx-skills/issues) and it gets
fixed.

---

## Words you will see, in plain terms

You do not need these to use the tool. They are here so nothing on this site
stops you.

| Word | What it means here |
|---|---|
| **Skill** | One instruction file teaching an assistant one review task. A folder with a `SKILL.md` inside |
| **`SKILL.md`** | The instruction file itself. Ordinary text you can read |
| **`PASTE.md`** | The same instructions, formatted to paste straight into a chat |
| **Repository / repo** | The folder holding all of this, stored on GitHub |
| **GitHub** | A website where files like this are published. You can read everything without an account |
| **Clone** | Download a copy of the whole folder to your computer |
| **Router** | A helper that reads your request and names the right skill |
| **Fixture** | A fake document, written by us, with known errors in it — used for testing |
| **Eval** | A test that checks whether a skill finds the errors a fixture contains |
| **`released` / `built`** | How finished a skill is. See [`VALIDATION.md`](../VALIDATION.md) — the difference is deliberate and it matters |

---

## The question you should be asking

**"Was this validated, or did an AI just write it?"**

Fair, and answered in full at [**`VALIDATION.md`**](../VALIDATION.md). The short
version: drafted with AI assistance, reviewed by a practising clinical
pharmacologist, checked by 46 automated gates — and **not yet scored against
real regulatory documents**. That scoring is underway against public FDA reviews
anyone can download, and the results will be published including the misses.

**Nothing here is clinically validated, and nothing here will claim to be.**

---

## Safety, briefly

- **Do not paste confidential material into a public AI chat window.** Use only
  what your organisation permits in that environment. This is your call and your
  responsibility, not the tool's.
- **Check every finding.** The tool reports a locator for each one so you can go
  and look. That is the point of the locator.
- **It is not a reviewer.** It is a way of noticing things faster. A qualified
  human decides, approves, signs, and submits.

---

**Stuck at any step?** That is worth reporting —
[open an issue](https://github.com/malekokour/clinpharm-pmx-skills/issues) and
say which step lost you. Instructions that only work for people who already know
how are not instructions.
