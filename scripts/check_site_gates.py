#!/usr/bin/env python3
"""No-tracking and accessibility gates for the static site.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-11
Dependencies: Python standard library only

Why these are release gates (PS-D027 D-L13)
-------------------------------------------
A site that silently adds analytics, or that traps keyboard users, is a product
defect — not polish to be deferred. For a project whose public claim is a privacy
boundary, an analytics beacon on the front page would contradict the product in
the one place every visitor sees.

So this runs in `make check`, and it fails the build.

What it checks
--------------
1. **No unapproved external resource.** Every `src`, `href` and `srcset` must be
   same-origin, or on the allowlist below. Scripts are refused outright — the
   site ships none, and the cheapest way to keep it that way is to make adding
   one fail.
2. **No tracking signatures**, even inline: analytics snippets, beacons, pixels.
3. **Keyboard and structure**: a `lang` attribute, a skip link or a `<main>`
   landmark, and an accessible name on every link and image.
4. **`prefers-reduced-motion`** is honoured wherever animation is declared.
5. **No hover-only navigation** — a `:hover` rule that reveals a menu with no
   `:focus`, `:focus-visible` or `:focus-within` counterpart.

What it does not check
----------------------
Rendered contrast ratios and real keyboard traversal need a browser, which this
gate deliberately does not require: it must run on a clean checkout in CI with
nothing installed. Those remain a manual step in the release checklist, and this
file says so rather than implying full WCAG coverage.

Every result is reported with a denominator.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

#: External origins the site may reference. Deliberately tiny. GitHub is the
#: project's own home and the links are navigational, not resource loads.
ALLOWED_ORIGINS = (
    "https://github.com/malekokour/",
    "https://malekokour.github.io/",
)

#: Substrings that indicate a tracker, however it is delivered. Matched against
#: the whole document so an inline snippet is caught as readily as a script tag.
TRACKER_SIGNATURES = (
    "google-analytics", "googletagmanager", "gtag(", "ga(", "_gaq",
    "plausible.io", "fathom", "matomo", "piwik", "segment.com", "analytics.js",
    "hotjar", "clarity.ms", "mixpanel", "amplitude.com", "facebook.net",
    "fbq(", "doubleclick", "adsbygoogle", "beacon.js", "sentry.io",
)

RESOURCE_ATTR = re.compile(r"""\b(?:src|href|srcset|action)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
SCRIPT_TAG = re.compile(r"<script\b", re.IGNORECASE)
IFRAME_TAG = re.compile(r"<iframe\b", re.IGNORECASE)
LINK_TAG = re.compile(r"<a\b[^>]*>(.*?)</a>", re.IGNORECASE | re.DOTALL)
IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ALT_ATTR = re.compile(r"\balt\s*=\s*[\"'][^\"']*[\"']", re.IGNORECASE)
ARIA_LABEL = re.compile(r"\baria-label\s*=\s*[\"'][^\"']+[\"']", re.IGNORECASE)


def is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "//"))


def main() -> int:
    if not SITE.is_dir():
        print("PASS: no site/ directory — nothing to gate")
        return 0

    html_files = sorted(SITE.rglob("*.html"))
    css_files = sorted(SITE.rglob("*.css"))
    if not html_files:
        print("FAILED: site/ exists but contains no HTML")
        return 1

    problems: list[str] = []
    resources = links = images = 0

    for path in html_files:
        name = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()

        # 1 — scripts and frames
        if SCRIPT_TAG.search(text):
            problems.append(f"{name}: contains a <script> tag; the site ships no JavaScript")
        if IFRAME_TAG.search(text):
            problems.append(f"{name}: contains an <iframe>; third-party frames are not allowed")

        # 2 — trackers, however delivered
        for signature in TRACKER_SIGNATURES:
            if signature in lowered:
                problems.append(f"{name}: tracking signature present: {signature!r}")

        # 3 — external resources
        for url in RESOURCE_ATTR.findall(text):
            resources += 1
            if is_external(url) and not url.startswith(ALLOWED_ORIGINS):
                problems.append(f"{name}: external resource outside the allowlist: {url}")

        # 4 — structure and accessible names
        if not re.search(r"<html\b[^>]*\blang\s*=", text, re.IGNORECASE):
            problems.append(f"{name}: <html> has no lang attribute")
        if "<main" not in lowered and "skip to" not in lowered:
            problems.append(f"{name}: no <main> landmark and no skip link")

        for inner in LINK_TAG.findall(text):
            links += 1
            if not re.sub(r"<[^>]+>", "", inner).strip():
                problems.append(f"{name}: a link has no accessible text")

        for tag in IMG_TAG.findall(text):
            images += 1
            if not ALT_ATTR.search(tag) and not ARIA_LABEL.search(tag):
                problems.append(f"{name}: an <img> has no alt or aria-label: {tag[:60]}")

    # 5 — motion and hover-only navigation
    animated = reduced_motion = False
    for path in css_files:
        text = path.read_text(encoding="utf-8")
        name = path.relative_to(ROOT)
        if re.search(r"\b(animation|transition)\s*:", text, re.IGNORECASE):
            animated = True
        if "prefers-reduced-motion" in text:
            reduced_motion = True
        hover_rules = len(re.findall(r":hover\b", text, re.IGNORECASE))
        focus_rules = len(re.findall(r":focus(?:-visible|-within)?\b", text, re.IGNORECASE))
        if hover_rules and not focus_rules:
            problems.append(
                f"{name}: {hover_rules} :hover rule(s) and no :focus counterpart — "
                "keyboard users cannot reach what hover reveals"
            )

    if animated and not reduced_motion:
        problems.append(
            "site CSS declares animation or transition but never honours "
            "prefers-reduced-motion"
        )

    print(
        f"\nSite gates: {len(html_files)} HTML file(s), {len(css_files)} stylesheet(s), "
        f"{resources} resource reference(s), {links} link(s), {images} image(s) checked; "
        f"{len(TRACKER_SIGNATURES)} tracker signature(s) searched"
    )
    print(
        "  not covered here (needs a browser): rendered contrast ratios and real "
        "keyboard traversal — manual step in the release checklist"
    )

    if problems:
        print(f"\nFAILED: {len(problems)} site gate problem(s)")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("PASS: no trackers, no unapproved external resources, structure checks clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
