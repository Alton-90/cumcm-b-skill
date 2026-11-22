---
name: python-code-reviewer
description: Review, run, debug, and verify approved Python modeling code against its code plan, data contract, method decision, risk conditions, and experiment outputs, saving one compact JSON review.
---

# Preconditions

- Python code and `code/Qx/qx_code_plan.md` exist.
- Approved method decision, method card, data profile, and relevant run summary are available.
- Required inputs are accessible.

# Workflow

1. Resolve the approved main and usable baseline. Flag scripts for unapproved candidates unless a fallback activation exists.
2. Inspect and run the code in the intended order.
3. Evaluate required checks:
   - `syntax`: imports, execution, exceptions, and obvious runtime faults.
   - `input_contract`: paths, fields, units, shapes, missing-data handling, raw-data protection, applicable information boundaries, required upstream artifact identity/version/hash/freshness/uncertainty, any approved prospective analysis-domain rule/mask, and exact audited-to-parsed-to-excluded/eligible-to-used row/entity reconciliation. Reject unexplained losses and undeclared main/baseline population differences.
   - `method_alignment`: formulas, objectives, constraints, assumptions, main/baseline roles, and fallback scope match the approved plan; reject forbidden future information and unapproved objective scalarization. For an applicable operating-point contract, verify group isolation and that threshold/policy selection uses training/calibration data only, never outer-evaluation labels.
   - `reproducibility`: seed, deterministic setup, dependency/runtime record, and rerun consistency.
   - `output_contract`: saved tables/metrics/figures, valid run summary, comparable main/baseline metrics, per-method objective values, constraint violations, degeneracy evidence, and fallback-trigger state. Any infeasible output fails even if its total objective is better. For abstention/triage, actions must be disjoint and exhaustive, abstentions must not count as negatives, and coverage/deferral plus the hard metric on its declared population must be reported under identical main/baseline semantics.
4. Add risk-specific checks only when relevant, such as leakage, constraint feasibility, numerical stability, or scale.
5. If asked to fix findings, make minimal changes, rerun affected checks, and record the repair. Otherwise report findings without changing code.
6. Save `code/Qx/reviews/qx_python_review.json`.

# Review Schema

```json
{
  "schema_version": 1,
  "question_id": "Q1",
  "language": "python",
  "reviewed_files": [],
  "decision_id": "q1_method_choice",
  "checks": {
    "syntax": {"status": "PASS", "evidence": []},
    "input_contract": {"status": "PASS", "evidence": []},
    "method_alignment": {"status": "PASS", "evidence": []},
    "reproducibility": {"status": "PASS", "evidence": []},
    "output_contract": {"status": "PASS", "evidence": []}
  },
  "findings": [],
  "verdict": "PASSED",
  "reviewed_at": "ISO-8601"
}
```

Statuses are `PASS`, `FAIL`, or `NOT_APPLICABLE` with a reason. `NOT_APPLICABLE` is valid for genuinely static/no-dependency contract fields. Any required `FAIL` blocks G3; a better aggregate objective never overrides a failed named check.

# Rules

- Do not pad evidence to reach a count.
- Do not fabricate execution or outputs.
- Do not approve a toy diagnostic reference as the official baseline.
- Do not silently change mathematical meaning.
- Fail the applicable check for lookahead, unapproved scalarization, an infeasible output, or a missing, stale, identity-mismatched, or uncertainty-incompatible required upstream artifact.
- Fail `input_contract` when a structure-dependent calculation uses observations outside its evidenced eligible domain, changes the domain after seeing outcome quality, omits the approved mask/rule, or merely warns about ineligible observations while retaining them.
- Fail `input_contract` when audited rows/entities do not reconcile through exclusions to eligible and used populations, any exclusion reason is not prospectively authorized, or main and baseline use different comparison populations without an approved method-level exception.
- Fail the applicable named check when an operating threshold/policy reads outer-evaluation labels, repeated entities cross calibration/evaluation partitions, hard-constraint stability evidence is missing, or an abstention is hidden or scored as an ordinary negative.
- Do not create success logs beyond the review JSON.
- Treat code newer than its review as requiring the affected checks to rerun, not necessarily the entire pipeline.

# Verification

- Every required named check has concrete evidence.
- Main and baseline are approved and comparable.
- Run summary and on-disk outputs agree.
- Static contract checks still run when execution cannot; never classify an unchecked violation as a pass.
- Applicable analysis-domain selection is prospective and the run summary proves the exact rule used, including exclusions.
- Applicable population reconciliation is arithmetic, reason-coded, and tied to one declared main/baseline comparison identity.
- Applicable operating-point review proves group-safe training-only calibration, common action semantics, hard-constraint accounting, and explicit coverage/deferral.
- Review verdict follows check statuses.
