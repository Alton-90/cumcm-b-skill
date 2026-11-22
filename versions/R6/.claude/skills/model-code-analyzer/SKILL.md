---
name: model-code-analyzer
description: Translate a human-approved main method and usable baseline into a minimal language-neutral implementation and experiment contract. Use after G2.5 and data readiness, before Python or MATLAB code generation.
---

# Purpose

Define exactly what code must implement and save. Do not expand the approved experiment scope or fully plan a dormant fallback.

# Preconditions

- `methods/Qx/qx_method_card.json` and probe summary exist.
- `methods/Qx/qx_decisions.jsonl` contains a human `DECIDED` method choice.
- A usable baseline is identified.
- Cleaned data and `data_profile.json` are ready when data is required.
- Implementation target and round are known.

Read legacy candidate/decision artifacts only when the new artifacts are absent.

# Workflow

1. Read the approved choice, method card, probe conditions, and experiment budget.
2. Plan only:
   - approved `main`;
   - approved `usable_baseline`;
   - shared helpers and comparison logic.
3. Record the fallback ID and trigger, but do not plan its full implementation unless the trigger is already evidenced and the human chose activation.
4. Map mathematical definitions to inputs, processing steps, intermediate evidence, outputs, and validation checks.
5. Carry the applicable information boundary, objective roles, hard constraints, and typed upstream artifact identities into one shared contract for main and baseline. Define a directly comparable metric/output contract only after feasibility is checked.
   - If either method relies on local data properties, carry the approved `analysis_domain_contract` into the shared contract: exact prospective rule or mask derivation, evidence source, excluded-domain reporting, and a check that execution cannot choose a band from outcome quality. Main and baseline must share the rule unless the human-approved method definition explicitly requires otherwise.
   - When data are row- or entity-based, carry an `input_population_contract`: audited, parsed, excluded, eligible, and used row/entity counts; prospectively authorized exclusion reasons; arithmetic reconciliation; and one comparison-population identity shared by main and baseline unless the approved method meaning explicitly requires and explains a difference.
   - For an applicable classification operating target, carry the approved `operating_point_contract`: decision unit, positive class, grouping key, hard metric/bound, calibration-versus-evaluation boundary, action labels, abstention/deferral semantics, and required coverage metrics. Threshold or policy selection must remain inside training/calibration partitions.
   - If a cheaper proxy screens candidates before the hard evaluator, carry a `candidate_screening_contract`: proxy/final-evaluator identities, feasible anchors, prospective coverage or diversity strata, out-of-rank exploration reserve, retained/rejected counts, joint-composition semantics, and the single bounded diagnosis allowed before declaring prefix failure or activating fallback. For continuous universal constraints, name the analytic reduction, conservative enclosure, or convergence/error certificate used by the final evaluator.
   - Carry an `output_obligation_contract` from the problem parse: required entities/slots, when zero or missing output is legal, how conditional obligations are reported, and which artifacts depend on the finally selected method. Predeclare a selected-output fingerprint over method ID, parameters, composition, evaluator, resolution/tolerances, and source-run identity for later robustness and export checks.
6. Define the round output:

```text
results/Qx/experiments/roundN/
├── figures/
├── tables/
├── metrics/
└── run_summary.json
```

Create `logs/` only for failures, warnings, or reproducibility needs.
7. Write the shared `code/Qx/qx_code_plan.md`; scripts go under python/ or matlab/ below code/Qx.
8. Hand off to the matching language generator.

# Run Summary Contract

Require:

The versioned schema linked below is the only machine contract; do not copy legacy examples.

# Code Plan Contents

- target language and round purpose;
- approved decision ID;
- main and baseline IDs and roles;
- input fields and units;
- per-method computation steps;
- comparable outputs and metrics;
- shared information-boundary checks, objective values, constraint-violation reporting, and upstream artifact identity/version/hash/uncertainty for both main and baseline;
- prospective analysis-domain rule/mask, eligibility evidence, included/excluded counts or ranges, and post-hoc-selection guard when applicable;
- audited-to-used row/entity reconciliation, authorized exclusion reasons, and main/baseline comparison-population identity when data are row- or entity-based;
- group-safe training-only threshold/policy calibration, hard operating constraints, action labels, and abstention/coverage metrics when applicable;
- feasibility- and interaction-preserving candidate screening, bounded rejection-cause diagnosis, and any continuous-constraint certificate when a proxy or finite screen is used;
- output obligations plus the exact selected-output fingerprint and dependent artifacts that must be fresh before final export;
- risk-probe conditions that implementation must monitor;
- fallback trigger evaluation;
- paths, seed, dependencies, and expected runtime;
- named review checks expected downstream.

# Rules

- Do not write executable model code.
- Do not add candidates or change model meaning.
- Do not plan a diagnostic reference as the official baseline.
- Do not implement a fallback before activation.
- Do not give main and baseline different information, objective, constraint, or upstream-artifact contracts.
- Stop when a required upstream artifact is missing, stale, identity-mismatched, or uncertainty-incompatible, or when a required objective trade-off remains unapproved.
- Stop when a load-bearing analysis-domain property is unresolved, its rule was chosen after outcome inspection, or the plan only warns about ineligible observations while still using them.
- Stop when audited input cannot reconcile to the eligible and used populations, an exclusion lacks a prospective reason, or main and baseline silently use different comparison populations.
- Stop when an applicable threshold/policy can read outer-evaluation labels, repeated entities can cross partitions, or abstention and coverage semantics are unresolved.
- Stop when a proxy-truncated prefix can erase all feasible or interaction-relevant candidates without declared anchors, coverage/exploration, and a bounded diagnosis, or when joint feasibility is replaced by unproved standalone-score addition.
- Stop when a finite check is presented as a certificate for a continuous universal constraint without a defensible reduction, conservative enclosure, or convergence/error bound.
- Do not require success logs.
- Do not create a README when the code plan already provides the same instructions.
- Stop if a human choice, required parameter, input field, or comparable baseline output is missing.

# Verification

- Plan scope is exactly main plus usable baseline unless fallback activation is recorded.
- Outputs are directly comparable.
- Probe risks and fallback trigger are represented in `run_summary.json`.
- Both method records carry the same applicable contract evidence and report objective values and constraint violations separately.
- Any applicable analysis-domain contract is prospective, executable, shared where required, and auditable in the run summary.
- Applicable input populations reconcile exactly and use one declared comparison identity across main and baseline unless an approved exception is explicit.
- Any applicable operating-point contract is group-safe, calibration/evaluation-isolated, executable, and exposes every action plus coverage/deferral metrics.
- Any applicable candidate-screening contract is prospective, preserves feasibility and interaction coverage within budget, and records why candidates were retained or rejected.
- Output obligations and selected-output fingerprint fields are executable and sufficient to detect stale robustness, reports, tables, or exports after a selection change.
- Paths follow the experiment contract.
- Handoff targets the correct language generator.

# Structural method handoff

When the method card cites a solution playbook, read that specific file via [the local index](../method-selector/references/solution-playbooks.md). Preserve its task-specific mathematical/input/output mapping and apply only relevant validation checks within existing plan, review or robustness artifacts. Adapt a runnable baseline to all real task obligations; synthetic examples never replace contest evidence. A language port needs its own execution evidence. No additional choice card or artifact is required merely for using a playbook.

# R6 canonical machine contract

Authoritative JSON schemas: [run-summary](../workflow-orchestrator/schemas/run-summary.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.
