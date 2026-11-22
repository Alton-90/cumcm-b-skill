---
name: model-code-analyzer
description: Translate a human-approved main method and usable baseline into a minimal language-neutral implementation and experiment contract. Use after G2.5 and data readiness, before Python or MATLAB code generation.
---

# Purpose

Define exactly what code must implement and save. Do not expand the approved experiment scope or fully plan a dormant fallback.

# Preconditions

- `methods/Qx/qx_method_card.md` and probe summary exist.
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
6. Define the round output:

```text
results/Qx/experiments/roundN/
├── figures/
├── tables/
├── metrics/
└── run_summary.json
```

Create `logs/` only for failures, warnings, or reproducibility needs.
7. Write `code/Qx/qx_code_plan.md` for Python or `code/matlab/Qx/qx_code_plan.md` for MATLAB.
8. Hand off to the matching language generator.

# Run Summary Contract

Require:

```json
{
  "schema_version": 1,
  "question": "Q1",
  "round": "round1",
  "implementation_target": "python",
  "random_seed": 2026,
  "approved_decision_id": "q1_method_choice",
  "methods": [
    {
      "method_id": "M1",
      "role": "usable_baseline",
      "script": "code/Q1/q1_baseline.py",
      "status": "success",
      "execution_time_seconds": 0,
      "input_files": [],
      "output_files": [],
      "figure_files": [],
      "metrics_summary": {},
      "information_boundary_check": {"status": "NOT_APPLICABLE", "evidence": []},
      "objective_values": [],
      "constraint_violations": [],
      "upstream_artifacts": [],
      "warnings": [],
      "errors": []
    }
  ],
  "comparison": {},
  "contract_evidence": {
    "objective_contract": {},
    "unresolved_tradeoffs": [],
    "shared_information_boundary": {},
    "upstream_artifact_contract": [],
    "analysis_domain_contract": {"status": "NOT_APPLICABLE", "prospective_rule": "", "included": null, "excluded": null, "evidence": []}
  },
  "fallback_trigger": {
    "fallback_id": null,
    "condition": null,
    "observed": false,
    "evidence": null
  },
  "environment": {}
}
```

# Code Plan Contents

- target language and round purpose;
- approved decision ID;
- main and baseline IDs and roles;
- input fields and units;
- per-method computation steps;
- comparable outputs and metrics;
- shared information-boundary checks, objective values, constraint-violation reporting, and upstream artifact identity/version/hash/uncertainty for both main and baseline;
- prospective analysis-domain rule/mask, eligibility evidence, included/excluded counts or ranges, and post-hoc-selection guard when applicable;
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
- Do not require success logs.
- Do not create a README when the code plan already provides the same instructions.
- Stop if a human choice, required parameter, input field, or comparable baseline output is missing.

# Verification

- Plan scope is exactly main plus usable baseline unless fallback activation is recorded.
- Outputs are directly comparable.
- Probe risks and fallback trigger are represented in `run_summary.json`.
- Both method records carry the same applicable contract evidence and report objective values and constraint violations separately.
- Any applicable analysis-domain contract is prospective, executable, shared where required, and auditable in the run summary.
- Paths follow the experiment contract.
- Handoff targets the correct language generator.
