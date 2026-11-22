---
name: matlab-model-code-generator
description: Generate and run minimal reproducible MATLAB or Beita Tianyuan compatible code for the human-approved main method and usable baseline, with compact experiment artifacts and a canonical run summary.
---

# Preconditions

- G2.5 human method choice is recorded.
- `code/matlab/Qx/qx_code_plan.md` exists.
- Required cleaned data and profile exist.
- The plan targets MATLAB or 北太天元.

Legacy artifacts may be read during migration but do not override the human decision.

# Workflow

1. Read the code plan, decision ledger, method card, probe conditions, and data profile.
2. Confirm scope: approved main plus usable baseline. Implement a fallback only after activation.
3. Generate conservative `.m` files under `code/matlab/Qx/`.
4. Prefer basic matrix/table operations and avoid optional toolboxes unless the plan approves them.
5. Save tables, metrics, useful figures, and `run_summary.json` under `results/Qx/experiments/roundN/`.
6. Evaluate output-degeneracy and fallback-trigger metrics required by the plan.
7. Materialize the planned input-population reconciliation before fitting: audited, parsed, excluded-by-reason, eligible, and per-method used row/entity counts. Stop rather than report success when counts do not reconcile or main/baseline silently use different comparison populations.
8. Apply any planned candidate-screening contract: retain feasible anchors, prospective coverage/diversity strata, and out-of-rank exploration; record retained/rejected reasons; evaluate interacting components with the approved joint operator; and allow prefix failure to trigger only the bounded diagnosis.
9. Implement the planned analytic, conservative, or convergence-backed certificate for any continuous universal constraint, and save output-obligation status plus deterministic per-method output fingerprints.
10. Use `diary` or another full log only for a failure or reproducibility warning.
11. Run in the available compatible runtime. If unavailable, report the unexecuted state explicitly.
12. Hand off to `code-reviewer`.

# Script Layout

```text
code/matlab/Qx/
├── qx_code_plan.md
├── qx_baseline.m
├── qx_main.m
└── run_all.m        % only when useful
```

Do not create scripts for unapproved candidates or a duplicate README.

# Compatibility Rules

- Prefer `readtable`, `readmatrix`, `writetable`, `writematrix`, `save`, `load`, and `fullfile`.
- Use `rng(2026)` or the recorded seed.
- Use `jsonencode` when supported; otherwise write the required JSON fields deterministically.
- Avoid Live Scripts, App Designer, GUI code, Simulink, and toolbox-only functions unless explicitly approved.
- Note any 北太天元 compatibility risk in the run summary.

# Run Summary

Follow the `model-code-analyzer` contract, including approved decision ID, roles, paths, metrics, output-degeneracy evidence, fallback state, timing, seed, environment, warnings, and errors.

When applicable, also record audited-to-used row/entity reconciliation, authorized exclusion reasons, and the comparison-population identity used by each method.

Also record any proxy/final-evaluator screening contract, coverage reserve, joint-composition evidence, bounded-diagnosis state, continuous-constraint certificate, output obligations, and per-method output fingerprints.

# Rules

- Do not change the selected mathematical method.
- Do not access or overwrite raw data.
- Do not fabricate successful execution when MATLAB/北太天元 is unavailable.
- Do not discard rows or entities without a recorded prospective exclusion reason and reconciled counts.
- Do not infer infeasibility from a proxy-truncated prefix, remove declared feasibility anchors/exploration, or score interacting components only by an unproved sum of standalone values.
- Do not present arbitrary discretization as a certificate for a continuous universal constraint.
- Keep only evidence-bearing intermediate outputs.
- Separate Type 1 diagnostics from paper figures.

# Verification

- Main and baseline are directly comparable and both executed when a runtime is available.
- Fallback code exists only when activated.
- Formal outputs and run summary exist.
- Compatibility, seed, inputs, warnings, and errors are recorded.
- Required concentration/degeneracy checks are saved.
- Applicable candidate-screening and output-obligation contracts are fully materialized.
- Next handoff is `code-reviewer`.
