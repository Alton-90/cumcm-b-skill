---
name: matlab-code-reviewer
description: Review, run, debug, and verify approved MATLAB or Beita Tianyuan modeling code against its plan, data contract, method decision, compatibility constraints, and experiment outputs, saving one compact JSON review.
---

# Preconditions

- MATLAB code and `code/Qx/qx_code_plan.md` exist.
- Approved decision, method card, data profile, and run summary are available.
- MATLAB or 北太天元 runtime availability is known.

# Workflow

1. Resolve approved main/baseline scope and any activated fallback.
2. Inspect and run the code when a compatible runtime is available.
3. Evaluate:
   - `syntax`
   - `input_contract`, including applicable information boundaries, required upstream artifact identity/version/hash/freshness/uncertainty, any approved prospective analysis-domain rule/mask, and exact audited-to-parsed-to-excluded/eligible-to-used row/entity reconciliation; reject unexplained losses or undeclared main/baseline population differences;
   - `method_alignment`, including forbidden future information, unapproved objective scalarization, group isolation, and training/calibration-only threshold or policy selection when an operating-point contract applies;
   - `candidate_screening`, when applicable: proxy/final-evaluator identity, retained feasibility anchors and coverage/exploration, reconciled rejection reasons, the actual joint-composition operator, bounded diagnosis before any prefix-based infeasibility conclusion, and a defensible certificate for continuous universal constraints;
   - `reproducibility`
   - `output_contract`, including per-method objective values, constraint violations, output-obligation status, and deterministic per-method output fingerprints; an infeasible output fails even if its total objective is better. For abstention/triage, verify disjoint exhaustive actions, never count abstention as negative, and require coverage/deferral plus the hard metric on its declared population under identical main/baseline semantics.
4. Include compatibility evidence for toolbox usage, `jsonencode`, file I/O, plotting/export, and 北太天元 constraints.
5. Add only relevant numerical, feasibility, leakage, or scale checks.
6. If runtime is unavailable, use `NOT_RUN` only for runtime-dependent items rather than claiming execution success; still perform static contract checks.
7. If asked to fix findings, patch minimally and rerun affected checks.
8. Save `code/Qx/reviews/qx_matlab_review.json`.

# Review Schema

Use the same schema as `python-code-reviewer`, with:

- `"language": "matlab"`
- `runtime`
- `compatibility_target`
- optional `compatibility` check

Required named checks use `PASS`, `FAIL`, or justified `NOT_APPLICABLE`; simple static/no-dependency fields may be `NOT_APPLICABLE` without penalty. Runtime-dependent checks use `NOT_RUN` when execution was impossible; this blocks G3 until executed. A better aggregate objective never overrides a failed named check.

# Rules

- Do not pad pass items.
- Do not fabricate MATLAB/北太天元 execution.
- Do not approve unavailable toolbox dependencies without an explicit target exception.
- Do not change the mathematical model silently.
- Fail the applicable check for lookahead, unapproved scalarization, an infeasible output, or a missing, stale, identity-mismatched, or uncertainty-incompatible required upstream artifact.
- Fail `input_contract` when a structure-dependent calculation uses observations outside its evidenced eligible domain, changes the domain after seeing outcome quality, omits the approved mask/rule, or merely warns about ineligible observations while retaining them.
- Fail `input_contract` when audited rows/entities do not reconcile through reason-coded exclusions to eligible and used populations, or main and baseline differ without an approved method-level exception.
- Fail the applicable named check when threshold/policy selection reads outer-evaluation labels, repeated entities cross partitions, hard-constraint stability evidence is absent, or an abstention is hidden or scored as a negative.
- Fail `candidate_screening` for lost declared anchors/coverage/exploration, unreconciled rejection counts, a prefix-based infeasibility claim without bounded diagnosis, unproved standalone scoring of interacting components, or an unsupported continuous-constraint certificate.
- Do not require a duplicate Markdown review.

# Verification

- Approved main and baseline scope is enforced.
- Compatibility constraints are checked.
- Run summary and outputs agree.
- Python and MATLAB/北太天元 apply the same information, objective, feasibility, and dependency semantics.
- Python and MATLAB/北太天元 enforce the same prospective analysis-domain rule and exclusion evidence when applicable.
- Python and MATLAB/北太天元 enforce the same population-reconciliation and operating-point/abstention semantics when applicable.
- Python and MATLAB/北太天元 enforce the same feasibility/interaction-preserving screening contract and expose the same output-obligation and fingerprint semantics.
- Verdict follows required check statuses and runtime evidence.

# Structural method handoff

When the method card cites a solution playbook, read that specific file via [the local index](../method-selector/references/solution-playbooks.md). Preserve its task-specific mathematical/input/output mapping and apply only relevant validation checks within existing plan, review or robustness artifacts. Adapt a runnable baseline to all real task obligations; synthetic examples never replace contest evidence. A language port needs its own execution evidence. No additional choice card or artifact is required merely for using a playbook.

# R6 canonical machine contract

Authoritative JSON schemas: [review](../workflow-orchestrator/schemas/review.schema.json). All new machine records use schema_version=2 and artifact_type; extension fields belong under extensions. JSONL decisions validate each record with decision.schema.json.

Read [paths and artifact ownership](../workflow-orchestrator/references/workspace-contract.md) for exact destinations and [gate execution](../workflow-orchestrator/references/gate-runtime.md) for command semantics. Markdown is a readable explanation, never an independent PASS/state source. After writing an artifact, validate the relevant gate; do not hand-write a passing gate result or reuse a stale result. Human/semantic judgment and machine validation are separate.
