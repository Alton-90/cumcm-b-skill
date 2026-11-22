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

# Verification

- Every major final claim has a supporting check or explicit limitation.
- Perturbations are justified and reproducible.
- Baseline and main comparisons remain metric-compatible.
- Applicable hard operating constraints are evaluated across predeclared group-safe perturbations; any abstention/triage path exposes action nondegeneracy and coverage/deferral.
- Concentration/degeneracy risks are revisited when relevant.
- Submission report sources its numbers from the summary and experiment artifacts.
