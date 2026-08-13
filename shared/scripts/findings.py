"""The finding and report contract shared by every deterministic checker.

Two invariants hold across all tools in this repository, and both are enforced
here rather than left to each script:

1. Every finding is **mechanical**. A tool reports that two documents disagree,
   that a required item is absent, or that an arithmetic relation does not hold.
   It never decides which value is correct, whether a difference matters
   clinically, or what dose to give.

2. Every summary states its **denominator**. "3 findings" is not interpretable;
   "3 findings across 47 statements checked" is. A report that cannot say what
   it examined cannot distinguish a clean document from an unread one.

Author: Malek Okour
Dependencies: Python standard library only — tools must run from a package ZIP
with nothing installed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

SEVERITIES = ("Critical", "Major", "Minor")


@dataclass
class Finding:
    """A mechanical finding. Never a scientific conclusion."""

    rule: str
    severity: str
    item: str
    observed: str
    expected: str
    locator: str
    detail: str
    kind: str = "mechanical"

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"severity must be one of {SEVERITIES}, got {self.severity!r}")

    def as_dict(self) -> dict[str, str]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "item": self.item,
            "observed": self.observed,
            "expected": self.expected,
            "locator": self.locator,
            "detail": self.detail,
            "kind": self.kind,
        }


@dataclass
class Report:
    """Findings plus the denominators that make a count interpretable."""

    tool: str
    findings: list[Finding] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)
    unassessable: list[dict[str, str]] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    def cannot_assess(self, item: str, why: str, resolved_by: str) -> None:
        """Record what could not be checked, and what would make it checkable.

        Silence about an unexamined item is indistinguishable from a pass, which
        is the failure this whole repository is built to avoid.
        """
        self.unassessable.append({"item": item, "why": why, "resolved_by": resolved_by})

    def count(self, name: str, value: int) -> None:
        self.counts[name] = value

    def tally(self) -> dict[str, int]:
        out = {s: 0 for s in SEVERITIES}
        for f in self.findings:
            out[f.severity] += 1
        return out

    def summary(self) -> str:
        if not self.counts:
            raise ValueError(
                f"{self.tool}: refusing to summarise without a denominator. "
                "Call count() with what was actually examined."
            )
        denom = " · ".join(f"{k} {v}" for k, v in sorted(self.counts.items()))
        t = self.tally()
        return (
            f"{self.tool}: {len(self.findings)} finding(s) "
            f"[Critical {t['Critical']} · Major {t['Major']} · Minor {t['Minor']}] "
            f"across {denom}; {len(self.unassessable)} not assessable"
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "tool": self.tool,
            "counts": self.counts,
            "tally": self.tally(),
            "findings": [f.as_dict() for f in self.findings],
            "unassessable": self.unassessable,
            "boundary": (
                "Mechanical findings only. This tool does not decide which value "
                "is correct, whether a difference is clinically meaningful, or "
                "what dose to give."
            ),
        }

    def render(self, as_json: bool = False) -> str:
        if as_json:
            return json.dumps(self.as_dict(), indent=2)
        lines = [self.summary()]
        for f in self.findings:
            lines.append(f"  [{f.severity}] {f.rule}")
            lines.append(f"    item     : {f.item}")
            lines.append(f"    as written: {f.observed}  @ {f.locator}")
            if f.expected:
                lines.append(f"    expected : {f.expected}")
            if f.detail:
                lines.append(f"    detail   : {f.detail}")
        for u in self.unassessable:
            lines.append(f"  [CANNOT_ASSESS] {u['item']} — {u['why']}")
            lines.append(f"    would resolve: {u['resolved_by']}")
        return "\n".join(lines)
