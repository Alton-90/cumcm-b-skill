---
name: python-model-code-generator
description: Generate and run minimal reproducible Python modeling code for the human-approved main method and usable baseline, saving compact experiment artifacts and a canonical run summary.
---

# Preconditions

- G2.5 human method choice is recorded in `methods/Qx/qx_decisions.jsonl`.
- `code/Qx/qx_code_plan.md` exists.
- Required cleaned data and profile exist.
- The plan targets Python.

Legacy method pools and `code/model-code-analyzer.md` may be read during migration, but they do not override the human choice.

# Workflow

1. Read the code plan, decision ledger, method card, probe conditions, and data profile.
2. Confirm scope:
   - one approved main method;
   - one usable baseline;
   - fallback only when an activation decision or evidenced trigger exists.
3. Generate clear runnable `.py` files under `code/Qx/`.
4. Use project-root-safe paths, fixed seeds, explicit inputs, and minimal justified dependencies.
5. Save:
   - tables to `results/Qx/experiments/roundN/tables/`;
   - metrics to `.../metrics/`;
   - useful diagnostic/comparison figures to `.../figures/`;
   - canonical `run_summary.json`.
6. Evaluate and record output-degeneracy and fallback-trigger metrics required by the plan.
7. Materialize the planned input-population reconciliation before fitting: audited, parsed, excluded-by-reason, eligible, and per-method used row/entity counts. Stop rather than report success when counts do not reconcile or main/baseline silently use different comparison populations.
8. Apply any `candidate_screening_contract` before expensive evaluation. Preserve declared feasible anchors, coverage/diversity strata, and the out-of-rank exploration reserve; record retained/rejected counts by reason. Evaluate interacting components with the approved composition operator. Prefix exhaustion may trigger only the planned bounded diagnosis, not an infeasibility claim or silent fallback.
9. Implement any continuous universal-constraint certificate exactly as planned; do not promote arbitrary point sampling to a proof.
10. Materialize the output-obligation record and deterministic method/output fingerprints needed to bind later robustness and export to the exact selected strategy.
11. Persist full logs only on failure or when a warning needs reproduction.
12. Run the code. Do not claim success from code generation alone.
13. Hand off to `code-reviewer`.

# Script Layout

Prefer the smallest clear layout:

```text
code/Qx/
├── qx_code_plan.md
├── qx_baseline.py
├── qx_main.py
└── run_all.py        # only when coordination is useful
```

Do not create one script per unapproved candidate. Do not create a README that duplicates the code plan.

# Run Summary

Follow the schema in `model-code-analyzer`. Include:

- approved decision ID;
- method IDs and roles;
- inputs and outputs;
- seed and environment;
- execution status and timing;
- compact metric summaries;
- output-degeneracy evidence;
- warnings/errors;
- fallback-trigger state.
- input-population reconciliation and comparison-population identity when applicable.
- candidate-screening retention/rejection evidence, bounded-diagnosis state, composition operator, and continuous-constraint certificate when applicable.
- output-obligation status and per-method output fingerprints sufficient to identify the exact later selection.

# Rules

- Do not change the approved model or baseline.
- Do not read or overwrite raw data.
- Do not hide assumptions in code.
- Do not discard rows or entities without a recorded prospective exclusion reason and reconciled counts.
- Do not infer infeasibility from a failed proxy prefix, discard declared feasibility anchors/exploration reserve, or replace a joint evaluator with unproved standalone-score addition.
- Do not label a finite sample as a continuous-constraint certificate without the planned reduction or error bound.
- Do not emit placeholder metrics, figures, or successful statuses.
- Prefer portable `.py` scripts over notebook-only workflows.
- Keep intermediate files only when needed for explanation, review, robustness, or debugging.
- Use Type 1 diagnostic figures internally; do not present them as paper figures.

# Verification

- Main and baseline both ran and are directly comparable.
- Fallback code is absent unless activated.
- Formal outputs and run summary exist.
- Seed, inputs, versions, warnings, and errors are recorded.
- Required concentration/degeneracy checks are saved.
- Applicable candidate-screening and output-obligation contracts are fully materialized.
- Next handoff is `code-reviewer`.

# Structural method handoff

When the method card cites a solution playbook, read that specific file via [the local index](../method-selector/references/solution-playbooks.md). Preserve its task-specific mathematical/input/output mapping and apply only relevant validation checks within existing plan, review or robustness artifacts. Adapt a runnable baseline to all real task obligations; synthetic examples never replace contest evidence. A language port needs its own execution evidence. No additional choice card or artifact is required merely for using a playbook.
