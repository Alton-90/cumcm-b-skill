---
name: solution-package-builder
description: Assemble a submission-ready writer package from final method, result, robustness, figure, and human-decision artifacts, then freeze approved numerical claims with provenance.
---

# Purpose

Create the writer's single source package and immutable numerical snapshot. Do not manufacture missing judgments or freeze unapproved claims.

# Preconditions

- `rigor_profile` is `submission`.
- Final method explanation, final result analysis, robustness report, and figure plan exist.
- Human method, result, stability, and claim-scope decisions exist in `qx_decisions.jsonl`.
- Canonical sources are current.

# Workflow

1. Collect final method structure, result claims, limitations, figures, tables, and decision provenance.
2. Draft `results/Qx/reports/qx_solution_package_for_writer.md`.
3. Flag every proposed top-line claim with:
   - value and unit;
   - canonical source path and location;
   - robustness support;
   - decision ID for claim scope or rationale;
   - confidence/limitation.
4. Invoke one final choice card when package sign-off is missing:
   - keep;
   - downgrade;
   - drop.
5. Route the human answer to `modeler-decision-logger` as `package_signoff`.
6. Only after sign-off, execute freeze_results.py; never compose frozen values or their passing status manually.
7. Verify every numerical package claim resolves to the freeze and every judgment claim resolves to a human decision ID.

# Frozen Number Contract

Create results/Qx/reports/freeze_plan.json (claim IDs, canonical JSON source paths, RFC 6901 JSON Pointers and units; no copied values). Package sign-off must cite the current plan and selected run. Run scripts/freeze_results.py --workspace ROOT --question Qx --mode complete. Values are extracted by code from the selected method's registered outputs. CSV/table sources must first be converted to a traceable canonical metrics JSON by the experiment code; the freezer never guesses locators.

An evidence_only freeze can preserve judged failure/incompleteness, but does not pass G4B or allow paper/final assembly. Replacing a freeze requires renewed current sign-off and --replace-reason; the script preserves the prior snapshot and appends the change log. It is a versioned snapshot, not a tamper-proof immutable store.

# Rules

- Do not create `solution-package-builder_modeler_decision.md`.
- Do not emit `frozen_numbers.json` before human package sign-off.
- Never edit an existing freeze by hand.
- Transcribe human rationales; do not re-compose them as stronger claims.
- The package may cite the compact method-card history but must not depend on a separate iteration log.
- Do not copy raw exploratory outputs into the package without final validation.

# Change and Re-freeze

When a canonical source changes after freeze:

1. append the reason to `freeze_change_log.md`;
2. update and rerun the canonical source;
3. obtain renewed human judgment when the evidence changed materially;
4. regenerate the freeze;
5. run scoped consistency for Qx.

# Verification

- All prerequisites are final and current.
- Package sign-off exists in the JSONL ledger.
- Every frozen value has a real canonical source and stable locator.
- Every package number matches the freeze.
- Every modeling judgment traces to a human decision.
- Writer can use the package without searching scattered results.

# R6 canonical machine contract

Authoritative JSON schemas: [freeze-plan](../workflow-orchestrator/schemas/freeze-plan.schema.json); [frozen-numbers](../workflow-orchestrator/schemas/frozen-numbers.schema.json); [report-binding](../workflow-orchestrator/schemas/report-binding.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.

For a durable/final readable report, save `results/Qx/reports/writer_package.json` using [report-binding.schema.json](../workflow-orchestrator/schemas/report-binding.schema.json), report_kind=writer_package, its report hash and actual input hashes. Global symbols/assumptions/references use question_id=null; per-Q reports use the real question ID.
