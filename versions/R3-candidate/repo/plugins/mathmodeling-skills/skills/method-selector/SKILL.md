---
name: method-selector
description: Build and risk-screen a compact role-based method shortlist for a mathematical-modeling subquestion. Use after problem framing and data profiling, before model code generation, to propose a main candidate, a usable baseline, and at most one conditional fallback without padding the pool.
---

# Purpose

Convert the framed problem and data profile into a small executable decision surface. Screen methods for load-bearing data, assumption, degeneracy, sensitivity, and scale risks before asking the human to choose.

This skill proposes and probes methods. The human chooses the method.

# Preconditions

- G1 problem framing passed.
- Required output and evaluation criteria are known.
- Relevant data inventory or audit exists.
- `planning/symbol_table.md` and `planning/model_assumptions.md` exist when the problem needs them.

If these are missing, return to the producer skill rather than guessing.

# Inputs

- Problem parse and classification.
- Data audit, including missingness, effective sample size, imbalance, cardinality, and distribution summaries.
- Literature analysis when available.
- Contest deadline, implementation language, interpretability needs, and compute limits.
- `planning/session_config.json`.
- Existing `methods/Qx/qx_method_card.md` and decision ledger when revising.

# Workflow

1. **Align the decision surface.**
   - Invoke `decision-prompt-builder` before generating an open-ended shortlist.
   - Ask about human-owned trade-offs, not algorithm names.
   - Reuse answers already present in the decision ledger.

2. **Derive method requirements.**
   - Consume applicable `decision_context`, `objective_contract`, and typed cross-question dependencies from the problem parse.
   - Start from required output, hard constraints, data characteristics, validation criteria, explanation burden, and experiment budget.
   - Screen information availability at each decision time before scoring a method. A method that uses forbidden future information is `FAIL`; incomplete evidence may be `CONDITIONAL` only with a concrete boundary-respecting repair.
   - Treat hard feasibility as prior to objective comparison. Do not scalarize objectives or resolve an unresolved trade-off unless the human has approved that choice.
   - For a classification, ranking, screening, or alarm decision with a hard operating target, define an `operating_point_contract` before comparing candidates: decision unit and positive class; constrained metric and human-supplied bound; grouping key; threshold/policy calibration data versus untouched evaluation data; action labels; and any abstention/deferral semantics and required coverage metric. Main and baseline must use the same contract.
   - Identify the failure modes that would make a method unusable.

3. **Create a role-based shortlist.**
   - One `main_candidate`: best fit to the chosen trade-off.
   - One `usable_baseline`: completes the real task and yields directly comparable outputs.
   - At most one `conditional_fallback`: differs in a meaningful mathematical way and has an explicit activation trigger.
   - If a simple reference cannot complete the real task, label it `diagnostic_reference`; it does not satisfy the baseline requirement.
   - Do not add a method merely to reach a candidate count.

4. **Define method-specific risk checks.**
   - Use the contract in `references/risk-probe-contract.md`.
   - Select only relevant assumption checks.
   - Always check output degeneracy or concentration with metrics appropriate to the output.
   - When a method relies on periodicity, stationarity, smoothness, a valid sensor range, or another local-domain property, probe that property on the proposed analysis domain. Define the inclusion/exclusion rule prospectively from admissible evidence; never select the domain after seeing which band gives the preferred result.
   - When a threshold or action policy is learned from data, require group-aware calibration inside training/resampling partitions; outer evaluation labels may score but never select that threshold or policy. Predeclare how the hard operating target will be checked across meaningful split/seed perturbations and what fallback or claim downgrade follows instability.
   - Bound probe runtime rather than source-line count.

5. **Run the risk probe on the main candidate and usable baseline.**
   - Use a representative slice or full-data diagnostic as appropriate; never rely only on the first rows.
   - The probe may use reusable scripts and may save detailed metrics, but its canonical output is one compact summary.
   - Probe the fallback only enough to establish that its trigger and risk profile are credible. Do not fully implement it.

6. **Write canonical artifacts.**
   - `methods/Qx/qx_method_card.md`
   - `methods/Qx/probes/risk_probe_summary.json`
   - Update `planning/manifests/Qx.json` if present.

7. **Ask for the method choice.**
   - Present the probe evidence through a choice card.
   - After the user answers, hand the exact answer to `modeler-decision-logger` for append-only capture in `methods/Qx/qx_decisions.jsonl`.
   - If no answer is available, stop. Do not create a placeholder decision file.

