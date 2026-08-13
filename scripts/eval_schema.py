"""Executable schemas for the PS-D028 evaluation suite layout.

Author: ClinPharm PMx Skills contributors
Date: 2026-08-06
Dependencies: strictyaml (pinned in requirements.lock); Python standard library

Why these are schemas and not documentation
-------------------------------------------
PS-D028 chose YAML with a ``mechanical`` / ``judged`` split so that machine
checkable assertions can fail a build while judged ones are scored openly
against a rubric. A written layout cannot enforce that split — the previous
grader accepted any shape at all, because it never read the suite.

These validators reject a malformed case at load time. ``strictyaml`` is used
rather than PyYAML because it refuses implicit typing: ``severity: Critical``
stays a string, ``locator_required: true`` must be an explicit boolean, and an
unlisted key is an error rather than a silently ignored field. A schema that
quietly accepts a typo'd key is the same class of defect as a check that scans
zero files.

The record schemas (grading, timing, metrics, benchmark) deliberately match
skill-creator's published shapes in ``references/schemas.md`` verbatim. The
review viewer reads those field names exactly, and inventing a parallel shape
would mean the artifacts could not be opened by the official tooling.
"""

from __future__ import annotations

from typing import Any

from strictyaml import (
    Any as AnyYAML,  # aliased: `typing.Any` is used in the signatures below
)
from strictyaml import (
    Bool,
    Enum,
    Int,
    Map,
    Optional,
    Seq,
    Str,
    load,
)
from strictyaml.exceptions import StrictYAMLError

# --- vocabulary ---------------------------------------------------------------

#: The four promotion-gate layers. A case declares which one it exercises so a
#: dossier can state coverage per layer instead of one undifferentiated total.
LAYERS = ["activation", "execution", "safety", "portability"]

#: Defect severities. `Critical` carries a hard rule at the promotion gate:
#: one missed Critical fails outright, so it may not be spelled loosely.
SEVERITIES = ["Critical", "Major", "Minor"]

#: PS-D024 qualification vocabulary. A diagnostic suite may describe evidence
#: still to be collected; a qualifying suite must carry numeric, executable
#: thresholds rather than prose placeholders.
QUALIFICATION_PROFILES = ["LOW", "MEDIUM", "HIGH"]
THRESHOLD_STATES = ["diagnostic", "qualifying"]
QUALIFICATION_POLICY = "PS-D024-v1"
PROFILE_CORE_RUNS = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

#: How a defect is expected to be caught. `script` misses are script bugs and
#: must be fixed in the script rather than excused as model variance.
DETECTORS = ["script", "model", "either"]

# --- mechanical assertion shapes ----------------------------------------------
#
# Each shape answers one question about the response text, and each is
# evaluated by reading `outputs/response.md`. There is no shape that can pass
# without the response containing something.

#: The response must report a specific planted defect from the expert key.
#:
#: **A defect is a value pair, not a token.** Every planted defect in this
#: repository's fixtures is "the document says X where the source says Y", so an
#: assertion binds both sides: ``observed`` (the wrong value as written) and
#: ``expected`` (what the source says). Both must appear in the *same* finding,
#: together with a locator, and — where asserted — the right severity.
#:
#: This replaces a single ``match`` token, which bound nothing. On 2026-08-06 a
#: D4 assertion matching ``mL/h`` passed a response reading *"the CLI reported
#: **no finding**, because `mL/h` is a valid clearance unit"* — the exact
#: opposite of detection — and separately passed a line grading that Critical
#: defect as Major. A number appearing anywhere, including inside a
#: reconciliation table the model was merely transcribing, is not detection.
DEFECT_ASSERTION = Map(
    {
        "defect": Str(),
        "severity": Enum(SEVERITIES),
        "detected_by": Enum(DETECTORS),
        "observed": Str(),
        "expected": Str(),
        Optional("locator_required", default=True): Bool(),
        Optional("severity_required", default=True): Bool(),
    }
)

#: The response must state a denominator — "checked N", "6/6", "N of M".
#: The product's central claim is that every finding states its denominator, so
#: this is checkable rather than judged.
DENOMINATOR_ASSERTION = Map({"denominator_stated": Bool()})

