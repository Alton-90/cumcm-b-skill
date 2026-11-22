# P17 Prospective Behavior Test Plan

These are contract fixtures, not model executions. Existing BT-01 through BT-08 remain unchanged. Only the two P16-approved gaps add coverage.

## BT-09 — Input-population reconciliation

- Reject silent loss between audited and parsed populations when no authorized exclusion explains it.
- Accept exact audited → parsed → eligible → used row/entity reconciliation with disjoint reason-coded exclusions.
- Reject undeclared main/baseline comparison-population mismatch.
- Confirm the contract is present in the planner, both generators, both language reviewers, and the orchestrator.

## BT-10 — Hard operating point and abstention semantics

- Reject threshold/policy selection that reads outer-evaluation labels.
- Reject repeated-entity overlap across calibration and evaluation.
- Reject a deferred/indeterminate action counted as negative or reported without coverage and deferral.
- Accept a group-isolated, training-calibrated, predeclared-stability triage contract with identical main/baseline actions.
- Confirm the contract is present across method selection, code planning/review, robustness, reporting, and orchestration.

The suite must pass once on the candidate. A failure permits only a targeted repair and rerun; a passing suite is not repeated for reassurance.
