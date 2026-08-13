#!/usr/bin/env python3
"""Generate the published map — one page per job-model task.

The map is Layer 1 of the product: the profession made navigable, usable with no
AI and no install. It is generated from the coverage ledger, so a page cannot
claim coverage the ledger does not record.

The index is the interactive job tree: Band → Domain → Subdomain → L3. Visual
language follows the 2026-08-10 accordion (native <details>, no JavaScript).
Coverage colours are live from current_disposition — never copied from that
dated HTML, which froze at 28 covered / 54 partial / 74 nothing / 11 out of
scope. Partial and "outside v1 scope" are not live states. The two class=boundary
rows stay labelled "Outside this product" at the leaf.

Public-safety: only ledger fields reach the page — the task name, its place in
the tree, its artifact class, and how it is covered.

Site constraints this output must satisfy (scripts/check_site_gates.py):
  no JavaScript · no iframes · no external resources · no trackers ·
  lang attribute · a <main> landmark · accessible text on every link.

`--check` fails if any page is missing or stale, so a ledger edit that is not
regenerated cannot ship.
"""
from __future__ import annotations

import csv
import html
import json
import re
import sys
from collections import OrderedDict
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

BAND_COPY = {
    "A": ("Foundations",
          ("Knowledge and methods applied to everything below. Not ranked by "
           "frequency — this is substrate, not activity.")),
    "B": ("The development arc",
          "Sequential. Each domain fires at its own point in a programme's life."),
    "C": ("Cross-cutting obligations",
          "Apply at every stage of the development arc, not at one point in it."),
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
<body class="job-tree-page">
<a class="skip-link" href="#main">Skip to main content</a>
<main id="main" class="job-tree">
<p class="tree-brand"><a href="../index.html">ClinPharm PMx Skills</a> · the job map</p>
<header>
<p class="eyebrow">Coverage map · regenerated from the ledger</p>
<h1>The clinical pharmacology job</h1>
<p class="standfirst">{total} tasks across {bands} bands, {domains} domains, and {subdomains} sub-domains. Open a domain, then a sub-domain, to reach a task. Each task is coloured by whether a shipped skill actually carries it.</p>
</header>
<div class="root">
<span class="rn">ClinPharm PMx Skills</span>
<span class="tally">
<span class="t ok"><b>{carried}</b>carried</span>
<span class="t gap"><b>{uncarried}</b>nothing built</span>
</span>
<span class="rc">{total} tasks · {released} released packages · {built} built</span>
</div>
<p class="ctl-note">Native disclosure — no JavaScript. Coverage is regenerated from the ledger whenever the map is built, so a dated snapshot cannot silently become this page.</p>
{body}
<p class="tree-back"><a href="../index.html">Back to ClinPharm PMx Skills</a></p>
<footer>Generated from <code>catalog/job-model-167.tsv</code>. Skills review, reconcile, verify, structure, and flag. They never select a dose, sign off, or submit.</footer>
</main>
</body>
</html>
"""


def slug(s: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def leaf_state(row: dict[str, str]) -> tuple[str, str]:
    """Return (css-suffix, label) from live ledger fields only."""
    if row["class"] == "boundary":
        return "oos", "Outside this product"
    if row["current_disposition"] == "skill":
        return "ok", "Skill covers it"
    return "gap", "Nothing built"


def build_tree(rows: list[dict[str, str]]) -> str:
    """Accordion tree. Order follows the ledger. No JavaScript."""
    bands: OrderedDict[str, OrderedDict[str, OrderedDict[str, list]]] = OrderedDict()
    domain_no: dict[str, str] = {}
    sub_no: dict[tuple[str, str], str] = {}
    for r in rows:
        parts = r["locator"].split("/")
        domain_no[r["domain"]] = parts[1]
        sub_no[(r["domain"], r["subdomain"])] = parts[2]
        bands.setdefault(r["band"], OrderedDict()).setdefault(
            r["domain"], OrderedDict()
        ).setdefault(r["subdomain"], []).append(r)

    out: list[str] = ['<div class="tree">']
    for band, domains in bands.items():
        title, blurb = BAND_COPY[band]
        band_rows = [r for subs in domains.values() for tasks in subs.values() for r in tasks]
        n_ok = sum(1 for r in band_rows if leaf_state(r)[0] == "ok")
        n_gap = sum(1 for r in band_rows if leaf_state(r)[0] == "gap")
        n_oos = sum(1 for r in band_rows if leaf_state(r)[0] == "oos")
        n = len(band_rows)
        out.append(
            f'<div class="band"><span class="bl">Band {html.escape(band)}</span>'
            f'<span class="bn">{html.escape(title)}</span>'
            f'<span class="bd">{html.escape(blurb)}</span>'
            f'<span class="bnums"><b class="c-ok">{n_ok}</b>'
            f'<b class="c-gap">{n_gap}</b>'
            f'<b class="c-oos">{n_oos}</b>'
            f'<span class="bt">{n}</span></span></div>'
        )
        for domain, subs in domains.items():
            domain_rows = [r for tasks in subs.values() for r in tasks]
            n_ok = sum(1 for r in domain_rows if leaf_state(r)[0] == "ok")
            n_gap = sum(1 for r in domain_rows if leaf_state(r)[0] == "gap")
            n_oos = sum(1 for r in domain_rows if leaf_state(r)[0] == "oos")
            n = len(domain_rows)
            empty = " empty" if n_ok == 0 else ""
            ok_w = (100.0 * n_ok / n) if n else 0
            gap_w = (100.0 * n_gap / n) if n else 0
            oos_w = (100.0 * n_oos / n) if n else 0
            out.append(f'<details class="branch{empty}">')
            out.append("<summary>")
            out.append('<span class="tick"></span>')
            out.append(f'<span class="letter">{html.escape(domain_no[domain])}</span>')
            out.append(f'<span class="dname">{html.escape(domain)}</span>')
            out.append(
                f'<span class="bar" aria-hidden="true">'
                f'<i class="b-ok" style="width:{ok_w:.2f}%"></i>'
                f'<i class="b-gap" style="width:{gap_w:.2f}%"></i>'
                f'<i class="b-oos" style="width:{oos_w:.2f}%"></i></span>'
            )
            out.append(
                f'<span class="nums"><b class="c-ok">{n_ok}</b>'
                f'<b class="c-gap">{n_gap}</b>'
                f'<b class="c-oos">{n_oos}</b></span>'
            )
            out.append(f'<span class="n">{n}</span>')
            out.append("</summary>")
            out.append('<div class="subs">')
            for subdomain, tasks in subs.items():
                out.append('<details class="sub">')
                out.append(
                    f'<summary><span class="tick"></span>'
                    f'<span class="sn">{html.escape(sub_no[(domain, subdomain)])}</span>'
                    f'<span class="sname">{html.escape(subdomain)}</span>'
                    f'<span class="sn-count">{len(tasks)}</span></summary>'
                )
                out.append('<ul class="leaves">')
                for r in tasks:
                    state, label = leaf_state(r)
                    href = slug(r["task_L3"]) + ".html"
                    out.append(
                        f'<li class="leaf s-{state}">'
                        f'<span class="dot"></span>'
                        f'<a class="lname" href="{html.escape(href)}">'
                        f'{html.escape(r["task_L3"])}</a>'
                        f'<span class="lstate">{html.escape(label)}</span></li>'
                    )
                out.append("</ul></details>")
            out.append("</div></details>")
    out.append("</div>")
    return "\n".join(out)


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

    status: dict[str, int] = {}
    colls = sorted((ROOT / "collections").glob("*/collection.json"))
    for cf in colls:
        for s in json.loads(cf.read_text(encoding="utf-8")).get("skills", []):
            if isinstance(s, dict):
                status[s.get("status", "unknown")] = status.get(s.get("status", "unknown"), 0) + 1

    counts = {k: sum(1 for r in rows if r["class"] == k) for k in CLASS_COPY}
    carried = sum(1 for r in rows if r["current_disposition"] == "skill")
    pages["index.html"] = INDEX.format(
        released=status.get("released", 0),
        built=status.get("built", 0),
        total=len(rows),
        bands=len({r["band"] for r in rows}),
        domains=len({r["domain"] for r in rows}),
        subdomains=len({(r["band"], r["domain"], r["subdomain"]) for r in rows}),
        carried=carried,
        uncarried=len(rows) - carried,
        body=build_tree(rows),
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
          f"({carried} carried, {len(rows) - carried} open; "
          f"{counts['skill']} skills, {counts['context']} contexts, "
          f"{counts['shared-reference']} references, {counts['boundary']} boundaries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