#: The response must contain a literal string.
CONTAINS_ASSERTION = Map({"must_contain": Str(), Optional("label"): Str()})

#: The response must NOT contain a literal string. This is how false-positive
#: traps and the "never recommends a dose" boundary are checked.
ABSENT_ASSERTION = Map({"must_not_contain": Str(), Optional("label"): Str()})

#: The response must emit an exact classification token, e.g.
#: RESTRICTED_DO_NOT_PROCESS. Distinct from must_contain so that a safety
#: refusal reads as a refusal in the dossier rather than as a string match.
CLASSIFICATION_ASSERTION = Map({"classification": Str()})

#: Discriminating key -> the shape that key implies.
#:
#: strictyaml refuses to ``|`` two Map validators together and directs callers
#: to revalidation instead, so the assertion list is parsed as ``Any()`` and
#: each item is then revalidated against exactly one of these. The upside over
#: a union is the error message: a malformed defect assertion is reported
#: against the defect shape rather than as "matched none of five alternatives".
MECHANICAL_SHAPES = {
    "defect": DEFECT_ASSERTION,
    "denominator_stated": DENOMINATOR_ASSERTION,
    "must_contain": CONTAINS_ASSERTION,
    "must_not_contain": ABSENT_ASSERTION,
    "classification": CLASSIFICATION_ASSERTION,
}

# --- case and suite -----------------------------------------------------------

CASE_SCHEMA = Map(
    {
        "id": Str(),
        "layer": Enum(LAYERS),
        Optional("mode"): Str(),
        # Provenance for a case whose prompt was derived from the skill's own
        # text rather than authored freely — it carries the source sentence
        # verbatim so a reviewer can check the derivation instead of trusting
        # it. Used by the negative activation cases, where the prompt must
        # fall inside the skill's declared exclusion and nothing else.
        Optional("source_clause"): Str(),
        "prompt": Str(),
        Optional("inputs"): Seq(Str()),
        "assertions": Map(
            {
                Optional("mechanical"): Seq(AnyYAML()),
                Optional("judged"): Seq(Str()),
            }
        ),
    }
)

SUITE_SCHEMA = Map(
    {
        "skill": Str(),
        "version": Str(),
        "qualification_profile": Enum(QUALIFICATION_PROFILES),
        "qualification_policy": Str(),
        Optional("fixture_key"): Str(),
        Optional("note"): Str(),
        "thresholds": Map(
            {
                Optional("state", default="diagnostic"): Enum(THRESHOLD_STATES),
                "recall": Str(),
                "precision": Str(),
                Optional("pass_rate"): Str(),
                Optional("activation_accuracy"): Str(),
                Optional("baseline_delta"): Str(),
                Optional("missed_critical_allowed"): Int(),
                Optional("diagnostic_reason"): Str(),
            }
        ),
    }
)


class SchemaError(ValueError):
    """A suite or case file did not satisfy its schema."""


def load_case(text: str, label: str) -> dict[str, Any]:
    """Parse and validate one case file. Raises SchemaError on any violation.

    Two passes: the case shape, then each mechanical assertion against the one
    shape its discriminating key implies. An assertion carrying no recognised
    key is an error rather than an ignored entry — silently skipping it would
    let a typo'd assertion vanish from the denominator.
    """
    try:
        document = load(text, CASE_SCHEMA)
    except StrictYAMLError as exc:
        raise SchemaError(f"{label}: {exc}") from exc

    assertions = document["assertions"]
    if "mechanical" in assertions:
        for index, item in enumerate(assertions["mechanical"]):
            keys = set(item.data) if isinstance(item.data, dict) else set()
            discriminators = keys & set(MECHANICAL_SHAPES)
            if len(discriminators) != 1:
                raise SchemaError(
                    f"{label}: assertions.mechanical[{index}] must carry exactly one "
                    f"of {sorted(MECHANICAL_SHAPES)}; found {sorted(keys) or 'nothing'}"
                )
            try:
                item.revalidate(MECHANICAL_SHAPES[discriminators.pop()])
            except StrictYAMLError as exc:
                raise SchemaError(
                    f"{label}: assertions.mechanical[{index}]: {exc}"
                ) from exc

    data = document.data
    mechanical = data.get("assertions", {}).get("mechanical", [])
    judged = data.get("assertions", {}).get("judged", [])
    if not mechanical and not judged:
        raise SchemaError(f"{label}: case declares no assertions at all")
    return data


