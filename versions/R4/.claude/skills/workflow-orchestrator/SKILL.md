---
name: workflow-orchestrator
description: Inspect a mathematical-modeling workspace, evaluate lean or submission gates per subquestion, update machine-readable manifests, classify change impact, and route one next action without duplicating downstream work.
---

# Purpose

Act as the gate-driven scheduler and state reader. Do not solve models, write model code, or draft paper sections.

`../../AGENTS.md` is the packaged policy source. Prefer a project-root `AGENTS.md` when one exists; otherwise read the packaged copy relative to this `SKILL.md`. Apply that policy without reproducing large reports or dashboards.

# Session Start

Before orchestration in a new workspace:

- show `git status --short`;
- check the chosen runtime and required core packages;
- verify the workspace skeleton needed for the current request;
- read `planning/session_config.json`, accepting legacy `mode`.

Report warnings concisely. Do not create the full project skeleton unless the user is initializing a project.

# State Sources

Prefer, in order:

1. `planning/manifests/Qx.json`
2. canonical artifacts on disk
3. legacy dashboard and legacy method/decision artifacts

Never trust a dashboard over newer canonical artifacts.

# Manifest Contract

Maintain one compact JSON manifest per subquestion:

```json
{
  "schema_version": 1,
  "question_id": "Q1",
  "rigor_profile": "lean",
  "current_gate": "G2",
  "status": "method_screened_waiting_human",
  "artifacts": {
    "method_card": "methods/Q1/q1_method_card.md",
    "decision_ledger": "methods/Q1/q1_decisions.jsonl",
    "risk_probe": "methods/Q1/probes/risk_probe_summary.json",
    "latest_run": null
  },
  "dependency_gates": [],
  "allowed": {
    "code_generation": false,
    "freeze": false,
    "paper_writing": false,
    "final_assembly": false
  },
  "blockers": [],
  "result_readiness": {
    "selected_output_fingerprint": null,
    "output_obligations_satisfied": null,
    "matching_robustness_status": null,
    "evidence_frozen": false,
    "task_completion": false,
    "stale_artifacts": []
  },
  "next_action": {
    "owner": "human",
    "skill": "decision-prompt-builder",
    "reason": "method choice not recorded"
  },
  "updated_at": "ISO-8601"
}
```

Update only fields affected by the current state change. Generate a human dashboard on request or at a milestone; otherwise derive status directly from manifests.

# Gate Evaluation

Evaluate each Qx independently.

Before evaluating a downstream gate, apply a dependency gate only when its parse declares a real `cross_question_dependencies` entry. For each required upstream artifact, verify existence, required status, identity/version/hash, freshness, and uncertainty compatibility. A missing, stale, identity-mismatched, or uncertainty-incompatible artifact blocks only that downstream Qx and names the failed condition. Do not turn conceptual references into gates; a Qx with no real dependency remains eligible to progress in parallel.

## G1 — PROBLEM_FRAMED

Pass when parse, classification, data inventory, success criteria, and human framing exist. A placeholder in a human-owned field blocks the gate.

For a real upstream dependency, do not pass the relevant downstream gate until its dependency gate passes.

## G2 — METHOD_SCREENED

Pass when:

- `qx_method_card.md` defines a main candidate and usable baseline;
- the baseline completes the real task with comparable output;
- `risk_probe_summary.json` covers applicable checks, including output degeneracy;
- any load-bearing analysis-domain property is evidenced and its prospective inclusion/exclusion rule is fixed before execution;
- any applicable classification operating target fixes the decision unit, grouping boundary, calibration/evaluation separation, hard metric/bound, actions, and abstention/coverage semantics before implementation;
- any lossy proxy/top-k/beam screen has a prospective candidate-screening contract preserving feasible anchors, coverage/diversity, bounded out-of-rank exploration, interaction semantics, and one bounded coverage diagnosis; any finite certificate for a continuous universal constraint has a defensible reduction or error bound;
- main and baseline verdicts are `PASS` or justified `CONDITIONAL`;
- any fallback has a concrete trigger.

Do not require a fixed number of candidates, universal PoCs, or a source-line limit.

## G2.5 — METHOD_CHOSEN_BY_HUMAN

Pass when `qx_decisions.jsonl` contains a human `DECIDED` method choice citing probe evidence. While blocked, allow data preparation but not model code generation.

## G3 — CODE_AND_EXPERIMENT_REVIEWED

Pass when:

- approved main and baseline executed;
- latest `run_summary.json` is complete;
- language review contains passing named checks for syntax, input contract, method alignment, reproducibility, and output contract.
- when the method is domain-sensitive, the run and review prove that the approved analysis-domain rule was applied unchanged; an unresolved or post-hoc domain selection blocks G3.
- when data are row- or entity-based, the run and review reconcile audited, parsed, reason-coded excluded, eligible, and used populations; unexplained loss or an undeclared main/baseline population mismatch blocks G3.
- for an applicable operating-point contract, the run and review prove group-safe training/calibration-only threshold selection, identical main/baseline action semantics, and explicit hard-metric plus coverage/deferral accounting; outer-label tuning or treating abstention as negative blocks G3.
- when candidate screening applies, the run and review reconcile retained/rejected counts, prove declared anchors/coverage/exploration were preserved, evaluate interactions with the actual composition operator, and forbid a prefix-based infeasibility conclusion before the bounded diagnosis; unsupported continuous-constraint certificates block G3.

Accept legacy Markdown review artifacts during migration, but prefer JSON for new work.

