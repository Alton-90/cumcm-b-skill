---
name: robustness-checker
description: Design and run risk-targeted robustness, sensitivity, error, and baseline checks for an approved mathematical model, emitting compact machine evidence in lean mode and a final report in submission mode.
---

# Purpose

Test the claims most likely to fail. Choose checks from the model's assumptions and decision risks rather than filling a generic checklist.

# Preconditions

- Approved main and usable baseline executed.
- Run summary, method card, probe summary, and relevant outputs exist.
- Claim or decision to be tested is known.

# Workflow

1. Identify load-bearing assumptions and claims.
   - For a final-selection or export check, bind the test to an exact `selected_output_fingerprint`: method ID, parameters, component composition, evaluator, resolution/tolerances, and source-run identity. Evidence for a different fingerprint is stale, not transferable by similarity.
2. Select applicable checks:
   - parameter or weight perturbation;
   - alternate split or resampling;
   - seed stability;
   - outlier/missing-data treatment;
   - constraint/capacity perturbation;
   - baseline comparison;
   - output concentration/rank stability;
   - error and uncertainty analysis.
   - for a hard classification operating target: alternate group-safe split/resampling checks, with threshold or policy recalibration confined to each training/calibration partition;
   - for abstention/triage: action-state nondegeneracy, constraint metrics on the declared population, and coverage/deferral stability without treating abstentions as negatives.
3. State perturbation ranges and why they are meaningful before interpreting results.
   - Predeclare the pass rule for a hard operating constraint, including how many perturbations must be feasible and what fallback or claim downgrade follows failure. Do not choose this rule from the observed robustness result.
4. Run checks with fixed seeds where stochastic.
5. Save compact metrics to:

`robustness/Qx/qx_robustness_summary.json`

6. In `submission`, also save:

`robustness/Qx/qx_robustness_report.md`

7. If the stability verdict affects method continuation or claim scope, invoke one choice card and log the human answer in `qx_decisions.jsonl`.
8. When the selected method changes after a failed check, record the replacement fingerprint and list every selection-dependent report, sensitivity, table, or export that is stale. Recheck only the affected evidence; do not silently inherit the rejected strategy's robustness.

# Summary Contract

Record:

- tested claim/assumption;
- input and result source paths;
- perturbation;
- metric and threshold if predeclared;
- observed value;
- status `PASS`, `CONDITIONAL`, or `FAIL`;
- limitation;
- fallback-trigger relevance.
- selected-output fingerprint tested, whether it still matches the current selection, and selection-dependent artifacts made stale by any replacement;
- for an applicable hard operating target: group key, calibration/evaluation isolation, feasible perturbation count, metric range, and main/baseline comparison under the same action semantics;
- for abstention/triage: per-action counts or rates, coverage/deferral range, and explicit confirmation that abstentions were not scored as negatives.

# Rules

- Do not run irrelevant checks merely to reach a count.
- Do not invent a threshold after seeing the result without labeling it exploratory.
- Do not reuse outer-evaluation labels to recalibrate a threshold or allow repeated entities to cross resampling partitions.
- Do not let a favorable canonical split override failure of the predeclared operating-constraint stability rule.
- Do not convert stability metrics into the human confidence verdict.
- Do not create `robustness-checker_modeler_decision.md`.
- A failed robustness check is evidence for adjust/fallback/claim downgrade, not permission for AI to decide.
- Do not authorize final export or a completion claim from robustness evidence for a different method, parameter set, composition, evaluator, resolution, or source run.
- An immutable evidence freeze may preserve a conditional or failed result, but it must not be represented as task completion.

# Verification

- Every major final claim has a supporting check or explicit limitation.
- Perturbations are justified and reproducible.
- Baseline and main comparisons remain metric-compatible.
- Applicable hard operating constraints are evaluated across predeclared group-safe perturbations; any abstention/triage path exposes action nondegeneracy and coverage/deferral.
- Concentration/degeneracy risks are revisited when relevant.
- Final-selection checks match the exact current output fingerprint; any selection change has an explicit, minimal staleness/refresh record.
- Submission report sources its numbers from the summary and experiment artifacts.

# Structural method handoff

When the method card cites a solution playbook, read that specific file via [the local index](../method-selector/references/solution-playbooks.md). Preserve its task-specific mathematical/input/output mapping and apply only relevant validation checks within existing plan, review or robustness artifacts. Adapt a runnable baseline to all real task obligations; synthetic examples never replace contest evidence. A language port needs its own execution evidence. No additional choice card or artifact is required merely for using a playbook.

# R6 canonical machine contract

Authoritative JSON schemas: [robustness](../workflow-orchestrator/schemas/robustness.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.

For a durable/final readable report, save `results/Qx/reports/robustness_report.json` using [report-binding.schema.json](../workflow-orchestrator/schemas/report-binding.schema.json), report_kind=robustness_report, its report hash and actual input hashes. Global symbols/assumptions/references use question_id=null; per-Q reports use the real question ID.
