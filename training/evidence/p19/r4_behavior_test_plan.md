# R4 Prospective Behavior Test Plan

The suite tests only CHG-B05 and CHG-B06. It does not rerun the frozen contest model.

## CHG-B05

- Accept a proxy screen that binds proxy/final evaluators, preserves anchors and prospective coverage strata, reserves out-of-rank exploration, reconciles counts, evaluates interactions jointly, and declares one bounded diagnosis.
- Reject lost anchors, zero exploration, unreconciled counts, standalone-score substitution for an interacting objective, prefix-based infeasibility without diagnosis, and unsupported finite sampling of a continuous universal constraint.
- Accept an analytic/conservative/convergence-backed continuous-constraint certificate.

## CHG-B06

- Accept an immutable evidence freeze with unresolved obligations only when `task_completion=false`.
- Accept completion/export only when obligations are satisfied, the robustness fingerprint exactly matches the selected output, and no dependent artifact is stale.
- Reject completion with unresolved obligations, fingerprint mismatch, stale artifacts, relabeled baseline identity, or more than one bounded failure triage before new search.

## Packaging invariants

- Nine affected Skills contain the prospective contracts in all three mirrors.
- The three mirrors are byte-identical for every affected Skill.
- Exactly 27 Skill files differ from immutable R3; no files are added or missing.
- Added Skill text contains no 2025A-specific values, identifiers, paths, or named algorithms.
