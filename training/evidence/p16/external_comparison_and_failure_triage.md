# P16 External Comparison and Failure Triage — 2025 C

## Frozen boundary

This review begins only after the 2025 C blind workspace was frozen. The frozen blind-output manifest has SHA-256 `613a780af422d9412f69862bc098204d11c2499bf1bf4af6dec6c05b99a28e7a` and content fingerprint `8b78e27a921e0dc456ac9a2077ad788db5d0d60c212ddd0259b2ea9b783f2abd`. Nothing in `tests/holdout/2025C/B-LEAN-20260908-R2/contest_workspace/` may be rewritten by this review.

## External-reference availability

Disposition: `NO_APPLICABLE_REFERENCE_SOURCE`.

The curated corpus contains the official 2025 C problem and attachment under source `SRC-d38facaf8b96`, but no 2025 C answer, awarded paper, or expert commentary suitable for result comparison. The available 2025 answer papers B060/B157 and the expert commentary titled `碳化硅外延层厚度` concern the 2025 B problem and are not applicable comparison evidence for 2025 C. They were therefore not used to score, reinterpret, or revise the frozen C result. P16 relies on the frozen execution and failure traces only.

## Reusable-gap screen

Each proposed repair must satisfy all four iteration criteria: it changes a modeling decision or prevents a misleading/unreproducible output; it is a missing reusable Skill contract rather than task difficulty; a prospective behavior test distinguishes old from corrected behavior; and it contains no answer-specific number, method mandate, or post-hoc threshold.

### CHG-B03 — Input-population reconciliation gate

- **Blind evidence.** The first Q1 implementation silently lost 131 otherwise valid rows because its gestational-age parser accepted `周+天` but not pure week values. The controller rejected that superficially successful run; the accepted run restored the audited population to 1082 rows and 267 women with zero core-field rejects. Evidence: frozen `code/Q1/reviews/q1_python_review.json`, finding `Q1-PY-002`.
- **Why this is a Skill defect.** R2 requires paths, shapes, missingness and analysis-domain checks, but it does not require a machine-readable reconciliation from audited input to parsed, eligible and actually used populations. A parser or filter can therefore discard valid observations while downstream fitting still looks successful.
- **Prospective corrected behavior.** A run must report audited, parsed, excluded, eligible and used row/entity counts; exclusions must have prospectively authorized reason counts that reconcile arithmetically; main and baseline must use the same eligible population unless an approved method contract explicitly explains the difference. Unexplained loss or mismatch blocks G3.
- **Anti-overfit boundary.** No 2025 C field syntax, row count, participant count or parser rule enters the Skill.

### CHG-B04 — Hard operating-constraint and abstention/triage guardrail

- **Blind evidence.** The original binary Q4 method met the aggregate sensitivity constraint in only 4/7 predeclared split seeds despite beating the baseline specificity in 7/7; its robustness verdict correctly failed. The human then activated F4. With thresholds calibrated only inside training data and an explicit abnormal / indeterminate-retest / not-flagged action contract, the F4 path preserved all three states in 7/7 seeds, met aggregate safety sensitivity in 7/7, and retained specificity dominance in 7/7. Evidence: frozen `robustness/Q4/q4_robustness_summary.json` and `robustness/Q4/q4_f4_robustness_summary.json`.
- **Why this is a Skill defect.** R2 mentions imbalance, calibration and alternate splits, but does not explicitly join the full safety contract across selection, implementation, robustness and reporting: threshold choice must be isolated from outer evaluation; entity/group leakage must be forbidden; a hard operating constraint must be rechecked under predeclared perturbations; and abstentions must never be counted as negatives or hidden from coverage reporting.
- **Prospective corrected behavior.** Tuning a threshold on outer-test labels, splitting repeated entities across train/test, counting an indeterminate case as a negative, omitting the deferral fraction, or comparing main and baseline under different action semantics must fail. A nested group-aware threshold procedure with the same action/metric contract for main and baseline, predeclared robustness checks, and explicit coverage/deferral reporting may pass.
- **Anti-overfit boundary.** No 0.90 constant, F4 name, disease context, seed list, model label or 2025-specific value enters the Skill. The human/modeler supplies the task-specific operating constraint and fallback semantics.

## Rejected changes

- Do not encode the 2025 C workbook schema or gestational-age notation.
- Do not mandate M1–M4, Weibull AFT, logistic regression, threshold envelopes, or three-way triage for unrelated problems.
- Do not insert the observed row counts, performance values, split seeds or sensitivity threshold into reusable instructions.
- Do not add a retest-capacity ceiling that the task owner never supplied.
- Do not revise the frozen blind analysis merely because no external answer source exists.

## P16 decision

Accept exactly the two coherent bundles above, the maximum allowed by the iteration plan. This is a controller decision under the user's standing authorization. No separate per-bundle decision was recorded. P17 may create a separate candidate from immutable release `B-LEAN-20260908-R2`; the formal target remains read-only.