def load_suite(text: str, label: str) -> dict[str, Any]:
    """Parse and validate a suite.yaml. Raises SchemaError on any violation.

    Diagnostic suites may retain prose explaining why a metric is not yet
    claimable. Once ``thresholds.state`` becomes ``qualifying``, every metric
    required by the assigned profile must be a numeric fraction. This keeps a
    planning sentence from masquerading as a machine-enforceable gate.
    """
    try:
        data = load(text, SUITE_SCHEMA).data
    except StrictYAMLError as exc:
        raise SchemaError(f"{label}: {exc}") from exc

    if data["qualification_policy"] != QUALIFICATION_POLICY:
        raise SchemaError(
            f"{label}: qualification_policy must be {QUALIFICATION_POLICY!r}"
        )

    thresholds = data["thresholds"]
    if thresholds["state"] != "qualifying":
        return data

    profile = data["qualification_profile"]
    required = ["pass_rate", "activation_accuracy"]
    if profile in {"MEDIUM", "HIGH"}:
        required += ["recall", "precision"]

    for field in required:
        raw = thresholds.get(field)
        try:
            value = float(raw)
        except (TypeError, ValueError) as exc:
            raise SchemaError(
                f"{label}: qualifying {profile} threshold {field!r} must be a "
                f"numeric fraction; found {raw!r}"
            ) from exc
        if not 0.0 <= value <= 1.0:
            raise SchemaError(
                f"{label}: qualifying threshold {field!r}={value} is outside 0..1"
            )

    if "baseline_delta" in thresholds:
        try:
            delta = float(thresholds["baseline_delta"])
        except (TypeError, ValueError) as exc:
            raise SchemaError(
                f"{label}: baseline_delta must be numeric; found "
                f"{thresholds['baseline_delta']!r}"
            ) from exc
        if not -1.0 <= delta <= 1.0:
            raise SchemaError(
                f"{label}: baseline_delta={delta} is outside -1..1"
            )

    if thresholds.get("missed_critical_allowed", 0) != 0:
        raise SchemaError(
            f"{label}: qualifying suites must set missed_critical_allowed to 0"
        )
    return data


# --- record shapes ------------------------------------------------------------
#
# Validated structurally rather than by a JSON-Schema dependency, because these
# gates must run from a clean checkout. Each function returns a list of problems
# and never raises, so a caller can report every fault at once instead of the
# first.


def check_grading(record: dict[str, Any]) -> list[str]:
    """Validate a grading.json against skill-creator's published shape."""
    problems: list[str] = []
    expectations = record.get("expectations")
    if not isinstance(expectations, list) or not expectations:
        problems.append("grading.expectations must be a non-empty list")
        expectations = []
    for index, item in enumerate(expectations):
        if not isinstance(item, dict):
            problems.append(f"grading.expectations[{index}] is not an object")
            continue
        for field in ("text", "passed", "evidence"):
            if field not in item:
                problems.append(f"grading.expectations[{index}] missing '{field}'")
        # An empty evidence string is the vacuity this schema exists to stop:
        # a graded assertion whose justification is blank asserts nothing.
        if not str(item.get("evidence", "")).strip():
            problems.append(
                f"grading.expectations[{index}] has empty evidence; a graded "
                "assertion must say what in the output justified the verdict"
            )
    summary = record.get("summary")
    if not isinstance(summary, dict):
        problems.append("grading.summary missing")
        return problems
    for field in ("passed", "failed", "total", "pass_rate"):
        if field not in summary:
            problems.append(f"grading.summary missing '{field}'")
    if isinstance(summary.get("total"), int) and expectations:
        if summary["total"] != len(expectations):
            problems.append(
                f"grading.summary.total is {summary['total']} but there are "
                f"{len(expectations)} expectations"
            )
        counted = sum(1 for item in expectations if isinstance(item, dict) and item.get("passed"))
        if summary.get("passed") != counted:
            problems.append(
                f"grading.summary.passed is {summary.get('passed')} but "
                f"{counted} expectations are marked passed"
            )
    if summary.get("total") == 0:
        problems.append("grading.summary.total is 0 — a pass rate over no assertions")
    return problems