## G4 — RESULTS_JUDGED_AND_FROZEN

In `lean`, pass the result-judgment subgate when final-result and stability decisions cite computed evidence. Continue iterating without freezing when the human selects `adjust` or `fallback`.

Keep `evidence_frozen` distinct from `task_completion`. A conditional, incomplete, or failed result may be immutably evidence-frozen with explicit limitations, but it must keep final export/paper/final assembly blocked unless the output-obligation contract is satisfied or an explicit claim downgrade accepts the unresolved items.

Before final export or a completion claim, require robustness evidence matching the exact selected-output fingerprint: method, parameters, composition, evaluator, resolution/tolerances, and source run. A method substitution or parameter/evaluator change makes selection-dependent reports, sensitivities, tables, and exports stale until refreshed or marked not applicable. If the main fails or a baseline strictly wins, preserve the actual method identity and allow at most one bounded failure triage over already-produced alternatives before scheduling new search.

For a hard classification operating claim, require the predeclared group-safe perturbation verdict. A favorable canonical split cannot override a failed stability rule; route failure to fallback, adjustment, or claim downgrade. If abstention/triage is active, require nondegenerate action evidence and visible coverage/deferral.

In `submission`, additionally require:

- final method explanation;
- final result analysis;
- robustness report;
- package sign-off in the decision ledger;
- solution package;
- current `frozen_numbers.json`.

## G5 — PAPER_SECTION_READY

Require the three writer rules, frozen-number sourcing, human-confirmed interpretation/claim scope, and verified figures.

## G6 — FINAL_AUDIT_PASSED

Evaluate only in `submission`. Require passing consistency, completeness, and QA artifacts. Never infer that one auditor covers another.

# Routing

Choose one primary next action:

- missing framing → parser/classifier or human framing card;
- failed real dependency gate → the upstream artifact owner or a refresh/uncertainty-resolution action; keep unrelated Qx runnable;
- missing data profile → `data-auditor-cleaner`;
- unresolved load-bearing analysis domain → the data profiler or method selector that owns the prospective eligibility rule;
- unreconciled input population → the code planner/generator or reviewer that owns audited-to-used counts and exclusion reasons;
- invalid operating-point calibration or abstention accounting → method selector, code reviewer, or robustness checker according to the earliest failed gate;
- lossy candidate screening, unsupported continuous certification, or prefix-only infeasibility → code planner/generator/reviewer at the earliest failed gate; run only the predeclared bounded coverage diagnosis before considering fallback;
- missing method card/probe → `method-selector`;
- missing human method choice → `decision-prompt-builder`;
- approved method without implementation plan → `model-code-analyzer`;
- code/review incomplete → language generator or reviewer;
- meaningful experiment awaiting judgment → result choice card;
- final results without robustness → `robustness-checker`;
- submission package incomplete → final explainer, result report, or package builder;
- paper ready but unaudited → the earliest missing final auditor.

Do not invoke several judgment-bearing skills speculatively.

# Change Impact

Classify changes before scheduling checks:

- `NONE`: scratch, formatting, comments, non-semantic docs.
- `LOCAL`: exploratory code or method-card updates before freeze.
- `CANONICAL`: schema/units, symbols, equations, parameters, official values, figure paths.
- `FROZEN`: changes affecting frozen values or paper claims.

Route checks:

- `NONE`: none.
- `LOCAL`: local tests/review.
- `CANONICAL`: scoped consistency for affected Qx.
- `FROZEN`: thaw log, rerun affected work, re-freeze, scoped consistency.

Never schedule a full-workspace consistency audit solely because more than one file changed.

# Lean vs Submission

In `lean`:

- require only manifests, method card, decision ledger, probe summary, and run summaries;
- do not require per-round Markdown reports, full success logs, frozen numbers, paper artifacts, or final audits;
- persist a detailed report only at a human decision point or final round.

In `submission`:

- require final explanations, reviews, analyses, robustness, package, freeze, paper, and G6;
- run the full three-auditor layer once before final assembly.

# Compatibility

Read legacy artifacts when new ones are absent:

- `planning/progress_dashboard.md`
- `qx_method_candidates.md`
- `qx_method_iteration_log.md`
- `qx_decision_log.md`
- `decisions/*_modeler_decision.md`
- Markdown code reviews

Mark them `legacy_source` in the manifest and recommend migration at the next material edit. Do not regenerate legacy files for new work.

# Output

Return a compact state report:

- profile;
- per-question current gate and blocker;
- artifacts changed or missing;
- change-impact class;
- one next action;
- optional runners-up only when they can proceed independently.

Do not paste a full dashboard or large JSON structure unless the user asks.

# Verification

- State is derived from current canonical artifacts.
- Dependency blocks are limited to declared real dependencies and explain artifact/status/identity/freshness/uncertainty failures.
- Lean requirements are not confused with submission requirements.
- Human decisions were not inferred from AI suggestions.
- Structure-dependent execution is blocked until its analysis-domain eligibility and prospective selection rule are evidenced.
- G3 is blocked by unreconciled input loss, undeclared main/baseline population differences, outer-evaluation threshold tuning, group leakage, or hidden abstention semantics.
- G4 hard classification claims follow the predeclared perturbation verdict and expose coverage/deferral when applicable.
- Evidence freeze and task completion are separate; final export uses matching exact-selection robustness, satisfied output obligations, truthful method identity, and no undeclared stale dependents.
- Code generation, freeze, paper writing, and final assembly flags match the gates.
- Audit scope matches semantic impact.
- Manifest and reported next action agree.