# Method Card Contract

`qx_method_card.md` stays compact and contains:

```markdown
# Qx Method Card

## Goal and success criteria

## Contract compatibility
- Information boundary and state update:
- Objective roles, directions, units, aggregation, and thresholds:
- Operating point, grouping, calibration/evaluation split, actions, and abstention semantics when applicable:
- Unresolved human trade-offs:
- Required upstream artifacts, identity/freshness, and uncertainty:

## Human constraints
- Output form:
- Priority:
- Unacceptable failure:
- Experiment budget:

## Shortlist
| ID | Role | Mathematical idea | Why eligible | Main risk | Implementation cost |

## Baseline validity
- Real task completed:
- Comparable output/metric:
- If no, classification: diagnostic_reference

## Risk-probe summary
| ID | Executability | Data/assumptions | Degeneracy | Sensitivity | Scale | Verdict |

## Fallback trigger
- Trigger:
- Evidence to evaluate:

## Compact history
- One line per material change, with decision_id when human-owned.
```

Do not maintain a separate iteration log for new work.

# Probe Verdicts

- `PASS`: eligible for the human choice.
- `CONDITIONAL`: eligible only with a stated mitigation or fallback trigger.
- `FAIL`: not offered as a selectable main or baseline.

A method fails screening when a load-bearing assumption fails, the output degenerates, it cannot produce a legal result, or its cost violates the user's budget. A method does not fail merely because an irrelevant generic diagnostic is unavailable.

It also fails when its load-bearing analysis-domain property is violated or unresolved. It may remain `CONDITIONAL` only when a prospective, evidence-backed domain rule and fallback are recorded before execution; merely warning about bad observations while still fitting them is not a mitigation.

For an applicable operating-point contract, it also fails when threshold or policy selection reads outer-evaluation labels, repeated entities can cross calibration/evaluation partitions, the hard constraint lacks a predeclared stability check, or abstentions are hidden or counted as ordinary negatives. A fallback may remain conditional only with explicit action and reporting semantics.

It also fails when it requires forbidden future information, silently scalarizes an unapproved objective trade-off, or treats an infeasible output as eligible because another objective is better. A stated repair may support `CONDITIONAL` only when it removes that violation without making the decision for the human.

# Output and Handoff

After G2 screening:

- If the human choice is absent: return the evidence-backed choice card.
- If G2.5 is decided: hand the method card, probe summary, chosen IDs, and experiment budget to `model-code-analyzer`.
- Instruct code generation to implement only the approved main method and usable baseline.
- Keep the fallback dormant until its recorded trigger fires.

# Rules

- Do not use a fixed candidate count.
- Do not use source-line count as validation quality.
- Do not invent missing data fields, constraints, labels, or evaluation metrics.
- Do not call a nonfunctional toy method a baseline.
- Do not fully implement all shortlisted methods.
- Do not select the method or write the human rationale.
- Do not substitute a better total objective for hard-constraint feasibility.
- Do not invent an operating threshold, abstention rule, or capacity ceiling; expose the human-owned trade-off when it is missing.
- Respect typed upstream dependencies and their uncertainty; do not offer a method that consumes an absent, stale, mismatched, or incompatible required artifact.
- Keep AI suggestions visibly separate from the human decision.

# Compatibility

When revising an older workspace, read:

- `methods/Qx/qx_method_candidates.md`
- `methods/Qx/qx_method_iteration_log.md`
- `methods/Qx/poc/`

Migrate material evidence into the method card and probe summary. Do not require new legacy PoCs or iteration logs.

# References

- Risk checks and summary schema: `references/risk-probe-contract.md`
- Method-family routing cues: `references/method-family-guide.md`

# Verification

- Shortlist contains a main candidate and a genuinely usable baseline.
- Optional fallback has a concrete trigger.
- Main and baseline have evidence-backed probe verdicts.
- Any structure-dependent main/baseline has a shared, prospective analysis-domain rule with eligibility evidence, or is blocked.
- Any applicable operating-point contract is prospective, group-safe, evaluation-isolated, shared by main/baseline, and includes visible abstention/coverage semantics.
- Output-degeneracy checks are present.
- Method card and probe summary exist.
- No per-skill pending decision file was created.
- No code-generation handoff occurs before a human method choice is recorded.
