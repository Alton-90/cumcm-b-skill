---
name: final-method-explainer
description: Build the authoritative final method explanation for a submission-ready subquestion from the method card, human decision ledger, code plan, final results, and robustness evidence.
---

# Purpose

Explain the selected method completely without re-authoring why the human chose it.

# Preconditions

- `rigor_profile` is `submission` or writer handoff is explicitly requested.
- Human method choice and result verdicts are recorded in `qx_decisions.jsonl`.
- Approved code ran and final result/robustness evidence exists.

# Sources

Use:

- `qx_method_card.json`
- `qx_decisions.jsonl`
- `planning/model_assumptions.md`
- `planning/symbol_table.md`
- `qx_code_plan.md`
- final run summary and result analysis
- robustness summary/report

Read legacy candidate and iteration logs only for migration.

# Workflow

1. Resolve the final method and baseline from the latest non-stale human decisions.
2. Transcribe the human's selection rationale faithfully and cite its `decision_id`.
3. Explain:
   - goal and scope;
   - assumptions, including human-confirmed necessity labels;
   - symbols and units;
   - mathematical formulation;
   - inputs, outputs, objective/criteria, and constraints;
   - solution procedure;
   - baseline and why it is valid;
   - fallback trigger and whether it fired;
   - validation, robustness, limitations, and applicable range.
4. Ensure formulas match code and symbol table.
5. Save `methods/Qx/qx_final_method_explanation.md`.

# Rules

- Do not infer the chosen method from best metrics.
- Do not invent the why-this-method narrative.
- Do not create a new pending decision artifact.
- Do not restate a long iteration diary; include only material eliminated alternatives and evidence.
- Do not include unsupported numerical claims.

# Verification

- Final method and rationale trace to decision IDs.
- Assumptions, symbols, formulas, units, and code agree.
- Baseline is usable rather than merely diagnostic.
- Risks, fallback behavior, and limitations are explicit.
- The explanation is self-contained enough for the writer.

# R6 canonical machine contract

Authoritative JSON schemas: [report-binding](../workflow-orchestrator/schemas/report-binding.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.

For a durable/final readable report, save `results/Qx/reports/method_explanation.json` using [report-binding.schema.json](../workflow-orchestrator/schemas/report-binding.schema.json), report_kind=method_explanation, its report hash and actual input hashes. Global symbols/assumptions/references use question_id=null; per-Q reports use the real question ID.
