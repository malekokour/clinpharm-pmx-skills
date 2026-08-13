#!/usr/bin/env python3
"""Generate the published map — one page per job-model task.

The map is Layer 1 of the product: the profession made navigable, usable with no
AI and no install. It is generated from the coverage ledger, so a page cannot
claim coverage the ledger does not record.

Public-safety: the ledger lives in the private workspace, but only four fields
per row reach the page — the task name, its place in the tree, its artifact
class, and how it is covered. No private material crosses the boundary, and the
script fails rather than guessing if the ledger is unreachable.

Site constraints this output must satisfy (scripts/check_site_gates.py):
  no JavaScript · no iframes · no external resources · no trackers ·
  lang attribute · a <main> landmark · accessible text on every link.

`--check` fails if any page is missing or stale, so a ledger edit that is not
regenerated cannot ship.
"""
from __future__ import annotations

import csv
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "map"
LEDGER = ROOT / "catalog" / "job-model-167.tsv"

CLASS_COPY = {
    "skill": ("Skill", "A workflow you can run. The router selects it."),
    "context": ("Context", ("Not a workflow. It attaches to whichever skill you are "
                           "running and changes how that skill interprets your data.")),
    "shared-reference": ("Shared reference", ("Criteria other skills read. It has no "
                                             "workflow of its own.")),
    "boundary": ("Outside this product", ("Real professional work, deliberately not "
                                         "covered here. Named rather than hidden.")),
}

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — ClinPharm PMx Skills</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<a href="#main">Skip to main content</a>
<main id="main">
<nav aria-label="Breadcrumb"><p>{crumb}</p></nav>
<h1>{title}</h1>
<p>{class_note}</p>
<h2>Where this sits</h2>
<dl>
<dt>Band</dt><dd>{band}</dd>
<dt>Domain</dt><dd>{domain}</dd>
<dt>Subdomain</dt><dd>{subdomain}</dd>
<dt>Kind</dt><dd>{class_label}</dd>
</dl>
<h2>How it is covered</h2>
<p>{coverage}</p>
<h2>What a skill will not do</h2>
<p>Skills review, reconcile, verify, structure and flag. A qualified human
decides, approves, signs off, submits and acts. That boundary does not move.</p>
<p><a href="index.html">Back to the map</a></p>
</main>
</body>
</html>
"""

INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The map — ClinPharm PMx Skills</title>
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<a href="#main">Skip to main content</a>
<main id="main">
<h1>The map of clinical pharmacology and pharmacometrics</h1>
<p>{total} tasks across {bands} bands, {domains} domains and {subdomains}
subdomains. Every one is either covered by something that runs, or named as work
this product deliberately does not do. Open a domain, then a subdomain, to reach
an L3 task page.</p>
<p>{skills} are skills. {contexts} are contexts that attach to a skill rather
than running on their own. {refs} are shared references other skills read.
{bounds} are outside this product and say so.</p>
<h2>What is built today</h2>
<p>The map above describes the profession. This is what currently ships against
it, regenerated from the collections rather than written by hand:</p>
<ul>
<li><strong>{released} released</strong> — the evaluation gate passed</li>
<li><strong>{built} built</strong> — the package validates; the gate has not run</li>
<li><strong>{packages} packages</strong> across {colls} collections</li>
</ul>
<p>The gap between {packages} and {skills} is the work remaining. It is stated
rather than implied, and no date is attached to it.</p>
{body}
<p><a href="../index.html">Back to ClinPharm PMx Skills</a></p>
</main>
</body>
</html>
"""


