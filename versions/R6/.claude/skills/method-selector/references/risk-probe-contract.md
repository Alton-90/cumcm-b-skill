# Risk Probe Contract

Use only checks relevant to the method, but always cover executability, representative data coverage, output degeneracy, small perturbations, and scale.

## Canonical summary

Save `methods/Qx/probes/risk_probe_summary.json`:

The sole machine definition is [risk-probe.schema.json](../../workflow-orchestrator/schemas/risk-probe.schema.json). Emit one methods entry per screened method; put each applicable risk under its checks with status/reason/evidence. Method-level verdict remains PASS/CONDITIONAL/FAIL.

## Representative data

- Do not default to the first N rows.
- Preserve chronological order for forecasting probes.
- Use stratified or distribution-covering samples for imbalanced data.
- Use the full dataset for inexpensive distribution and concentration diagnostics.
- Record the selection rule and row count.

## Method-specific checks

- Evaluation/ranking: indicator redundancy, weight dominance, score variance, unique ranks, top-k mass, rank overlap under normalization/weight perturbations.
- Prediction: leakage, split validity, stationarity where assumed, residual behavior, interval coverage, baseline error, extrapolation limits.
- Optimization: constraint feasibility, slack, integrality, sensitivity to costs/capacities, solution implementability, runtime scaling.
- Clustering/classification: class or cluster imbalance, separation, label availability, calibration, stability across seeds.
- Mechanism models: units, identifiability, boundary/initial conditions, conservation, parameter sensitivity.
- Simulation: seed control, number of replications, distribution assumptions, confidence interval stability.

## Interpretation

- Prefer several cheap targeted checks over one impressive but weakly related metric.
- A concentration metric needs a problem-specific interpretation; low variance is not automatically bad when the expected truth is genuinely concentrated.
- Record thresholds before using them as pass/fail criteria, or label the verdict `CONDITIONAL`.
