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
   - `input_contract`: paths, fields, units, shapes, missing-data handling, raw-data protection, applicable information boundaries, required upstream artifact identity/version/hash/freshness/uncertainty, and any approved prospective analysis-domain rule/mask with included/excluded evidence.
   - `method_alignment`: formulas, objectives, constraints, assumptions, main/baseline roles, and fallback scope match the approved plan; reject forbidden future information and unapproved objective scalarization.
   - `reproducibility`: seed, deterministic setup, dependency/runtime record, and rerun consistency.
   - `output_contract`: saved tables/metrics/figures, valid run summary, comparable main/baseline metrics, per-method objective values, constraint violations, degeneracy evidence, and fallback-trigger state. Any infeasible output fails even if its total objective is better.
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
- Do not create success logs beyond the review JSON.
- Treat code newer than its review as requiring the affected checks to rerun, not necessarily the entire pipeline.

# Verification

- Every required named check has concrete evidence.
- Main and baseline are approved and comparable.
- Run summary and on-disk outputs agree.
- Static contract checks still run when execution cannot; never classify an unchecked violation as a pass.
- Applicable analysis-domain selection is prospective and the run summary proves the exact rule used, including exclusions.
- Review verdict follows check statuses.