def slug(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def main() -> int:
    check = "--check" in sys.argv
    if not LEDGER.exists():
        print(f"FAILED: ledger not reachable at {LEDGER}. The map is generated from "
              "it; refusing to emit pages from nothing.")
        return 1

    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8"), delimiter="\t"))
    if len(rows) != 167:
        print(f"FAILED: ledger has {len(rows)} rows, expected 167")
        return 1

    pages: dict[str, str] = {}
    for r in rows:
        label, note = CLASS_COPY[r["class"]]
        cov = r["coverage_via"]
        cov_txt = ("A skill of its own." if cov == "self"
                   else html.escape(cov).replace("carried by L3: ",
                                                 "Carried by the skill for: "))
        pages[f"{slug(r['task_L3'])}.html"] = PAGE.format(
            title=html.escape(r["task_L3"]),
            crumb=html.escape(f"Band {r['band']} › {r['domain']} › {r['subdomain']}"),
            band=html.escape(r["band"]), domain=html.escape(r["domain"]),
            subdomain=html.escape(r["subdomain"]),
            class_label=label, class_note=note, coverage=cov_txt,
        )

    # Nested accordion: Band → Domain → Subdomain → L3 links.
    # Uses <details>/<summary> only — no JavaScript (site gates).
    bands: dict[str, dict[str, dict[str, list]]] = {}
    for r in rows:
        bands.setdefault(r["band"], {}).setdefault(r["domain"], {}).setdefault(
            r["subdomain"], []
        ).append(r)
    body: list[str] = []
    for band, domains in bands.items():
        body.append(f'<section class="map-band" aria-label="Band {html.escape(band)}">')
        body.append(f"<h2>Band {html.escape(band)}</h2>")
        for domain, subs in domains.items():
            n_tasks = sum(len(tasks) for tasks in subs.values())
            body.append('<details class="map-domain">')
            body.append(
                f"<summary><span class=\"map-label\">{html.escape(domain)}</span>"
                f"<span class=\"map-count\">{n_tasks} tasks</span></summary>"
            )
            for subdomain, tasks in subs.items():
                body.append('<details class="map-subdomain">')
                body.append(
                    f"<summary><span class=\"map-label\">{html.escape(subdomain)}</span>"
                    f"<span class=\"map-count\">{len(tasks)}</span></summary>"
                )
                body.append("<ul>")
                for r in tasks:
                    body.append(
                        f'<li><a href="{slug(r["task_L3"])}.html">'
                        f'{html.escape(r["task_L3"])}</a> — {html.escape(r["class"])}</li>'
                    )
                body.append("</ul>")
                body.append("</details>")
            body.append("</details>")
        body.append("</section>")

    # Live status, read from the collections — the source of record for package
    # status. Never typed: a hand-written tally is the defect this product's status
    # vocabulary exists to prevent.
    import json
    status: dict[str, int] = {}
    colls = sorted((ROOT / "collections").glob("*/collection.json"))
    for cf in colls:
        for s in json.loads(cf.read_text(encoding="utf-8")).get("skills", []):
            if isinstance(s, dict):
                status[s.get("status", "unknown")] = status.get(s.get("status", "unknown"), 0) + 1

    counts = {k: sum(1 for r in rows if r["class"] == k) for k in CLASS_COPY}
    pages["index.html"] = INDEX.format(
        released=status.get("released", 0),
        built=status.get("built", 0),
        packages=sum(status.values()),
        colls=len(colls),
        total=len(rows), bands=len({r["band"] for r in rows}),
        domains=len({r["domain"] for r in rows}),
        subdomains=len({r["subdomain"] for r in rows}),
        skills=counts["skill"], contexts=counts["context"],
        refs=counts["shared-reference"], bounds=counts["boundary"],
        body="\n".join(body),
    )

    if check:
        stale = [n for n, t in pages.items()
                 if not (OUT / n).exists() or (OUT / n).read_text(encoding="utf-8") != t]
        extra = [p.name for p in OUT.glob("*.html")] if OUT.exists() else []
        extra = [n for n in extra if n not in pages]
        if stale or extra:
            print(f"FAILED: {len(stale)} stale/missing page(s), {len(extra)} orphaned")
            for n in (stale + extra)[:8]:
                print(f"  - {n}")
            print("  regenerate: python scripts/build_map_site.py")
            return 1
        print(f"PASS: map current — {len(pages) - 1} task pages + index, "
              f"from {len(rows)} ledger rows")
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.glob("*.html"):
        if p.name not in pages:
            p.unlink()
    for n, t in pages.items():
        (OUT / n).write_text(t, encoding="utf-8")
    print(f"wrote {len(pages) - 1} task pages + index into site/map/ "
          f"({counts['skill']} skills, {counts['context']} contexts, "
          f"{counts['shared-reference']} references, {counts['boundary']} boundaries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
