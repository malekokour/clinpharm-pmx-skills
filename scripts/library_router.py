"""Advisory library router — deterministic selection helper (PS-D027).

Reads catalog/nav_registry.json and optional settings. Never bypasses safety
refuses. Does not invoke LLMs. Returns a selection record for the host/agent.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SETTINGS = {
    "selection_mode": "ask",
    "ambiguity_policy": "ask_user",
    "allow_agent_auto_select": False,
    "eligible_statuses": ["released"],
    "force_skill": None,
    "force_skill_scope": "per_invocation",
    "disabled_skills": [],
    "risk_ceiling": "MEDIUM",
    "show_selection_reasons": True,
}

KNOWN_KEYS = frozenset(DEFAULT_SETTINGS) | {"schema_version", "notes"}

#: Both separation thresholds are **ratios of the leader's score**, not absolute
#: point gaps. They were absolute until 2026-08-11, which was safe only while
#: every token weighed exactly 1.0; under the rarity weighting in
#: `token_weights` an absolute gap means different things for a request built
#: from rare terms than for one built from common ones. Ratios are scale-free.
#:
#: A runner-up at or above this fraction of the leader is too close to call, and
#: the router asks rather than choosing a reading.
#:
#: Calibrated against the measured separation on this registry under rarity
#: weighting: an unambiguous single-package request scores its runner-up at
#: ~0.13 of the leader, a request naming two packages at ~0.57, and a genuinely
#: vague one at 0.81-1.00. The two bands are the other way round from the naive
#: reading, and deliberately so — *very* close means "cannot tell which one",
#: while *moderately* close means "two distinct peaks, so probably both".
AMBIGUITY_RATIO = 0.75

#: Below the ambiguity ratio but at or above this one, with clear separation from
#: third place, the runner-up is a genuine second peak — the signature of a
#: request naming two packages rather than one. Screening threshold, not a
#: correctness boundary; exercised in both directions by
#: evals/library-router/selection-cases.json.
SECOND_PEAK_RATIO = 0.50

HUMAN_ONLY = re.compile(
    r"\b(sign[- ]?off|approve submission|select(?:ing)? (?:a )?dose|"
    r"prescribe|autonomous (?:dose|decision))\b",
    re.IGNORECASE,
)
OOS = re.compile(
    r"\b(wet[- ]?lab|cmc|medical affairs|patient[- ]facing|"
    r"diagnos(?:e|is|tic treatment))\b",
    re.IGNORECASE,
)
#: Joins a request that names two things. Required by the two-strong-candidates
#: guard **in addition to** the score signature.
#:
#: The score signature alone is not specific enough. At n=50 the FIX-11 fixtures
#: showed `review the bioanalytical validation report` putting the right package
#: first at ratio 1.00 with a distractor at 0.54 — a second peak by the numbers,
#: but the request names one thing, and asking about it would be a false alarm on
#: a request the router had answered correctly. A request that genuinely names
#: two packages joins them with a word: "the CSR **and** the protocol".
#:
#: The trade is deliberate and asymmetric. A two-target request written without a
#: conjunction falls through to top-1 — a plausible answer to half the request,
#: not a wrong answer to all of it.
CONJUNCTION = re.compile(
    r"\b(and|plus|both|together|as well as|along with|then)\b", re.IGNORECASE
)

MULTI = re.compile(
    r"\b(full (?:poppk|pop[- ]?pk|submission|programme|program)|"
    r"entire (?:nDA|bla|submission)|end[- ]to[- ]end (?:pmx|poppk))\b",
    re.IGNORECASE,
)

#: Meta-routing asks name no clinical object. Without this guard they score
#: against every package that mentions "skill" or "library" in its description
#: and silently resolve — the opposite of asking the user which skill to use.
META_ASK = re.compile(
    r"\bwhich (?:library )?skill\b|\bwhat skill (?:should|do) i (?:use|run|pick)\b|"
    r"\bhelp me (?:choose|pick|select) (?:a |the )?skill\b",
    re.IGNORECASE,
)


def load_settings(path: Path | None = None) -> dict[str, Any]:
    settings = dict(DEFAULT_SETTINGS)
    candidate = path or (ROOT / "scripts" / "settings.example.json")
    if candidate.is_file():
        raw = json.loads(candidate.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("settings must be a JSON object")
        unknown = set(raw) - KNOWN_KEYS
        if unknown:
            raise ValueError(f"unknown settings keys: {sorted(unknown)}")
        for key, value in raw.items():
            if key in {"schema_version", "notes"}:
                continue
            if key not in DEFAULT_SETTINGS:
                continue
            expected = type(DEFAULT_SETTINGS[key])
            if DEFAULT_SETTINGS[key] is None:
                if value is not None and not isinstance(value, str):
                    raise ValueError(f"{key} must be string or null")
            elif not isinstance(value, expected):
                raise ValueError(f"{key} must be {expected.__name__}")
            settings[key] = value
    return settings


def load_registry(path: Path | None = None) -> list[dict[str, Any]]:
    registry_path = path or (ROOT / "catalog" / "nav_registry.json")
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        raise ValueError("nav_registry.skills must be a non-empty list")
    return skills


def load_statuses(root: Path | None = None) -> dict[str, str]:
    base = root or ROOT
    found: dict[str, str] = {}
    for path in sorted((base / "collections").glob("*/collection.json")):
        catalog = json.loads(path.read_text(encoding="utf-8"))
        for entry in catalog.get("skills", []):
            skill_id = entry.get("id")
            if isinstance(skill_id, str) and skill_id:
                found[skill_id] = str(entry.get("status") or "built")
    return found


def classify(utterance: str) -> str:
    text = utterance.strip()
    if not text:
        return "AMBIGUOUS"
    if HUMAN_ONLY.search(text):
        return "HUMAN_ONLY"
    if OOS.search(text):
        return "OOS"
    if MULTI.search(text):
        return "MULTI"
    if META_ASK.search(text):
        return "AMBIGUOUS"
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    if len(tokens) <= 4 and not any(
        t in tokens for t in ("review", "reconcile", "verify", "prepare", "map")
    ):
        return "SIMPLE"
    return "SINGLE"


#: Punctuation *between digits* only. Regulatory section numbers are written
#: "2.7.2" in prose and "272" in identifiers, and the tokenizer below drops
#: anything under three characters — so "review ctd 2.7.2 content" lost its one
#: discriminating term entirely and scored no better on `review-ctd-272-content`
#: than on three sibling packages whose ids also end in "content". Joining the
#: digit run restores it. Deliberately narrow: it must not join "section 12" to
#: a following number, so the lookarounds require digits on both sides.
DIGIT_RUN_SEPARATOR = re.compile(r"(?<=\d)[.\-– ](?=\d)")


def normalise(utterance: str) -> str:
    """Lowercase and join digit runs so section numbers survive tokenizing."""
    return DIGIT_RUN_SEPARATOR.sub("", utterance.lower())


def _haystack(skill: dict[str, Any]) -> str:
    skill_id = str(skill.get("id") or "")
    nav = str(skill.get("nav_path") or "").replace("/", " ")
    return f"{skill_id} {nav}".lower()


def token_weights(skills: list[dict[str, Any]]) -> dict[str, float]:
    """Weight each registry token by how rare it is across the registry.

    Flat token weights were the scoring model until 2026-08-11, and they do not
    survive scale. In this library ``review``, ``report`` and ``table`` appear in
    a large fraction of package names, so they carry the same weight as
    ``bioanalytical`` or ``dsur`` — which carry all of the actual signal.

    At n=22 the right package still won, because no sibling matched *both*
    common tokens. The FIX-11 fixtures showed what happens when it does: at
    n=50, ``review the bioanalytical validation report`` tied 4.50–4.50 against a
    distractor named ``…-review-covariate-report-…``, purely on ``review`` +
    ``report``. Top-1 fell from 21/21 to 18/21.

    The weight is ``log(N / df)``, the standard inverse-document-frequency form:
    a token in every package contributes ~0, a token in one package contributes
    ``log(N)``. This is scale-free, needs no tuning per registry size, and is
    computed from the registry itself rather than from a hand-kept stopword list
    that would go stale the first time a package was renamed.
    """
    total = len(skills)
    document_frequency: dict[str, int] = {}
    for skill in skills:
        for token in set(re.findall(r"[a-z0-9]+", _haystack(skill))):
            if len(token) >= 3:
                document_frequency[token] = document_frequency.get(token, 0) + 1
    # +1 inside the log keeps a token present in every package at a small
    # positive weight rather than exactly zero: it is weak evidence, not none.
    return {
        token: math.log((total + 1) / count)
        for token, count in document_frequency.items()
    }


def _score(
    utterance: str,
    skill: dict[str, Any],
    weights: dict[str, float] | None = None,
) -> float:
    text = normalise(utterance)
    skill_id = str(skill.get("id") or "")
    hay = _haystack(skill)
    score = 0.0
    for token in re.findall(r"[a-z0-9]+", text):
        # Short tokens are dropped as noise — "of", "an", "in" carry nothing. Numbers
        # are the exception, and in this library they are the opposite of noise: the
        # entire distinction between USPI Section 7 and Section 12, or between CTD
        # 2.5, 2.7.1 and 2.7.2, is a one- or two-character numeral.
        #
        # Found 2026-08-11: "review the uspi section 12 labelling content" ranked
        # Section 12 first but at only a 0.78 margin over Section 7, because "12"
        # was discarded and every remaining token matched both. The router asked
        # instead of answering. Dropping the digit dropped the answer.
        if len(token) < 3 and not token.isdigit():
            continue
        # An unweighted call (no registry in hand) falls back to the flat model,
        # which keeps `_score` usable on a single skill in isolation.
        weight = 1.0 if weights is None else weights.get(token, math.log(2.0))
        if token in hay:
            score += weight
        if token in skill_id:
            score += 0.5 * weight
    for alias in skill.get("aliases") or []:
        if str(alias).lower() in text:
            score += 3.0
    return score


#: The router skill is part of the library for humans to invoke, but it must never
#: be a *selection result*. Otherwise "which skill should I use?" resolves to
#: library-router itself once its description shares vocabulary with the ask —
#: a meta loop, not a routing answer.
NON_SELECTABLE = frozenset({"library-router"})


def select(
    utterance: str,
    *,
    settings: dict[str, Any] | None = None,
    skills: list[dict[str, Any]] | None = None,
    statuses: dict[str, str] | None = None,
) -> dict[str, Any]:
    cfg = settings or load_settings()
    registry = skills or load_registry()
    status_map = statuses or load_statuses()
    disabled = set(cfg.get("disabled_skills") or [])
    eligible = set(cfg.get("eligible_statuses") or ["released"])

    # Classification runs BEFORE any operator preference is applied.
    #
    # It did not until 2026-08-11, and the ordering was a safety defect rather
    # than a style question: skills/library-router/SKILL.md states that
    # "preferences cannot bypass refuse paths for human-only, OOS, or safety
    # cases", but `force_skill` was read first, so an operator who had pinned a
    # skill turned "select a dose for this cohort" into a routed request. The
    # selection suite case SEL-REFUSE-06 exists to hold this ordering: it was
    # written against the old behaviour, went red on this change, and its
    # expectation was corrected to the refusal the contract always promised.
    complexity = classify(utterance)
    if complexity in {"HUMAN_ONLY", "OOS"}:
        return {
            "complexity": complexity,
            "decision": "refuse",
            "chosen": None,
            "candidates": [],
            "reasons": [complexity.lower(), "preference_cannot_bypass_refuse"]
            if cfg.get("force_skill")
            else [complexity.lower()],
        }

    force = cfg.get("force_skill")
    if force:
        if force in disabled:
            return {
                "complexity": "REFUSE",
                "decision": "refuse",
                "chosen": None,
                "candidates": [],
                "reasons": ["force_skill_disabled"],
            }
        return {
            "complexity": "SINGLE",
            "decision": "force",
            "chosen": force,
            "candidates": [force],
            "reasons": ["force_skill_per_invocation"],
        }

    if complexity == "MULTI":
        return {
            "complexity": complexity,
            "decision": "ask",
            "chosen": None,
            "candidates": [],
            "reasons": ["multi_no_silent_swarm", "offer_skill_sequence"],
        }

    if complexity == "AMBIGUOUS" and META_ASK.search(utterance):
        return {
            "complexity": "AMBIGUOUS",
            "decision": "ask",
            "chosen": None,
            "candidates": [],
            "reasons": ["meta_skill_ask", "need_task_object"],
        }

    # Weights come from the registry actually in play, so a caller passing a
    # 100-entry fixture gets weights computed over those 100 rather than over
    # the shipped 22.
    weights = token_weights(registry)

    scored: list[tuple[float, str, str]] = []
    for skill in registry:
        skill_id = str(skill.get("id") or "")
        if not skill_id or skill_id in disabled or skill_id in NON_SELECTABLE:
            continue
        status = status_map.get(skill_id, "built")
        score = _score(utterance, skill, weights)
        if score > 0:
            scored.append((score, skill_id, status))
    scored.sort(key=lambda row: (-row[0], row[1]))

    if not scored:
        return {
            "complexity": complexity,
            "decision": "ask",
            "chosen": None,
            "candidates": [],
            "reasons": ["no_candidates"],
        }

    top_score, top_id, top_status = scored[0]
    candidates = [sid for _, sid, _ in scored[:5]]
    second_ratio = scored[1][0] / top_score if len(scored) > 1 and top_score else 0.0
    if second_ratio >= AMBIGUITY_RATIO:
        return {
            "complexity": "AMBIGUOUS",
            "decision": "ask",
            "chosen": None,
            "candidates": candidates,
            "reasons": ["close_top2", f"second_ratio={second_ratio:.2f}"],
        }

    # Two named targets, not one ambiguous one. The margin test above catches a
    # tie; it does not catch "review the CSR *and* the protocol PK sections",
    # where the top two are 4.50 / 3.00 and the third is 1.50. That is not a
    # close call between two readings of one request — it is one request naming
    # two skills, and answering it with a silent top-1 drops half of what was
    # asked for. The signature is a genuine second peak: the runner-up is a
    # large fraction of the leader AND is itself clearly clear of the field.
    #
    # Measured on this registry (2026-08-11): single-skill utterances score
    # second place at the 1.50 noise floor against a 4.50-9.00 leader, so the
    # ratio test does not fire on them. The suite in evals/library-router/
    # holds both directions so a future scoring change cannot quietly erase
    # either one.
    # Two conditions, and both are necessary. A separation test alone fires on
    # single-target requests that merely have a plausible runner-up; a
    # conjunction alone fires on any sentence containing "and".
    #
    # A third condition — "the runner-up must also be clear of third place" —
    # was here until 2026-08-11 and has been removed. It was standing in for the
    # conjunction test before that existed, and once both were required it
    # produced a false negative the moment a 23rd package was added: the new
    # package scored 0.83 of the runner-up on a shared token, the "clear of
    # third" test failed, and a request naming two packages went back to
    # silently answering half of it. Two conditions that each carry the same
    # signal is one condition too many.
    if second_ratio >= SECOND_PEAK_RATIO and CONJUNCTION.search(utterance):
        return {
            "complexity": "MULTI",
            "decision": "ask",
            "chosen": None,
            "candidates": candidates,
            "reasons": [
                "two_strong_candidates",
                "offer_skill_sequence",
                f"second_ratio={second_ratio:.2f}",
            ],
        }

    reasons = [f"score={top_score:.2f}", f"status={top_status}"]
    if top_status not in eligible:
        reasons.append("not_in_eligible_statuses")

    # Default product posture: recommend + ask unless auto-select enabled
    if cfg.get("selection_mode") == "ask" and not cfg.get("allow_agent_auto_select"):
        return {
            "complexity": complexity,
            "decision": "ask",
            "chosen": top_id,
            "candidates": candidates,
            "reasons": ["recommend_ask_confirm", *reasons],
        }

    if cfg.get("selection_mode") == "manual_only":
        return {
            "complexity": complexity,
            "decision": "ask",
            "chosen": top_id,
            "candidates": candidates,
            "reasons": ["manual_only", *reasons],
        }

    if top_status not in eligible:
        return {
            "complexity": complexity,
            "decision": "ask",
            "chosen": top_id,
            "candidates": candidates,
            "reasons": ["auto_blocked_ineligible_status", *reasons],
        }

    return {
        "complexity": complexity,
        "decision": "top1",
        "chosen": top_id,
        "candidates": candidates,
        "reasons": reasons,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="ClinPharm PMx Skills advisory library router")
    parser.add_argument("utterance", nargs="+", help="User/agent request text")
    parser.add_argument("--settings", type=Path, default=None)
    args = parser.parse_args()
    result = select(" ".join(args.utterance), settings=load_settings(args.settings))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
