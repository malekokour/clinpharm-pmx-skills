# Prefer the project virtualenv when one exists, and fall back to `python3`
# otherwise. A bare `python3` default made `make evals` fail with
# ModuleNotFoundError: strictyaml on a machine that HAD a working .venv — the
# interpreter it picked simply was not the one the dependencies were installed
# into. CI creates no .venv and installs the lockfile into its own interpreter,
# so the fallback is the path CI takes. Override with `make PYTHON=... `.
PYTHON ?= $(shell test -x .venv/bin/python && echo .venv/bin/python || echo python3)
RUFF   ?= $(shell test -x .venv/bin/ruff && echo .venv/bin/ruff || echo ruff)

.PHONY: check lint validate gates registry evals defect-shape portability portable-frontmatter vendored routing router-selection nav-registry claim-ledger site-gates lifecycle grounding fixture-arithmetic docs-check parity benchmark-digests privacy-scan grade-evals test docs media release-check all

# `check` runs what CI runs. It previously ran only check_all.py while CI also
# ran ruff, so a green local gate said nothing about whether CI would pass —
# and the first push failed on three lint errors that had never been visible
# locally. If the two ever diverge again, that is the bug.
check: lint
	$(PYTHON) scripts/check_all.py

# A missing linter is a blocker, not a pass. Skipping it silently would restore
# exactly the gap this target exists to close, so it fails with instructions.
lint:
	@command -v $(RUFF) >/dev/null 2>&1 || { \
		echo "FAILED: ruff is not installed, so the lint gate cannot run."; \
		echo "  It is pinned in requirements.lock and CI runs it on every push."; \
		echo "  Install it:  $(PYTHON) -m pip install --requirement requirements.lock"; \
		exit 1; \
	}
	# `skills` is in this list because it was not, and 47 shipped scripts went
	# unlinted while the internal ones were checked on every push. The scripts a
	# user actually runs had the weaker guarantee — the same asymmetry that let
	# three of them report clean results over nothing.
	$(RUFF) check scripts tests skills

validate:
	$(PYTHON) scripts/validate_repo.py

# Vision v1.2 gates: tool budget, size budget, allowed-tools, registry schema,
# ledger coverage. Each proven able to go red before being wired in.
gates:
	$(PYTHON) scripts/check_v12_gates.py

registry:
	$(PYTHON) scripts/build_nav_registry.py

parity:
	$(PYTHON) scripts/check_docx_parity.py

benchmark-digests:
	$(PYTHON) scripts/verify_benchmark_digests.py

privacy-scan:
	$(PYTHON) scripts/privacy_scan.py

# `grade-evals` used to run scripts/grade_local_evals.py, which carried its
# results as a literal True/False table and read a _eval-workspace/ that has
# never existed in this tree — so it exited 2 while claiming to be a gate.
# Grading is now per-run and needs a workspace argument, so it is not a
# repository-wide target: there is nothing to grade until runs exist.
#
# `evals` validates the suites themselves, which IS repository-wide and is
# what `make check` should have been able to assert all along.
evals:
	$(PYTHON) scripts/eval_suite_check.py

# A defect assertion binds a value pair. This rejects sides that describe a
# value instead of being one (FIX-10 / phrase-brittle finding, remedy 3).
defect-shape:
	$(PYTHON) scripts/check_defect_assertion_shape.py

portability:
	$(PYTHON) scripts/check_portability.py

# The portability *claim*: six standard frontmatter keys, no host-only body
# syntax, reported with a denominator so it cannot pass over nothing.
portable-frontmatter:
	$(PYTHON) scripts/check_portable_frontmatter.py

vendored:
	$(PYTHON) scripts/check_vendored.py

routing:
	$(PYTHON) scripts/check_routing.py

# Distinct from `routing`, which screens whether the declared *scopes* partition.
# This one runs the router and checks which package it actually returns.
router-selection:
	$(PYTHON) scripts/check_router_selection.py --verbose

# Does every field the router design method asks for resolve, for every
# registered package? Reports where each one resolved from.
nav-registry:
	$(PYTHON) scripts/check_nav_registry.py

# Every public count re-derived from its source of record.
claim-ledger:
	$(PYTHON) scripts/check_claim_ledger.py --check

# No-tracking and accessibility are release gates, not polish (PS-D027 D-L13).
site-gates:
	$(PYTHON) scripts/check_site_gates.py

# The install/update/rollback/uninstall runbook must name things that exist.
lifecycle:
	$(PYTHON) scripts/check_lifecycle_docs.py

grounding:
	$(PYTHON) scripts/check_fixture_grounding.py

# Wired into `check` on 2026-08-06, when Table 14.2.1 was rebuilt and this went
# green. It was deliberately held out while it failed by design; the revisit
# trigger recorded there has now fired.
fixture-arithmetic:
	$(PYTHON) scripts/check_fixture_arithmetic.py

grade-evals:
	@echo "grade-evals is per-run, not repository-wide. Stage, execute, then grade:"
	@echo "  $(PYTHON) scripts/eval_workspace.py stage evals/<skill> --workspace <ws> --runs 3"
	@echo "  # executor fills outputs/response.md, outputs/metrics.json, timing.json"
	@echo "  $(PYTHON) scripts/eval_workspace.py check <ws>"
	@echo "  $(PYTHON) scripts/eval_grade.py <ws>/eval-<case>/<config>/run-N --case <case>.yaml --write"
	@echo "  $(PYTHON) scripts/eval_benchmark.py <ws> --skill-name <skill>"
	@echo ""
	@echo "To validate the suites without running anything:  make evals"
	@exit 1

test:
	$(PYTHON) -m unittest discover -s tests -v

# One starter per released package. The previous recipe built a single
# a single leftover Start.md that no longer exists — a leftover from when
# the repository held one skill — so this target could not complete.
# Derived from status, not a hand-kept list. The previous recipe named four
# conversions explicitly; when a skill gained a starter the recipe was updated
# and the parity check was not, so a generated DOCX went unverified. Two
# hand-kept lists of the same thing drift — now there are none.
docs:
	$(PYTHON) scripts/build_catalog_json.py
	$(PYTHON) scripts/build_docs.py
	$(PYTHON) scripts/build_catalog_docs.py

docs-check:
	$(PYTHON) scripts/build_catalog_json.py --check
	$(PYTHON) scripts/build_docs.py --check
	$(PYTHON) scripts/build_catalog_docs.py --check

media:
	$(PYTHON) scripts/build_demo_gif.py
	swift scripts/build_demo_mp4.swift docs/assets/demo docs/assets/clinpharm-pmx-skills-workflow.mp4

release-check: check
	$(PYTHON) scripts/build_release.py --check

all: docs media check
