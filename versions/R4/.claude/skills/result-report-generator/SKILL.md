---
name: result-report-generator
description: Summarize modeling experiment evidence, compare the approved main method with a usable baseline, surface fallback triggers, and produce a decision-point or final report without creating routine per-round prose.
---

# Purpose

Turn saved experiment artifacts into compact evidence. Do not treat ordinary successful runs as requiring a long report, and do not choose the winning method.

# Inputs

- `run_summary.json`
- method card and probe summary
- decision ledger
- saved tables, metrics, and figures
- session `rigor_profile`

Stop if the run summary claims outputs that do not exist or if main and baseline are not comparable.

For final export or a completion report, also stop when the current selected-output fingerprint lacks matching stability evidence, output obligations are unresolved, or a selection change left dependent artifacts stale. An immutable evidence freeze may still record a conditional result when its manifest sets `task_completion=false` and keeps final assembly blocked.

For a classification operating target, also stop when main and baseline use different action/metric semantics, threshold calibration touched outer-evaluation labels, or abstention/deferral accounting is absent.

# Modes

## Ordinary lean round

- Validate the run summary and referenced artifacts.
- Return a compact evidence digest in the conversation.
- Do not save a Markdown report unless:
  - a fallback trigger fired;
  - a material anomaly or contradiction exists;
  - the human must make a proceed/adjust/fallback decision.

## Decision-point round

Save:

`results/Qx/experiments/roundN/qx_decision_report.md`

Include only:

- main vs baseline metrics;
- output-degeneracy/concentration evidence;
- assumption or feasibility warnings;
- robustness evidence already available;
- fallback trigger state;
- unresolved trade-offs.
- hard operating-constraint stability and, when applicable, disjoint action counts plus coverage/deferral; keep abstentions separate from negative predictions.

Then invoke `decision-prompt-builder`. After the human answers, route the answer to `modeler-decision-logger`.

## Final/submission mode

Save:

`results/Qx/reports/qx_final_result_analysis.md`

Include:

- final main/baseline comparison;
- uncertainty and error;
- concentration/degeneracy interpretation;
- robustness links;
- limitations and applicable scope;
- exact source paths for numerical claims.
- the declared operating population, perturbation feasibility evidence, and coverage/deferral limits when classification uses abstention or triage.
- required output items, legal-zero/missing rules, unresolved obligations, selected-output fingerprint, matching robustness verdict, and `evidence_frozen` versus `task_completion` status.

# Rejection and Fallback

- Archive a method only after a human `result_verdict` or `fallback_activation` decision.
- Move rejected code and outputs to `workspace/archived/<Qx>/<method>_REJECTED_roundN/`.
- Add one compact history line to `qx_method_card.md`; do not create a separate iteration log.
- Do not archive from an AI suggestion alone.

# Rules

- Do not fabricate metrics, comparisons, or interpretations.
- Separate facts from human verdicts.
- Do not create `result-report-generator_modeler_decision.md`.
- Do not repeat the full run summary; cite it and extract only decision-relevant evidence.
- Do not call a diagnostic reference a usable baseline.
- Do not generate paper prose.
- Do not describe abstentions as negatives, hide the deferred fraction, or imply a capacity guarantee that was not supplied and tested.
- Do not relabel a surviving baseline as the main method. If the main fails or the baseline strictly wins under the approved comparison, report the actual selected identity and route one bounded triage over existing alternatives before proposing new search.
- Do not reuse reports, sensitivities, tables, or exports tied to an old selected-output fingerprint; refresh the affected artifacts or mark them stale/not applicable.

# Verification

- Every reported number resolves to a saved artifact.
- Main/baseline comparison uses the same split, unit, and metric definition.
- Applicable classification comparison uses the same operating-point and action semantics and reports hard-constraint stability plus coverage/deferral.
- Output concentration and fallback trigger are addressed.
- Final/export reports distinguish evidence freeze from task completion, satisfy output obligations, and cite robustness for the exact selected fingerprint with no undeclared stale dependents.
- Reports are generated only at decision points or final mode.
- Human verdicts are read from or appended to the canonical JSONL ledger.
