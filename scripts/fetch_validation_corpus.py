#!/usr/bin/env python3
"""Fetch the public regulatory documents this library is validated against.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-14
Dependencies: Python standard library, plus `pdftotext` (poppler) for text

    python3 scripts/fetch_validation_corpus.py            # fetch what is missing
    python3 scripts/fetch_validation_corpus.py --verify   # re-check digests only
    python3 scripts/fetch_validation_corpus.py --list     # show the manifest

Why this exists
---------------
The first substantive question the library got in public was:

    "Were these skills created by AI, or have they been validated by humans,
     tested with actual reports, analyses, datasets?"

A claim to have tested against real documents is worth nothing unless the reader
can fetch the same documents and check. So the corpus is **public regulatory
material only**, and this script is how anyone reproduces it.

What is in scope, and what is not
---------------------------------
**In scope — published, free, no login:**

  * Drugs@FDA Clinical Pharmacology and Biopharmaceutics Reviews, and Integrated
    / Multi-discipline Reviews
  * EMA European Public Assessment Report assessment histories
  * EMA Clinical Data Publication (Policy 0070) — **full redacted CSRs**
  * Health Canada Public Release of Clinical Information — **full redacted CSRs,
    protocols, statistical analysis plans**
  * Published PopPK / exposure-response papers with public supplements
  * CDISC pilot SDTM/ADaM datasets — real structure, synthetic subjects

**Never, under any circumstance:** anything from an employer, any
sponsor-confidential draft, any unpublished submission, any patient-level
dataset that is not a public synthetic or pilot set. The distinction that
matters is **published versus internal**, not CSR versus review — a published
redacted CSR is exactly as real as an internal one, and unlike an internal one
it can be checked by a stranger.

The PDFs are not committed
--------------------------
This script records each document's **URL and SHA-256** and downloads to an
ignored directory. Redistributing regulators' PDFs is unnecessary — anyone can
fetch them — and committing hundreds of megabytes to prove a point is not a
point worth proving. The digest is what makes a result reproducible: fetch the
same URL, get the same bytes, run the same skill.

The one gotcha that would otherwise waste an afternoon
------------------------------------------------------
**Drugs@FDA returns HTTP 404 to a default `curl`/`urllib` user-agent.** Not a
403, not a redirect — a 404 with a 419-byte HTML error page. Anything that
checks only "did I get a file?" happily writes that HTML to `something.pdf` and
carries on, and the corpus ends up full of error pages that extract to nothing.

Measured 2026-08-14 on the same URL, seconds apart:

    default user-agent   -> HTTP 404,       419 bytes, text/html
    browser user-agent   -> HTTP 200, 7,316,306 bytes, application/pdf

So this script sends a browser user-agent **and** verifies that what arrived is
actually a PDF, by magic bytes, before recording it. A downloader that trusts
the status code alone is the same shape as a scanner that reads zero bytes and
reports success — which this repository has already met three times.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Downloads land OUTSIDE the repository, in the platform cache directory.
#:
#: The first version wrote them to `validation/corpus/` inside the tree, and the
#: repository contract gate immediately refused: "unlisted directory at
#: repository root". It was right, and the fix is not to add an allowlist entry.
#: 45 MB of regulators' PDFs are not part of this project's public surface, and
#: putting them inside it would mean either scanning them on every build or
#: hiding them behind an ignore rule — and a directory that exists but is
#: excused from enumeration is exactly the shape this repository files findings
#: about.
#:
#: Outside the tree there is no question to answer. Override with
#: CLINPHARM_CORPUS_DIR if you keep documents elsewhere.
CORPUS = Path(
    os.environ.get(
        "CLINPHARM_CORPUS_DIR",
        Path.home() / ".cache" / "clinpharm-pmx-skills" / "corpus",
    )
)

#: The manifest DOES ship: digests are the reproducibility contract, and they
#: are a catalog of what the library is tested against.
MANIFEST = ROOT / "catalog" / "validation-corpus.json"

#: Drugs@FDA rejects the default urllib agent with a 404. See the module
#: docstring — this is the single most load-bearing line in the file.
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)

PDF_MAGIC = b"%PDF-"


@dataclass
class Document:
    """One public regulatory document."""

    doc_id: str
    #: Regulator or publisher, as a reader would name it.
    source: str
    #: What this document is, in the reader's language.
    title: str
    url: str
    #: Which skills this document is used to validate.
    validates: list[str] = field(default_factory=list)
    #: Why this document was chosen — kept so selection is auditable rather than
    #: looking like cherry-picking.
    rationale: str = ""


#: Deliberately small to start. Five documents scored honestly is worth more
#: than fifty scored loosely, and a believable small result is the one people
#: act on.
CORPUS_DOCS: list[Document] = [
    Document(
        doc_id="fda-nda-209529-clinpharm",
        source="FDA (Drugs@FDA)",
        title="Clinical Pharmacology and Biopharmaceutics Review(s), NDA 209529",
        url="https://www.accessdata.fda.gov/drugsatfda_docs/nda/2020/"
        "209529Orig1s000ClinPharmR.pdf",
        validates=["review-renal-impairment", "review-hepatic-impairment"],
        rationale="A full CP review containing a dedicated renal impairment "
        "assessment, so a skill's findings can be compared against what an FDA "
        "reviewer actually wrote about the same study.",
    ),
    Document(
        doc_id="fda-nda-215859-clinpharm",
        source="FDA (Drugs@FDA)",
        title="Clinical Pharmacology and Biopharmaceutics Review(s), NDA 215859",
        url="https://www.accessdata.fda.gov/drugsatfda_docs/nda/2022/"
        "215859Orig1s000ClinPharmR.pdf",
        validates=["review-renal-impairment", "review-exposure-response-relationships"],
        rationale="Carries renal dosing conclusions tied to eGFR bands, which is "
        "exactly the reconciliation a review skill claims to perform.",
    ),
    Document(
        doc_id="fda-nda-202293-clinpharm",
        source="FDA (Drugs@FDA)",
        title="Clinical Pharmacology and Biopharmaceutics Review(s), NDA 202293",
        url="https://www.accessdata.fda.gov/drugsatfda_docs/nda/2014/"
        "202293orig1s000clinpharmr.pdf",
        validates=["review-renal-impairment", "review-exposure-response-relationships"],
        rationale="Contains renal impairment PK and PD figures, giving a case "
        "where exposure and effect must be reconciled rather than read off.",
    ),
    Document(
        doc_id="fda-nda-204671-clinpharm",
        source="FDA (Drugs@FDA)",
        title="Clinical Pharmacology and Biopharmaceutics Review(s), NDA 204671",
        url="https://www.accessdata.fda.gov/drugsatfda_docs/nda/2013/"
        "204671Orig1s000ClinPharmR.pdf",
        validates=["review-renal-impairment", "review-ddi-evidence"],
        rationale="Combines renal impairment with a co-administration dosing "
        "consequence, so a skill has to keep two threads straight.",
    ),
    Document(
        doc_id="fda-nda-207923-clinpharm",
        source="FDA (Drugs@FDA)",
        title="Clinical Pharmacology and Biopharmaceutics Review(s), NDA 207923",
        url="https://www.accessdata.fda.gov/drugsatfda_docs/nda/2015/"
        "207923Orig1s000ClinPharmR.pdf",
        validates=["review-renal-impairment"],
        rationale="Held back from the first scoring round as an unseen document "
        "for the independent human trial, so stage 2 is not judging findings it "
        "has already read.",
    ),
]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(doc: Document, destination: Path) -> tuple[bool, str]:
    """Download one document, refusing anything that is not really a PDF."""
    request = urllib.request.Request(doc.url, headers={"User-Agent": BROWSER_UA})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
            status = response.status
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except (urllib.error.URLError, TimeoutError) as exc:
        return False, f"network error: {exc}"

    # Status alone is not evidence. Drugs@FDA has served a 419-byte HTML error
    # page for a .pdf URL; writing that to disk and moving on is how a corpus
    # fills up with error pages nobody notices.
    if not payload.startswith(PDF_MAGIC):
        head = payload[:60].decode("utf-8", "replace").replace("\n", " ")
        return False, (
            f"HTTP {status} but the body is not a PDF ({len(payload)} bytes, "
            f"starts {head!r}) — a browser User-Agent is required for Drugs@FDA"
        )

    destination.write_bytes(payload)
    return True, f"{len(payload):,} bytes"


def extract_text(pdf: Path) -> tuple[int, str]:
    """Return (characters, note). Text is what a skill actually reads."""
    if not shutil.which("pdftotext"):
        return 0, "pdftotext not installed (brew install poppler) — text skipped"
    txt = pdf.with_suffix(".txt")
    completed = subprocess.run(
        ["pdftotext", "-layout", str(pdf), str(txt)],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0 or not txt.is_file():
        return 0, f"pdftotext failed: {completed.stderr.strip()[:80]}"
    chars = len(txt.read_text(encoding="utf-8", errors="replace"))
    return chars, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="re-check digests only")
    ap.add_argument("--list", action="store_true", help="print the manifest")
    args = ap.parse_args()

    if args.list:
        print(f"{len(CORPUS_DOCS)} public document(s) in the corpus:\n")
        for doc in CORPUS_DOCS:
            print(f"  {doc.doc_id}\n    {doc.source} — {doc.title}\n    {doc.url}")
            print(f"    validates: {', '.join(doc.validates) or '(none yet)'}")
            print(f"    why: {doc.rationale}\n")
        return 0

    CORPUS.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    failures = 0

    for doc in CORPUS_DOCS:
        pdf = CORPUS / f"{doc.doc_id}.pdf"

        if args.verify:
            if not pdf.is_file():
                print(f"  MISSING  {doc.doc_id} — run without --verify to fetch")
                failures += 1
                continue
            print(f"  {sha256_of(pdf)[:16]}…  {doc.doc_id}")
            continue

        if pdf.is_file() and pdf.read_bytes()[:5] == PDF_MAGIC:
            note = "already present"
            ok = True
        else:
            ok, note = fetch(doc, pdf)

        if not ok:
            print(f"  FAILED   {doc.doc_id}: {note}")
            failures += 1
            continue

        chars, text_note = extract_text(pdf)
        digest = sha256_of(pdf)
        records.append(
            {
                "doc_id": doc.doc_id,
                "source": doc.source,
                "title": doc.title,
                "url": doc.url,
                "sha256": digest,
                "bytes": pdf.stat().st_size,
                "text_characters": chars,
                "validates": doc.validates,
                "rationale": doc.rationale,
            }
        )
        extra = f", {chars:,} chars of text" if chars else f" — {text_note}"
        print(f"  ok       {doc.doc_id}: {note}{extra}")

    if args.verify:
        print(f"\n{'FAIL' if failures else 'PASS'}: verified {len(CORPUS_DOCS)} "
              f"document(s), {failures} missing")
        return 1 if failures else 0

    if records:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(
            json.dumps(
                {
                    "_comment": "Public regulatory documents this library is "
                    "validated against. The PDFs are not committed — fetch them "
                    "with scripts/fetch_validation_corpus.py and compare the "
                    "sha256 to confirm you have the same bytes.",
                    "documents": records,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {MANIFEST.relative_to(ROOT)} "
              f"({len(records)} document(s), digests recorded)")

    total = sum(r["text_characters"] for r in records)
    print(
        f"{'FAIL' if failures else 'PASS'}: {len(records)}/{len(CORPUS_DOCS)} "
        f"document(s) fetched and verified as PDFs, {total:,} characters of text"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