def check_timing(record: dict[str, Any]) -> list[str]:
    """Validate a timing.json.

    REQ-SC-004 requires tokens and duration captured immediately, because the
    task notification carrying them is not persisted anywhere else. A run whose
    timing is absent or null is recorded as incomplete rather than as zero.

    Batch execution
    ---------------
    When several runs are executed by one executor, the notification reports one
    token count and one duration for the whole batch. Per-run figures are not
    merely unrecorded — they are **unknowable**, and dividing the batch total by
    the run count would invent them.

    So a run may instead declare ``telemetry_granularity: "batch"`` and carry the
    batch figures with the count they cover. That is honest: it says what is
    known and refuses to imply what is not. ``total_tokens`` and ``duration_ms``
    must then be explicitly null, so no reader can mistake a batch figure for a
    per-run one, and no aggregation can sum them by accident.

    The default stays ``"run"``, and under it nulls remain a failure. This is a
    narrowing of the rule to what it can actually enforce, not a relaxation of
    it: a batch-executed run still cannot be graded without stating its batch
    telemetry and how many runs that telemetry covers.
    """
    problems: list[str] = []
    granularity = record.get("telemetry_granularity", "run")

    if granularity not in ("run", "batch"):
        problems.append(
            f"timing.telemetry_granularity is '{granularity}'; expected 'run' or 'batch'"
        )
        return problems

    if granularity == "batch":
        for field in ("batch_total_tokens", "batch_duration_ms", "batch_run_count"):
            if field not in record:
                problems.append(f"timing declares batch granularity but is missing '{field}'")
            elif not isinstance(record[field], (int, float)) or record[field] is None:
                problems.append(f"timing.{field} must be numeric under batch granularity")
        if record.get("batch_run_count") == 0:
            problems.append("timing.batch_run_count is 0 — telemetry over no runs")
        for field in ("total_tokens", "duration_ms"):
            if record.get(field) is not None:
                problems.append(
                    f"timing.{field} must be null under batch granularity — a per-run "
                    "figure derived from a batch total would be invented, not measured"
                )
        return problems

    for field in ("total_tokens", "duration_ms"):
        if field not in record:
            problems.append(f"timing missing '{field}'")
        elif record[field] is None:
            problems.append(
                f"timing.{field} is null — capture it when the run completes; "
                "it cannot be recovered afterwards"
            )
        elif not isinstance(record[field], (int, float)):
            problems.append(f"timing.{field} is not numeric")
    return problems


def check_metrics(record: dict[str, Any]) -> list[str]:
    """Validate an outputs/metrics.json."""
    problems: list[str] = []
    for field in ("total_tool_calls", "total_steps", "errors_encountered", "output_chars"):
        if field not in record:
            problems.append(f"metrics missing '{field}'")
    if record.get("output_chars") == 0:
        problems.append("metrics.output_chars is 0 — the run produced no output")
    return problems


#: What must exist before a run can be graded. `grading.json` is deliberately
#: absent: it is the grader's *output*, and requiring it as an input made
#: grading impossible until it had already happened.
REQUIRED_INPUT_FILES = ("timing.json", "outputs/response.md", "outputs/metrics.json")

#: What must exist for a run to count as complete — the inputs plus the grade.
#: Exposed so the workspace checker and the grader import one definition rather
#: than restating it, which is how the two drifted into disagreeing at all.
REQUIRED_RUN_FILES = (*REQUIRED_INPUT_FILES, "grading.json")

CONFIGURATIONS = ("with_skill", "without_skill")

__all__ = [
    "CASE_SCHEMA",
    "CONFIGURATIONS",
    "DETECTORS",
    "LAYERS",
    "PROFILE_CORE_RUNS",
    "QUALIFICATION_POLICY",
    "QUALIFICATION_PROFILES",
    "REQUIRED_INPUT_FILES",
    "REQUIRED_RUN_FILES",
    "SEVERITIES",
    "SUITE_SCHEMA",
    "THRESHOLD_STATES",
    "SchemaError",
    "check_grading",
    "check_metrics",
    "check_timing",
    "load_case",
    "load_suite",
]
